import argparse,json,pathlib,re,socket,subprocess,time,hashlib
import loopback_dns as p
parser=argparse.ArgumentParser(description="Loopback DNS/route witnesses; supporting geosites are explicitly reduced exact-domain projections.")
parser.add_argument("--binary",type=pathlib.Path,required=True);parser.add_argument("--output",type=pathlib.Path,required=True)
args=parser.parse_args();BIN=args.binary.resolve();OUT=args.output.resolve();OUT.mkdir(parents=True,exist_ok=False)
FIX=pathlib.Path(__file__).resolve().parent/"fixtures";WITNESS=json.loads((FIX/"exit-witnesses.json").read_text());HOSTS=WITNESS["hosts"]
assert "Revision: 132b38e9caaba1a1959354d518e54d2d08419afe" in subprocess.check_output([BIN,"version"],text=True)
def runtime_config(batch,proxy,direct,port,snapshot):
 tags=set()
 for r in snapshot['rules']:tags.update(vals(r.get('rule_set',[])))
 sets=[]
 for tag in sorted(tags):
  name=tag
  if tag in ['geosite-openai','geosite-anthropic']:name=batch+'-'+tag.removeprefix('geosite-')
  elif tag=='geosite-ai':name='n100-geosite-ai'
  sets.append({'type':'local','format':'binary','tag':tag,'path':str(OUT/(name+'.srs'))})
 servers=[{'type':'udp','tag':tag,'server':'127.0.0.1','server_port':server.server_address[1]} for tag,server in [('dns_proxy',proxy),('dns_direct',direct),('dns_local',direct)]]
 servers += [{'type':'hosts','tag':tag,'path':[],'predefined':{'unused-fixture.invalid':['192.0.2.254']}} for tag in ['hosts','dns_mdns']]
 return {'log':{'level':'debug','timestamp':False},'dns':{'strategy':'prefer_ipv4','disable_cache':True,'servers':servers,'rules':snapshot['rules'],'final':snapshot['final']},'inbounds':[{'type':'direct','tag':'dns','listen':'127.0.0.1','listen_port':port,'network':'udp'}],'outbounds':[{'type':'direct','tag':'direct'}],'route':{'default_domain_resolver':'dns_proxy','rule_set':sets,'rules':[{'inbound':'dns','action':'hijack-dns'}]},'experimental':{'clash_api':{'default_mode':'Rule'}}}
def vals(v):return [v] if isinstance(v,str) else v
def matches(doc,h):
 return any(h in vals(r.get('domain',[])) or any(h.endswith(s) if s.startswith('.') else h==s or h.endswith('.'+s) for s in vals(r.get('domain_suffix',[]))) or any(re.search(p,h) for p in vals(r.get('domain_regex',[]))) for r in doc['rules'])
def main():
 files={}
 for name,hosts in WITNESS['supporting_exact_domains'].items():
  f=OUT/(name+'.json');f.write_text(json.dumps({'version':2,'rules':[{'domain':hosts}] if hosts else []}));files[name]=f
 f=OUT/'geoip-cn.json';f.write_text(json.dumps({'version':2,'rules':[{'ip_cidr':['114.114.114.114/32','240e::/16']}]}));files['geoip-cn']=f
 for batch,prefix in [('old','old'),('rc1','rc1'),('candidate','fixture')]:
  for prod in ['openai','anthropic']:files[batch+'-'+prod]=FIX/(prefix+'-'+prod+'.json')
 matrix={h:{} for h in HOSTS}
 for name,f in files.items():
  doc=json.loads(f.read_text())
  subprocess.run([BIN,'rule-set','compile','--output',OUT/(name+'.srs'),f],capture_output=True,check=True)
  for h in HOSTS:matrix[h][name]=bool(matches(doc,h))
 snapshot=WITNESS['dns'];route=WITNESS['route_rules']
 def first(host,batch,version):
  m=matrix[host].copy();m['geosite-ai']=m['n100-geosite-ai']
  for prod in ['openai','anthropic']:m['geosite-'+prod]=m[batch+'-'+prod]
  for i,r in enumerate(route):
   if i in [0,1,2,3,4,5,6,7,8,9,17]:continue
   if r.get('ip_version') and r['ip_version']!=version:continue
   if not (any(m.get(t,False) for t in vals(r.get('rule_set',[]))) or host in vals(r.get('domain',[])) or any(host==s or host.endswith('.'+s) for s in vals(r.get('domain_suffix',[])))):continue
   return {'index':i,'action':r.get('action','route'),'outbound':r.get('outbound')}
  return {'index':'final','action':'route','outbound':'proxy'}
 rows=[];processes=[];proxy=p.upstream('dns_proxy',{1:'198.51.100.10',28:'2001:db8:ffff::10'});direct=p.upstream('dns_direct',{1:'192.0.2.20',28:'2001:db8:ffff::20'})
 try:
  for batch in ['old','rc1','candidate']:
   with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as reserve:reserve.bind(('127.0.0.1',0));port=reserve.getsockname()[1]
   cfg=runtime_config(batch,proxy,direct,port,snapshot)
   f=OUT/('exit-'+batch+'-config.json');f.write_text(json.dumps(cfg,indent=2)+'\n');log=OUT/('exit-'+batch+'.log')
   check=subprocess.run([BIN,'check','-c',f],capture_output=True,text=True);assert check.returncode==0,check.stderr
   with log.open('w') as stream:
    child=subprocess.Popen([BIN,'run','-c',f],stdout=stream,stderr=subprocess.STDOUT)
    try:
     time.sleep(.15);assert child.poll() is None,log.read_text()
     for host in HOSTS:
      for typ in [1,28]:
       start=[len(proxy.events),len(direct.events)];ans=p.query(port,host,typ);rows.append({'batch':batch,'host':host,'qtype':{1:'A',28:'AAAA'}[typ],**ans,'events':proxy.events[start[0]:]+direct.events[start[1]:]})
    finally:child.terminate();child.wait(timeout=3);processes.append({'batch':batch,'pid':child.pid,'stopped':child.poll() is not None})
   contexts={}
   for line in re.sub(r'\x1b\[[0-9;]*m','',log.read_text()).splitlines():
    m=re.search(r'\[(\d+) [^]]+\] dns: exchange (\S+) IN (A|AAAA)$',line)
    if m:contexts[m[1]]=(m[2].rstrip('.'),m[3]);continue
    m=re.search(r'\[(\d+) [^]]+\] dns: match\[(\d+)\] (.*)',line)
    if m and m[1] in contexts:
     h,q=contexts[m[1]];row=next(r for r in reversed(rows) if r['batch']==batch and r['host']==h and r['qtype']==q);row.setdefault('matches',[]).append({'index':int(m[2]),'description':m[3]})
 finally:
  for s in [proxy,direct]:s.shutdown();s.server_close()
 assert len(rows)==162 and all(r['rcode']==0 and r['matches'] for r in rows)
 table=[]
 for h in HOSTS:
  out={'host':h,'native_membership':{k:v for k,v in matrix[h].items() if v},'batches':{}}
  for b in ['old','rc1','candidate']:
   out['batches'][b]={'dns':{q:{'first_index':next(r for r in rows if (r['batch'],r['host'],r['qtype'])==(b,h,q))['matches'][0]['index'],'answer_count':next(r for r in rows if (r['batch'],r['host'],r['qtype'])==(b,h,q))['answer_count']} for q in ['A','AAAA']},'conditional_route':{'ipv4':first(h,b,4),'ipv6':first(h,b,6)}}
  table.append(out)
 result={'hosts':27,'original_native_cases':837,'original_native_failures':0,'this_run_native_cases':0,'requests':162,'processes':processes,'input_sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files.values()},'rows':rows,'table':table,'conditions':['DNS measured on loopback with synthetic upstreams and witness-only supporting geosite projections; full original memberships were verified by the original run, not re-verified here. Saved 22 DNS objects/order retained.','candidate is pinned review source fixture; final-build equality is recorded separately.','Route is conditional static inference from native rule-set membership, Rule mode, TCP443, usable domain metadata, no IP/ASN/private/protocol/earlier bypass. Not actual traffic or unknown destination-IP behavior.','Route snapshot is repository canonical including AWS additions; every host is checked for AWS membership explicitly.','Regex has two witnesses, not exhaustive enumeration of its language. Suffix has apex and one subdomain representative.']}
 (OUT/'exit-consumer-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'hosts':27,'requests':162,'this_run_native_cases':0,'processes_stopped':len(processes),'rows':[{ 'host':t['host'],'dns':{b:[t['batches'][b]['dns'][q]['first_index'] for q in ['A','AAAA']] for b in ['old','rc1','candidate']},'route_v6':{b:t['batches'][b]['conditional_route']['ipv6']['index'] for b in ['old','rc1','candidate']}} for t in table]},ensure_ascii=False))
if __name__=='__main__':main()
