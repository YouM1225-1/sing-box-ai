import argparse,json,os,pathlib,re,socket,subprocess,time
import loopback_dns as p
parser=argparse.ArgumentParser(description="Minimal alpha.9 DNS mixed domain/CIDR modern-vs-legacy and SRS-vs-inline mechanism regression.")
parser.add_argument("--binary",type=pathlib.Path,required=True)
parser.add_argument("--output",type=pathlib.Path,required=True)
args=parser.parse_args();BIN=args.binary.resolve();OUT=args.output.resolve();OUT.mkdir(parents=True,exist_ok=False)
FIX=pathlib.Path(__file__).resolve().parent/"fixtures"
assert "Revision: 132b38e9caaba1a1959354d518e54d2d08419afe" in subprocess.check_output([BIN,"version"],text=True)
def runtime_config(proxy,direct,port):
 return {"log":{"level":"debug","timestamp":False},"dns":{"disable_cache":True,"servers":[{"type":"udp","tag":s.tag,"server":"127.0.0.1","server_port":s.server_address[1]} for s in [proxy,direct]],"rules":[{"query_type":"HTTPS","action":"predefined"},{"rule_set":["geosite-openai","geosite-anthropic"],"query_type":"AAAA","action":"predefined"},{"rule_set":["geosite-openai","geosite-anthropic"],"server":"dns_proxy"},{"action":"evaluate","server":"dns_proxy"},{"match_response":True,"action":"respond"}],"final":"dns_proxy"},"inbounds":[{"type":"direct","tag":"dns","listen":"127.0.0.1","listen_port":port,"network":"udp"}],"outbounds":[{"type":"direct","tag":"direct"}],"route":{"default_domain_resolver":"dns_proxy","rule_set":[{"type":"local","format":"binary","tag":"geosite-"+p,"path":""} for p in ["openai","anthropic"]],"rules":[{"inbound":"dns","action":"hijack-dns"}]}}
QUERY={1:'A',28:'AAAA',16:'TXT',64:'SVCB',15:'MX',5:'CNAME',65:'HTTPS'}
def main():
 rows=[];checks=[];processes=[]
 for file in [FIX/(name+'.json') for name in ['old-openai','old-anthropic','fixture-openai','fixture-anthropic']]:
  subprocess.run([BIN,'rule-set','compile','--output',OUT/(file.stem+'.srs'),file],capture_output=True,check=True)
 proxy=p.upstream('dns_proxy',{1:'198.51.100.10',28:'2001:db8:ffff::10'});direct=p.upstream('dns_direct',{1:'192.0.2.20',28:'2001:db8:ffff::20'})
 try:
  for variant in ['old-srs','fixture-srs','old-inline','fixture-inline','legacy-old','legacy-fixture']:
   with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as reserve:reserve.bind(('127.0.0.1',0));port=reserve.getsockname()[1]
   old='old' in variant;cfg=runtime_config(proxy,direct,port)
   for i,entry in enumerate(cfg['route']['rule_set']):
    for product in ['openai','anthropic']:
     if entry['tag']=='geosite-'+product:
      path=FIX/(('old-' if old else 'fixture-')+product)
      if 'inline' in variant:cfg['route']['rule_set'][i]={'type':'inline','tag':entry['tag'],'rules':json.loads(path.with_suffix('.json').read_text())['rules']}
      else:entry['path']=str(OUT/(path.stem+'.srs'))
   env=os.environ.copy()
   if variant.startswith('legacy'):
    cfg['dns']['rules']=[{'rule_set':['geosite-openai','geosite-anthropic'],'server':'dns_proxy'}];cfg['dns']['final']='dns_direct';env['ENABLE_DEPRECATED_LEGACY_DNS_ADDRESS_FILTER']='true'
   file=OUT/(variant+'-dns-config.json');file.write_text(json.dumps(cfg,indent=2)+'\n')
   check=subprocess.run([BIN,'check','-c',file],capture_output=True,text=True,env=env);checks.append({'variant':variant,'exit':check.returncode,'stderr':check.stderr});assert check.returncode==0,check.stderr
   logpath=OUT/(variant+'-dns-runtime.log')
   with logpath.open('w') as log:
    proc=subprocess.Popen([BIN,'run','-c',file],stdout=log,stderr=subprocess.STDOUT,env=env)
    try:
     time.sleep(.15);assert proc.poll() is None,logpath.read_text()
     for host in ['auth.openai.com','api.anthropic.com','unmatched.audit-review.net']:
      for typ,name in QUERY.items():
       start=[len(proxy.events),len(direct.events)];answer=p.query(port,host,typ)
       rows.append({'variant':variant,'host':host,'qtype':name,**answer,'events':proxy.events[start[0]:]+direct.events[start[1]:]})
    finally:
     proc.terminate();proc.wait(timeout=3);processes.append({'variant':variant,'pid':proc.pid,'exited':proc.poll() is not None})
   contexts={};clean=re.sub(r'\x1b\[[0-9;]*m','',logpath.read_text())
   for line in clean.splitlines():
    m=re.search(r'\[(\d+) [^]]+\] dns: exchange (\S+) IN (\S+)$',line)
    if m:contexts[m[1]]=(m[2].rstrip('.'),m[3]);continue
    m=re.search(r'\[(\d+) [^]]+\] dns: match\[(\d+)\] (.*)',line)
    if m and m[1] in contexts:
     host,qt=contexts[m[1]];r=next(x for x in reversed(rows) if x['variant']==variant and x['host']==host and x['qtype']==qt);r.setdefault('matches',[]).append({'index':int(m[2]),'description':m[3]})
 finally:
  for s in [proxy,direct]:s.shutdown();s.server_close()
 assert len(rows)==126 and all(r['rcode']==0 for r in rows)
 for r in rows:
  if not r['variant'].startswith('legacy'):
   if r['qtype']=='HTTPS':expected=0
   elif r['host']=='unmatched.audit-review.net':expected=3
   elif r['qtype']=='AAAA':expected=1
   else:expected=2
   assert r['matches'][0]['index']==expected,r
  elif r['host']!='unmatched.audit-review.net' and r['qtype'] in ['TXT','SVCB','MX','CNAME']:
   assert [e['server'] for e in r['events']]==['dns_direct'],r
 lookup={(r['variant'],r['host'],r['qtype']):r for r in rows}
 for base in ['old','fixture']:
  for h in ['auth.openai.com','api.anthropic.com','unmatched.audit-review.net']:
   for qt in QUERY.values():
    a,b=lookup[base+'-srs',h,qt],lookup[base+'-inline',h,qt]
    assert a['answers']==b['answers'] and a.get('matches')==b.get('matches') and a['events']==b['events'],(a,b)
 (OUT/'non-address-results.json').write_text(json.dumps({'requests':126,'rows':rows,'checks':checks,'processes':processes,'assertions_passed':True,'legacy_warning':'Deprecated flag is set only in two isolated child processes to distinguish the old code path; no system/production environment changed.','conclusion':'Minimal five-rule modern fixture: TXT/SVCB/MX/CNAME hit product DNS rule2 despite IP-containing SRS; this reproducible fixture is distinct from the saved 22-rule N100-order observational matrix. Skipping was observed only in explicitly constructed legacy control. Inline and SRS route-set forms match for this matrix.'},indent=2)+'\n')
 print(json.dumps({'requests':126,'processes':len(processes),'assertions_passed':True,'modern_non_address_index':2,'legacy_non_address_server':'dns_direct'}))
if __name__=='__main__':main()
