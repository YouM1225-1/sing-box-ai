"""Audit the pinned local v0.1.12 rules and the fetched one-exit commit.
Run from any directory. Outputs evidence only; does not build or publish a release.
"""
import collections
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
BATCH = ROOT / 'artifacts/v0.1.12'
OLD = ROOT / 'docs/evidence/one-exit-b9d9f8a-2026-10-21'

def read(path):
    return json.loads(path.read_text())

def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = read(BATCH / 'manifest.json')
rules = read(BATCH / 'anthropic.json')['rules'][0]
source_rules = read(BATCH / 'anthropic-ip.json')['rules'][0]
assert (ROOT / 'VERSION').read_text().strip() == '0.1.12'
assert set(rules) == {'domain', 'domain_suffix', 'domain_keyword', 'ip_cidr'}
assert set(source_rules) == {'source_ip_cidr'}
protected = [ROOT / 'VERSION', ROOT / 'docs/plan.md']
for folder in ['sources', 'dist', 'artifacts/v0.1.12', 'scripts']:
    protected += [p for p in (ROOT / folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts]
before = {str(p.relative_to(ROOT)): sha(p) for p in protected}
for artifact in manifest['artifacts']:
    for name, expected in [(artifact['path'], artifact['sha256']), (artifact['source_path'], artifact['source_sha256'])]:
        assert sha(BATCH / name) == expected, name
    assert (ROOT / 'dist' / artifact['path']).read_bytes() == (BATCH / artifact['path']).read_bytes()

fetched = read(OUT / 'upstream-fetch.json')
assert fetched['commit']['sha'] == 'b9d9f8ab6687401f7588dfa7d7023cd58ffb4032'
template_checks = []
external = read(OLD / 'extracted-template-rules.json')['union']
for item in fetched['files']:
    content = item['content'].encode()
    assert content == (OLD / 'after' / item['path']).read_bytes()
    blob = b'blob ' + str(len(content)).encode() + b'\0' + content
    assert hashlib.sha1(blob).hexdigest() == item['sha']
    for entry in external:
        for occurrence in entry['templates']:
            if occurrence['file'] == item['path']:
                assert entry['type'] + ',' + entry['value'] + ',' in item['content'].splitlines()[occurrence['line'] - 1]
    template_checks.append({'file': item['path'], 'sha256': hashlib.sha256(content).hexdigest(), 'archive_equal': True})

groups = [
    ('产品主域与内容', 'domain_suffix', 'anthropic.com clau.de claude.ai claude.app claude.com claude.dev claudemcpclient.com claudemcpcontent.com claudeusercontent.com'),
    ('官网和身份服务扩展', 'domain_suffix', 'anthropic-com.ghost.io anthropic.auth0.com anthropic.com.cdn.cloudflare.net servd-anthropic-website.b-cdn.net'),
    ('身份验证与验证码', 'domain_suffix', 'withpersona.com hcaptcha.com'),
    ('身份验证与验证码', 'domain', 'challenges.cloudflare.com'),
    ('支付与结账', 'domain', 'api.stripe.com billing.stripe.com checkout.stripe.com js.stripe.com m.stripe.com r.stripe.com'),
    ('支付与结账', 'domain_suffix', 'stripe.network stripecdn.com'),
    ('客服', 'domain_suffix', 'intercom.io intercomcdn.com'),
    ('客服', 'domain', 'static.intercomassets.com'),
    ('遥测实验与风控共享服务', 'domain_suffix', 'growthbook.io segment.io statsigapi.net'),
    ('遥测实验与风控共享服务', 'domain', 'cdn.usefathom.com'),
    ('遥测实验与风控共享服务', 'domain_keyword', 'datadog sentry sift'),
    ('Artifacts 库与字体', 'domain', 'cdn.jsdelivr.net cdn.tailwindcss.com cdnjs.cloudflare.com code.jquery.com unpkg.com fonts.googleapis.com fonts.gstatic.com'),
    ('安装与插件', 'domain', 'formulae.brew.sh github.com raw.githubusercontent.com registry.npmjs.org storage.googleapis.com'),
    ('推送候选保留', 'domain', 'fcmtoken.googleapis.com'),
    ('可选外部集成', 'domain', 'api.revenuecat.com'),
    ('目的地址', 'ip_cidr', '153.61.224.0/22 160.79.104.0/21 2607:6bc0::/32 34.8.0.0/16'),
]
inventory = []
for group, kind, values in groups:
    for value in values.split():
        provenance = [p for p in manifest['provenance']['anthropic'] if (p['type'], p['value']) == (kind, value)]
        assert provenance, (kind, value)
        inventory.append({'group': group, 'type': kind, 'value': value, 'provenance': provenance})
expected_entries = {(kind, value) for kind, values in rules.items() for value in values}
assert len(inventory) == len(expected_entries) == 52
assert {(r['type'], r['value']) for r in inventory} == expected_entries
save('inventory.json', {'release': 'v0.1.12', 'kind': 'documentation-catalog-not-loadable-rule-set', 'destination': inventory, 'source': manifest['provenance']['anthropic-ip']})

def suffix(host, value):
    return host.endswith(value) if value.startswith('.') else host == value or host.endswith('.' + value)

def matches(host):
    return (host in rules['domain'] or any(suffix(host, v) for v in rules['domain_suffix'])
            or any(v in host for v in rules['domain_keyword']))

rows = []
hosts = set(rules['domain'])
# Normalization may absorb a documented exact host into a broader keyword.
# Keep those known witnesses when classifying a corresponding upstream service.
documented_hosts = [p['value'] for p in manifest['provenance']['anthropic'] if p['type'] == 'domain']
hosts.update(documented_hosts)
for entry in external:
    kind, value = entry['type'], entry['value']
    if not kind.startswith('DOMAIN'):
        continue
    if kind == 'DOMAIN-SUFFIX':
        full = any(suffix(value, v) for v in rules['domain_suffix']) or any(v in value for v in rules['domain_keyword'])
        partial = any(suffix(v.lstrip('.'), value) for v in rules['domain'] + rules['domain_suffix'])
        hosts.update([value, 'audit.' + value, 'a.b.' + value, value + '.invalid'])
    else:
        full = any(v in value for v in rules['domain_keyword'])
        partial = (any(value in v for v in rules['domain'] + rules['domain_suffix'])
                   or any(value in host and matches(host) for host in documented_hosts))
        hosts.update([value + '.example.org', 'audit-' + value + '-audit.example.org'])
    rows.append({'type': kind, 'value': value, 'status': 'full' if full else 'partial' if partial else 'no_dedicated_rule',
                 'new_in_any_template': any(t['added_in_this_template'] for t in entry['templates'])})
for value in rules['domain_suffix']:
    hosts.update([value, 'audit.' + value, 'a.b.' + value, 'not' + value, value + '.invalid'])
for value in rules['domain']:
    hosts.update(['audit.' + value, value + '.invalid'])
for value in rules['domain_keyword']:
    hosts.update([value + '.example.org', 'unrelated-' + value + '.invalid'])
hosts.update(['audit.datadog.pool.ntp.org', 'api.anthropic.com', 'cdn.usefathom.com', 'a.challenges.cloudflare.com', 'notclaude.ai', 'example.org'])
cases = []
for host in sorted(hosts):
    for ext in ['json', 'srs']:
        cases.append({'Name': 'domain:' + host, 'File': str((BATCH / ('anthropic.' + ext)).relative_to(ROOT)), 'Domain': host, 'Want': matches(host)})
addresses = {'192.0.2.1', '2001:db8::1'}
for value in rules['ip_cidr'] + source_rules['source_ip_cidr'] + ['2607:6bc0::/48', '2607:6bc0:11::/48']:
    net = ipaddress.ip_network(value)
    addresses.update(str(a) for a in [net.network_address, net.broadcast_address, net.network_address - 1, net.broadcast_address + 1])
for address in sorted(addresses):
    ip = ipaddress.ip_address(address)
    for name, active, direction in [('anthropic', rules['ip_cidr'], 'Destination'), ('anthropic-ip', source_rules['source_ip_cidr'], 'Source')]:
        hit = any(ip in ipaddress.ip_network(v) for v in active)
        for supplied in ['Source', 'Destination']:
            for ext in ['json', 'srs']:
                cases.append({'Name': supplied + ':' + address, 'File': str((BATCH / (name + '.' + ext)).relative_to(ROOT)), supplied: address, 'Want': hit and supplied == direction})
for domain in ['api.anthropic.com', 'example.org']:
    for destination in ['160.79.104.1', '192.0.2.1']:
        for ext in ['json', 'srs']:
            cases.append({'Name': 'domain-IP-OR', 'File': str((BATCH / ('anthropic.' + ext)).relative_to(ROOT)), 'Domain': domain, 'Destination': destination, 'Want': matches(domain) or destination == '160.79.104.1'})
# Harness resolves File relative to the case file; make every reference portable.
for case in cases:
    case['File'] = os.path.relpath(ROOT / case['File'], OUT)
save('native-cases.json', cases)
go = ROOT / '.tools/go1.27.1-restored/go/bin/go'
harness = ROOT / 'build/claude-rule-reorganization-harness'
env = dict(os.environ, GOMODCACHE=str(ROOT / '.tools/gomodcache'), GOCACHE=str(ROOT / '.tools/gocache'), GOPROXY='off', GOTOOLCHAIN='local')
subprocess.run([go, 'build', '-o', harness, '.'], cwd=ROOT / 'tests/harness', env=env, check=True)
native = subprocess.run([harness, OUT / 'native-cases.json'], capture_output=True, text=True, check=True)
(OUT / 'native-results.jsonl').write_text(native.stdout)
(OUT / 'native-summary.txt').write_text(native.stderr)
assert len(native.stdout.splitlines()) == len(cases)
assert all(json.loads(line)['pass'] for line in native.stdout.splitlines())
assert before == {str(p.relative_to(ROOT)): sha(p) for p in protected}
save('protected-file-hashes.json', before)
summary = {'checked_on': '2026-11-12', 'local_release': 'v0.1.12', 'field_counts': {k: len(v) for k, v in rules.items()},
           'destination_inventory_entries': len(inventory), 'source_entries': len(source_rules['source_ip_cidr']),
           'all_domain_scope_counts': dict(collections.Counter(r['status'] for r in rows)),
           'new_domain_scope_counts': dict(collections.Counter(r['status'] for r in rows if r['new_in_any_template'])),
           'domain_rows': rows, 'template_checks': template_checks, 'domain_witnesses': len(hosts), 'ip_witnesses': len(addresses),
           'native_cases': len(cases), 'native_failures': 0, 'protected_files_unchanged': len(before),
           'srs_hashes': {n: sha(BATCH / (n + '.srs')) for n in ['anthropic', 'anthropic-ip']},
           'harness_source_sha256': sha(ROOT / 'tests/harness/main.go'), 'go_version': subprocess.check_output([go, 'version'], text=True).strip(),
           'limitations': ['Local release verified against manifest and dist; no remote release download.',
                           'Native headless matching only, not consumer DNS, route priority, exit IP, payment, identity verification or IPv4 fallback.',
                           'Scope containment excludes incidental cross-keyword overlap and is not an enumeration of all domains.',
                           'No upstream script was executed. No product rules were changed.']}
save('audit-results.json', summary)
print(json.dumps({k: summary[k] for k in ['field_counts', 'all_domain_scope_counts', 'new_domain_scope_counts', 'domain_witnesses', 'ip_witnesses', 'native_cases', 'native_failures', 'protected_files_unchanged']}, ensure_ascii=False))
