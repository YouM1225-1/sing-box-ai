"""Read-only comparison of fixed one-exit templates and local v0.1.6 SRS.
No upstream code is executed. Run from the sing-box-ai repository root.
"""
import collections
import datetime
import hashlib
import ipaddress
import json
from pathlib import Path
import re
import subprocess

ROOT = Path.cwd()
OUT = Path(__file__).resolve().parent
external = json.loads((OUT / 'extracted-template-rules.json').read_text())
local = {name: json.loads((ROOT / 'artifacts/v0.1.6' / (name + '.json')).read_text())['rules'][0] for name in ['anthropic', 'openai']}

def suffix_matches(host, value):
    return host.endswith(value) if value.startswith('.') else host == value or host.endswith('.' + value)

def hits(host, rules):
    found = []
    for kind, values in rules.items():
        for value in values:
            if ((kind == 'domain' and host == value)
                or (kind == 'domain_suffix' and suffix_matches(host, value))
                or (kind == 'domain_keyword' and value in host)
                or (kind == 'domain_regex' and re.search(value, host))):
                found.append({'type': kind, 'value': value})
    return found

def scope_comparison(typ, value, rules):
    full, partial = [], []
    if typ == 'DOMAIN-SUFFIX':
        for kind, values in rules.items():
            for rule in values:
                item = {'type': kind, 'value': rule}
                if kind == 'domain_keyword' and rule in value:
                    full.append(item)
                elif kind == 'domain_suffix':
                    if suffix_matches(value, rule): full.append(item)
                    elif suffix_matches(rule.lstrip('.'), value): partial.append(item)
                elif kind == 'domain' and suffix_matches(rule, value): partial.append(item)
    elif typ == 'DOMAIN-KEYWORD':
        for kind, values in rules.items():
            for rule in values:
                item = {'type': kind, 'value': rule}
                if kind == 'domain_keyword' and rule in value: full.append(item)
                elif kind in ['domain', 'domain_suffix'] and value in rule: partial.append(item)
        # Unrelated local keywords also intersect this upstream keyword language,
        # but cannot prove complete coverage. Report an explicit counterexample.
        if not full and rules.get('domain_keyword'):
            partial += [{'type': 'keyword-language-intersection', 'value': k} for k in rules['domain_keyword']]
    return {'status': 'full' if full else 'partial' if partial else 'no_dedicated_rule', 'full_by': full, 'partial_by': partial}

rows=[]
for entry in external['union']:
    if not entry['type'].startswith('DOMAIN'):continue
    row=dict(entry)
    row['coverage']={name:scope_comparison(entry['type'],entry['value'],rules) for name,rules in local.items()}
    statuses=[v['status'] for v in row['coverage'].values()]
    row['combined_status']='full' if 'full' in statuses else 'partial' if 'partial' in statuses else 'no_dedicated_rule'
    row['new_in_any_template']=any(x['added_in_this_template'] for x in row['templates'])
    rows.append(row)

hosts=set()
for row in rows:
    v=row['value']
    if row['type']=='DOMAIN-SUFFIX':hosts.update([v,'audit.'+v,'a.b.'+v,v+'.invalid'])
    else:hosts.update([v+'.example.org','audit-'+v+'-audit.example.org','browser-intake-datadoghq.com','browser-intake-us5-datadoghq.com'])
    for product in row['coverage'].values():
        for hit in product['partial_by']:
            if hit['type']=='domain':hosts.add(hit['value'])
hosts.update(['cdn.usefathom.com','a.cdn.usefathom.com','js.stripe.com','a.js.stripe.com','cdn.growthbook.io','a.challenges.cloudflare.com','m.stripe.network','js.stripecdn.com','api.segment.io','api.hcaptcha.com','new-browser-intake.example.org','api.statsigapi.net','cdn.jsdelivr.net','fonts.googleapis.com','storage.googleapis.com','static.intercomassets.com','servd-anthropic-website.b-cdn.net','api.openai.com','cdn.oaistatic.com'])
checks=[]
for name,rules in local.items():
    for host in sorted(hosts):
        expected=bool(hits(host,rules))
        result=subprocess.run([str(ROOT/'.tools/sing-box'),'--disable-color','rule-set','match','--format','binary',str(ROOT/'artifacts/v0.1.6'/(name+'.srs')),host],capture_output=True,text=True,check=True)
        output=(result.stdout+result.stderr).strip();actual='match rules.' in output
        checks.append({'artifact':name,'kind':'domain','value':host,'expected':expected,'matched':actual,'passed':actual==expected,'matching_rules':hits(host,rules),'native_output':output})

for name,rules in local.items():
    for value in ['160.79.104.0/21','2607:6bc0::/48','2607:6bc0:11::/48','2607:6bc0::/32']:
        network=ipaddress.ip_network(value)
        for address in [network.network_address,network.broadcast_address]:
            expected=any(address in ipaddress.ip_network(v) for v in rules.get('ip_cidr',[]) if ipaddress.ip_network(v).version==address.version)
            result=subprocess.run([str(ROOT/'.tools/sing-box'),'--disable-color','rule-set','match','--format','binary',str(ROOT/'artifacts/v0.1.6'/(name+'.srs')),str(address)],capture_output=True,text=True,check=True)
            output=(result.stdout+result.stderr).strip();actual='match rules.' in output
            checks.append({'artifact':name,'kind':'destination-ip','parent_cidr':value,'value':str(address),'expected':expected,'matched':actual,'passed':actual==expected,'native_output':output})
assert all(row['passed'] for row in checks)
result={'schema':1,'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'comparison_release':'v0.1.6','external_commit':'b9d9f8ab6687401f7588dfa7d7023cd58ffb4032','domain_rows':rows,'native_checks':checks,'native_count':len(checks),'native_passed':True,'limitations':['Full coverage derives from whole-rule containment, not from one apex witness.','no_dedicated_rule means no corresponding service rule; arbitrary host labels may coincidentally hit existing keywords.','Explicit template rules only; inherited subscription rules, process detection, actual routing order and remote DNS are not simulated.','SRS matching does not encode one-exit proxy or REJECT actions.','Only these known regular-expression patterns are probed; no general regex language inclusion is claimed.']}
(OUT/'comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
summary=collections.Counter(r['combined_status'] for r in rows if r['new_in_any_template'])
print(json.dumps({'all_domain_expressions':len(rows),'new_domain_expressions':sum(r['new_in_any_template'] for r in rows),'new_combined_coverage':dict(summary),'native_checks':len(checks),'native_passed':True},ensure_ascii=False))
