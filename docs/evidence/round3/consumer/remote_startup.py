import argparse,hashlib,http.server,json,pathlib,socket,subprocess,threading,time
import loopback_dns as p
parser=argparse.ArgumentParser(description="Loopback-only alpha.9 remote startup/cache regression; no production configuration.")
parser.add_argument("--binary",type=pathlib.Path,required=True)
parser.add_argument("--output",type=pathlib.Path,required=True)
args=parser.parse_args();BIN=args.binary.resolve();OUT=args.output.resolve();OUT.mkdir(parents=True,exist_ok=False)
assert "Revision: 132b38e9caaba1a1959354d518e54d2d08419afe" in subprocess.check_output([BIN,"version"],text=True)
responses={};requests=[]
class Handler(http.server.BaseHTTPRequestHandler):
 def do_GET(self):
  status,content=responses.get(self.path,(503,b'offline'))
  requests.append({'path':self.path,'status':status,'if_none_match':self.headers.get('If-None-Match')})
  self.send_response(status);self.send_header('Content-Length',str(len(content)));self.end_headers();self.wfile.write(content)
 def log_message(self,*a):pass

def main():
 for name in ['old','new','wrong']:
  f=OUT/(name+'-startup.json');f.write_text(json.dumps({'version':2,'rules':[{'domain':[name+'.audit-review.net']}]})+'\n')
  subprocess.run([BIN,'rule-set','compile','--output',OUT/(name+'-startup.srs'),f],capture_output=True,check=True)
 (OUT/'invalid-startup.srs').write_bytes(b'not an SRS')
 httpd=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=httpd.serve_forever,daemon=True).start()
 dns=p.upstream('upstream',{1:'192.0.2.55',28:'2001:db8::55'})
 base='http://127.0.0.1:'+str(httpd.server_address[1]);rows=[]
 def run(label,url,cache,expect,initial=None,expected_host=None):
  with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as reserve:reserve.bind(('127.0.0.1',0));port=reserve.getsockname()[1]
  rule={'type':'remote','tag':'product','format':'binary','url':base+url,'update_interval':'24h'}
  if initial:rule['initial_path']=str(OUT/initial)
  cfg={'log':{'level':'debug'},'dns':{'disable_cache':True,'servers':[{'type':'udp','tag':'upstream','server':'127.0.0.1','server_port':dns.server_address[1]}],'rules':[{'rule_set':'product','query_type':'A','action':'predefined'}],'final':'upstream'},'inbounds':[{'type':'direct','tag':'dns','listen':'127.0.0.1','listen_port':port,'network':'udp'}],'outbounds':[{'type':'direct','tag':'direct'}],'http_clients':[{'tag':'local-http'}],'route':{'default_http_client':'local-http','default_domain_resolver':'upstream','rule_set':[rule],'rules':[{'inbound':'dns','action':'hijack-dns'}]},'experimental':{'cache_file':{'enabled':True,'path':str(OUT/cache)}}}
  f=OUT/(label+'-config.json');f.write_text(json.dumps(cfg,indent=2)+'\n');log=OUT/(label+'.log');start=len(requests);answers=[]
  with log.open('w') as stream:
   child=subprocess.Popen([BIN,'run','-c',f],stdout=stream,stderr=subprocess.STDOUT)
   try:
    for _ in range(50):
     if child.poll() is not None or 'sing-box started' in log.read_text():break
     time.sleep(.02)
    started=child.poll() is None and 'sing-box started' in log.read_text()
    assert started==expect,(label,log.read_text())
    if started:
     for host in ['old','new','wrong']:
      result=p.query(port,host+'.audit-review.net',1);answers.append({'host':host,**result})
      assert result['rcode']==0 and (result['answer_count']==0)==(host==expected_host),(label,answers)
   finally:
    if child.poll() is None:child.terminate()
    child.wait(timeout=3)
  row={'case':label,'url':url,'cache_file':cache,'initial_path':initial,'started':started,'process_exit':child.returncode,'http_requests':requests[start:],'answers':answers,'cache_sha256':hashlib.sha256((OUT/cache).read_bytes()).hexdigest() if (OUT/cache).exists() else None}
  rows.append(row);return row
 try:
  responses['/old.srs']=(200,(OUT/'old-startup.srs').read_bytes())
  run('01-seed-old','/old.srs','shared-cache.db',True,expected_host='old')
  responses['/old.srs']=(503,b'offline')
  same=run('02-same-url-offline','/old.srs','shared-cache.db',True,expected_host='old');assert not same['http_requests']
  responses['/new.srs']=(503,b'offline')
  run('03-new-url-offline','/new.srs','shared-cache.db',False)
  run('04-rollback-before-new-fetch','/old.srs','shared-cache.db',True,expected_host='old')
  responses['/new.srs']=(200,(OUT/'new-startup.srs').read_bytes())
  run('05-new-url-success','/new.srs','shared-cache.db',True,expected_host='new')
  run('06-rollback-after-new-fetch','/old.srs','shared-cache.db',False)
  responses['/new.srs']=(503,b'offline')
  run('07-initial-missing','/new.srs','missing-cache.db',False,initial='does-not-exist.srs')
  run('08-initial-invalid','/new.srs','invalid-cache.db',False,initial='invalid-startup.srs')
  run('09-initial-valid-wrong-content','/new.srs','wrong-cache.db',True,initial='wrong-startup.srs',expected_host='wrong')
  run('10-initial-valid-correct','/new.srs','correct-cache.db',True,initial='new-startup.srs',expected_host='new')
  run('11-rollback-with-old-initial','/old.srs','shared-cache.db',True,initial='old-startup.srs',expected_host='old')
  # Remote schema has no embedded rules fallback; check rejects it.
  cfg=json.loads((OUT/'01-seed-old-config.json').read_text());cfg['route']['rule_set'][0]['rules']=[{'domain':['old.audit-review.net']}]
  f=OUT/'unsupported-remote-inline-config.json';f.write_text(json.dumps(cfg,indent=2)+'\n')
  check=subprocess.run([BIN,'check','-c',f],capture_output=True,text=True);assert check.returncode!=0 and 'rules' in check.stderr
  (OUT/'remote-inline-rejection.json').write_text(json.dumps({'exit':check.returncode,'stderr':check.stderr.replace(str(OUT),'OUTPUT')},indent=2)+'\n')
 finally:
  httpd.shutdown();httpd.server_close();dns.shutdown();dns.server_close()
 (OUT/'remote-startup-results.json').write_text(json.dumps({'cases':rows,'assertions_passed':True,'network':'All HTTP/DNS endpoints/listeners loopback. No N100 access.','limitations':['No production proxy boot dependency simulated; controlled HTTP503 represents fetch failure.','Cache tests use fresh local alpha.9-created caches, not N100 cache.','A syntactically valid wrong initial SRS is accepted: URL/expected-hash identity is not checked by runtime.']},indent=2)+'\n')
 print(json.dumps({'cases':len(rows),'started':[r['case'] for r in rows if r['started']],'failed_as_expected':[r['case'] for r in rows if not r['started']],'remote_embedded_rules':'rejected'}))
if __name__=='__main__':main()
