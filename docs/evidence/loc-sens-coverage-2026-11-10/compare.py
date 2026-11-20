from pathlib import Path
import collections, datetime, hashlib, ipaddress, json, re, subprocess
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
NAMES = ['anthropic', 'openai', 'anthropic-ip']

def normalize(obj):
    result = {}
    for k, values in obj['rules'][0].items():
        if isinstance(values, str):
            values = [values]
        if k.endswith('ip_cidr'):
            values = [str(ipaddress.ip_network(v)) for v in values]
        result[k] = sorted(set(values))
    return result

sets, checks = {}, {}
for name in NAMES:
    src = ROOT / 'dist' / (name + '.srs')
    dest = OUT / (name + '.json')
    subprocess.run([str(ROOT / '.tools/sing-box'), 'rule-set', 'decompile', str(src), '-o', str(dest)], check=True, capture_output=True)
    sets[name] = normalize(json.loads(dest.read_text()))
    published = normalize(json.loads((ROOT / 'artifacts/v0.1.10' / (name + '.json')).read_text()))
    checks[name] = {'sha256': hashlib.sha256(src.read_bytes()).hexdigest(), 'same_release_srs': src.read_bytes() == (ROOT / 'artifacts/v0.1.10' / (name + '.srs')).read_bytes(), 'same_release_rules': sets[name] == published}
    assert checks[name]['same_release_srs'] and checks[name]['same_release_rules']

def suffix_matches(host, value):
    return host.endswith(value) if value.startswith('.') else host == value or host.endswith('.' + value)

def matches(host, rules):
    hits = []
    for k, values in rules.items():
        for v in values:
            if (k == 'domain' and host == v) or (k == 'domain_suffix' and suffix_matches(host, v)) or (k == 'domain_keyword' and v in host) or (k == 'domain_regex' and re.search(v, host)):
                hits.append({'type': k, 'value': v})
    return hits

content = (OUT / 'loc-sens-clash.txt').read_bytes()
entries = [tuple(map(str.strip, line[2:].split(',', 1))) for line in content.decode().splitlines() if line.startswith('- ')]
rows, cases = [], []
for typ, val in dict.fromkeys(entries):
    per, witnesses = {}, {}
    for name, rules in sets.items():
        if typ == 'DOMAIN':
            hits = matches(val, rules)
            status, probes = ('full' if hits else 'none'), [val]
        elif typ == 'DOMAIN-SUFFIX':
            hits = [{'type': k, 'value': v} for k, values in rules.items() for v in values if (k == 'domain_keyword' and v in val) or (k == 'domain_suffix' and suffix_matches(val, v))]
            narrower = [{'type': k, 'value': v} for k in ['domain', 'domain_suffix'] for v in rules.get(k, []) if v.lstrip('.') == val or v.lstrip('.').endswith('.' + val)]
            status = 'full' if hits else ('partial' if narrower else 'none')
            hits = hits or narrower
            probes = [val, 'probe.' + val, 'b.a.' + val, 'not' + val, val + '.invalid'] + [h['value'].lstrip('.') for h in narrower]
        elif typ == 'DOMAIN-KEYWORD':
            hits = [{'type': 'domain_keyword', 'value': v} for v in rules.get('domain_keyword', []) if v in val]
            narrower = [{'type': k, 'value': v} for k in ['domain', 'domain_suffix'] for v in rules.get(k, []) if val in v]
            status = 'full' if hits else ('partial' if narrower else 'none')
            hits = hits or narrower
            probes = [val + '.example.org', 'before' + val + 'after.example.org', 'example.org.' + val] + [h['value'].lstrip('.') for h in narrower]
        else:
            assert typ == 'PROCESS-NAME'
            assert not any(k.startswith('process_') for k in rules)
            hits, status, probes = [], 'none', []
        per[name] = {'status': status, 'rules': hits}
        for host in dict.fromkeys(probes):
            found = matches(host, rules)
            witnesses.setdefault(host, {})[name] = found
            cases.append({'Name': f'{typ}:{val}:{host}:{name}', 'File': '../../../dist/' + name + '.srs', 'Domain': host, 'Want': bool(found)})
    union = 'full' if any(v['status'] == 'full' for v in per.values()) else 'partial' if any(v['status'] == 'partial' for v in per.values()) else 'none'
    rows.append({'type': typ, 'value': val, 'occurrences': entries.count((typ, val)), 'status': union, 'per_ruleset': per, 'witnesses': witnesses})
ntp = {}
for host in ['datadog.pool.ntp.org', '0.datadog.pool.ntp.org', '1.datadog.pool.ntp.org', 'a.b.datadog.pool.ntp.org', 'pool.ntp.org', '0.pool.ntp.org', 'time.google.com', 'time.apple.com', 'time.cloudflare.com']:
    ntp[host] = {name: matches(host, rules) for name, rules in sets.items()}
    for name, hits in ntp[host].items():
        cases.append({'Name': 'NTP:' + host + ':' + name, 'File': '../../../dist/' + name + '.srs', 'Domain': host, 'Want': bool(hits)})
result = {'checked_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'source_url': 'https://gist.githubusercontent.com/janlay/bec3cade3361678d975a8394d54515c6/raw/loc-sens-clash.txt', 'source_sha256': hashlib.sha256(content).hexdigest(), 'version': (ROOT / 'VERSION').read_text().strip(), 'raw_count': len(entries), 'unique_count': len(rows), 'summary': dict(collections.Counter(r['status'] for r in rows)), 'artifact_checks': checks, 'rows': rows, 'ntp': ntp}
(OUT / 'comparison.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
(OUT / 'cases.json').write_text(json.dumps(cases, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: result[k] for k in ['raw_count', 'unique_count', 'summary', 'artifact_checks']}, indent=2))
for r in rows:
    print(r['status'], r['type'], r['value'], ', '.join(n + ':' + p['status'] for n,p in r['per_ruleset'].items() if p['status'] != 'none'))
print('cases', len(cases))
