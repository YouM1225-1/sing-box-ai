"""Verify canonical, parsed SRS semantics, native matches and reproducibility."""
import argparse
import datetime as dt
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from common import ARTIFACTS, OLD_IPS, ROOT, archives, canonical, compiler, date, input_files, load, local_path, need, run, semantic_key, sha, source_document, today, write_json


def reference_match(rows, domain="", source="", destination=""):
    """Small independent oracle for the allowed fields; not an SRS reader."""
    domain = domain.lower()
    for r in rows:
        typ, value = r["type"], r["value"]
        if typ == "domain" and domain == value:
            return True
        if typ == "domain_suffix" and domain and (domain.endswith(value if value.startswith(".") else "." + value) or not value.startswith(".") and domain == value):
            return True
        if typ == "domain_regex" and domain and re.search(value, domain):
            return True
        if typ in {"ip_cidr", "source_ip_cidr"}:
            addr = source if typ == "source_ip_cidr" else destination
            if addr and ipaddress.ip_address(addr) in ipaddress.ip_network(value):
                return True
    return False


def cases_for(selected):
    cases = []
    for artifact, rows in selected.items():
        def add(label, domain="", source="", destination="", fqdn="", expected=None):
            want = reference_match(rows, domain or fqdn, source, destination) if expected is None else expected
            for ext in ("json", "srs"):
                cases.append({"Name": artifact + ":" + label, "File": artifact + "." + ext, "Domain": domain, "Source": source, "Destination": destination, "FQDN": fqdn, "Want": want})
        for r in rows:
            typ, value = r["type"], r["value"]
            if typ in {"domain", "domain_suffix"}:
                root = value.lstrip(".")
                for host in (root, "a." + root, "b.a." + root, "not" + root, root + ".invalid"):
                    add(host, domain=host)
                add(root + ":upper", domain=root.upper())
                add(root + ":fqdn", fqdn=root)
            if typ in {"ip_cidr", "source_ip_cidr"}:
                net = ipaddress.ip_network(value)
                for ip in (str(net.network_address), str(net.broadcast_address)):
                    add(value + ":src:" + ip, source=ip)
                    add(value + ":dst:" + ip, destination=ip)
        for host in ("chatgpt-async-webps-prod-eastus-1.webpubsub.azure.com", "chatgpt-async-webps-prod-a.b-12.webpubsub.azure.com", "chatgpt-async-webps-prod-eastus-x.webpubsub.azure.com", "chatgpt-async-webps-prod-eastus-1.webpubsub.azure.com.evil.test"):
            add("baseline-regex:" + host, domain=host)
        for host in ("auth.openai.com", "chatgpt.com", "ws.chatgpt.com", "claude.ai", "claude.app", "challenges.cloudflare.com", "www.challenges.cloudflare.com", "challenges.cloudflare.com.example.org", "cloudflare.com", "www.cloudflare.com", "example.cloudflare.com", "notopenai.com", "auth.openai.com.example.org", "notclaude.ai", "cdnjs.cloudflare.com", "unrelated.example.org"):
            add("regression:" + host, domain=host)
        for ip in OLD_IPS + ("160.79.104.10", "160.79.106.1", "160.79.112.1", "2607:6bc0::1", "2001:db8::1", "203.0.113.1"):
            add("direction:src:" + ip, source=ip)
            add("direction:dst:" + ip, destination=ip)
        for ip in OLD_IPS:
            add("phased-out:" + ip, destination=ip, expected=False)
            add("phased-out-src:" + ip, source=ip, expected=False)
        if artifact in {"openai", "anthropic"}:
            add("challenge-required", domain="challenges.cloudflare.com", expected=True)
        if artifact == "anthropic":
            add("inbound-only-not-outbound", destination="160.79.106.1", expected=False)
            add("artifact-library", domain="cdnjs.cloudflare.com", expected=True)
        if artifact == "anthropic-ip":
            add("source-only", source="160.79.106.1", expected=True)
            add("source-not-destination", destination="160.79.106.1", expected=False)
    return cases


def harness(root, directory, go):
    lock = load(root / "tools.lock.json")
    env = os.environ.copy()
    env.update({"GOTOOLCHAIN": "local", "GOPROXY": "off", "GOSUMDB": "off", "GOWORK": "off"})
    version = run([go, "version"], env=env).stdout.split()
    need(len(version) >= 3 and version[2] == lock["go_version"], "Go toolchain version mismatch")
    cwd = root / "tests/harness"
    modules = run([go, "list", "-m", "github.com/sagernet/sing-box", "github.com/sagernet/sing"], cwd=cwd, env=env).stdout.splitlines()
    need("github.com/sagernet/sing-box v" + lock["sing_box"]["version"] in modules, "Harness sing-box dependency mismatch")
    need("github.com/sagernet/sing " + lock["sing_box"]["sing_module"] in modules, "Harness sing dependency mismatch")
    run([go, "mod", "verify"], cwd=cwd, env=env)
    executable = directory / "match-harness"
    run([go, "build", "-mod=readonly", "-trimpath", "-buildvcs=false", "-o", executable, "."], cwd=cwd, env=env)
    return executable, {"go_version": version[2], "sing_box_commit": lock["sing_box"]["commit"], "sing_module": lock["sing_box"]["sing_module"], "source_sha256": sha(cwd / "main.go"), "go_sum_sha256": sha(cwd / "go.sum")}


def release_gate(root, manifest):
    need(manifest["build_mode"] == "release", "Candidate batches cannot be released")
    canonical(root, "release", today())
    review = load(root / "sources/release-review.json")
    need(review.get("status") == "approved", "Release review/integration evidence is still pending")
    semantic_review = review.get("semantic_diff_review")
    need(isinstance(semantic_review, dict) and semantic_review.get("path") and semantic_review.get("sha256"), "Missing semantic diff review")
    semantic_path = local_path(root, semantic_review["path"])
    need(sha(semantic_path) == semantic_review["sha256"], "Semantic review record hash mismatch")
    artifact_hashes = {a["path"]: a["sha256"] for a in manifest["artifacts"]}
    need(review.get("artifacts") == artifact_hashes, "Review is for a different artifact batch")
    need(manifest.get("source_commit") and re.fullmatch(r"[0-9a-f]{40}", manifest["source_commit"]), "Release must identify a source commit")
    for relative, expected_hash in manifest["inputs"].items():
        committed = subprocess.run(["git", "show", f"{manifest['source_commit']}:{relative}"], cwd=root, capture_output=True)
        need(committed.returncode == 0 and hashlib.sha256(committed.stdout).hexdigest() == expected_hash, f"Input is not bound to the recorded source commit: {relative}")
    required = {"openai-login", "claude-login", "challenge", "stable-egress", "dns-routing", "voice", "artifacts", "plugins", "startup", "restart", "consumer-composition"}
    proofs = review.get("integration_evidence")
    need(isinstance(proofs, list) and proofs, "No consumer integration evidence")
    verified = []
    for e in proofs:
        path = local_path(root, e["path"])
        need(sha(path) == e["sha256"], "Integration evidence hash mismatch")
        proof = load(path)
        need(proof.get("result") == "passed" and proof.get("artifacts") == artifact_hashes, "Integration evidence failed or belongs to another batch")
        need(required <= set(proof.get("coverage", [])), "Integration coverage incomplete")
        need(all(proof.get(k) for k in ("platform", "version", "environment", "method", "address_families", "actual_egress", "consumer_config_sha256")), "Incomplete runtime evidence")
        need(re.fullmatch(r"[0-9a-f]{64}", proof["consumer_config_sha256"]), "Invalid config digest")
        need(date(proof["verified_on"]) <= today(), "Future integration evidence")
        need(set(manifest["enabled_optional"]) <= set(proof.get("validated_optional", [])), "Optional selection lacks integration evidence")
        verified.append({"platform": proof["platform"], "version": proof["version"], "address_families": proof["address_families"], "level": "maintainer-recorded-integration", "evidence": e})
    return verified


def validate(directory, go="go", for_release=False, root=ROOT):
    directory = Path(directory).resolve()
    manifest = load(directory / "manifest.json")
    need(isinstance(manifest, dict) and manifest.get("schema") == 2, "Empty/unknown manifest")
    need(manifest.get("build_mode") in {"candidate", "release"}, "Unknown manifest build_mode")
    if manifest["build_mode"] == "candidate":
        need(manifest.get("validated_consumers") == [] and manifest.get("integration_evidence") == [], "Candidate batches cannot claim runtime integration")
    need(manifest.get("inputs") == input_files(root), "Inputs changed since generation; rebuild the batch")
    selected, policy, normalization = canonical(root, manifest["build_mode"], date(manifest["review_as_of"]))
    need(manifest.get("features") == sorted(policy["features"]) and manifest.get("enabled_optional") == sorted(policy["enabled_optional"]), "Manifest feature policy mismatch")
    need(manifest.get("selected_pending") == sorted(policy.get("selected_pending", [])), "Manifest pending selection mismatch")
    need(manifest.get("baseline_inputs") == policy["baseline_inputs"] and manifest.get("provenance") == selected, "Manifest baseline/provenance mismatch")
    need(manifest.get("upstreams") == list(archives(root).values()) and manifest.get("normalization") == normalization, "Manifest input provenance mismatch")
    need(manifest.get("project_version") == (root / "VERSION").read_text().strip(), "Manifest project version mismatch")
    lock = load(root / "tools.lock.json")
    need(manifest.get("harness_dependencies") == {"go_version": lock["go_version"], "sing_module": lock["sing_box"]["sing_module"]}, "Manifest harness dependencies mismatch")
    need(manifest.get("field_counts") == {name: {k: len(v) for k, v in source_document(selected[name])["rules"][0].items()} for name in ARTIFACTS}, "Manifest field counts mismatch")
    need(manifest.get("rule_shape") == "one-default" and manifest.get("source_format_version") == 2 and manifest.get("format_min_reader_version") == "1.10.0", "Manifest structure mismatch")
    binary, compiler_info = compiler(root)
    need(manifest.get("compiler") == compiler_info, "Compiler differs from manifest")
    artifacts = manifest.get("artifacts")
    need(isinstance(artifacts, list) and len(artifacts) == 3, "Expected three artifacts")
    need({a.get("path") for a in artifacts} == {a + ".srs" for a in ARTIFACTS}, "Wrong/duplicate artifacts")
    with tempfile.TemporaryDirectory(prefix="sing-box-ai-validate-") as scratch:
        temp = Path(scratch)
        for artifact in artifacts:
            name = Path(artifact["path"]).stem
            need(artifact.get("source_path") == name + ".json", "Unexpected source filename")
            target, source = directory / artifact["path"], directory / artifact["source_path"]
            need(target.is_file() and source.is_file(), "Artifact missing")
            need(sha(target) == artifact.get("sha256") and sha(source) == artifact.get("source_sha256"), "Artifact hash mismatch")
            need(target.stat().st_size == artifact.get("bytes") and target.read_bytes()[:4] == b"SRS\x02" and artifact.get("binary_version") == 2, "Invalid SRS header/version/size")
            need(artifact.get("direction") == ("source" if name == "anthropic-ip" else "destination"), "Manifest direction mismatch")
            expected = source_document(selected[name])
            need(load(source) == expected, "Source JSON differs from current canonical")
            decoded = temp / (name + ".decoded.json")
            run([binary, "rule-set", "decompile", "--output", decoded, target])
            need(semantic_key(load(decoded)) == semantic_key(expected), "Source/binary semantic mismatch")
            # A second compiler invocation gets an independently recreated source file.
            recreate = temp / (name + ".json")
            rebuilt = temp / (name + ".srs")
            write_json(recreate, expected)
            run([binary, "rule-set", "compile", "--output", rebuilt, recreate])
            need(rebuilt.read_bytes() == target.read_bytes(), "Clean rebuild differs")
        cases = cases_for(selected)
        baseline_rows = {"baseline-" + name: [r for r in selected[name] if r["origin"] == "baseline"] for name in ("openai", "anthropic")}
        for name, rows in baseline_rows.items():
            artifact = name.removeprefix("baseline-")
            shutil.copyfile(local_path(root, policy["baseline_inputs"][artifact]["path"]), temp / (name + ".srs"))
            write_json(temp / (name + ".json"), source_document(rows))
        cases += cases_for(baseline_rows)
        for i, (expression, tests) in enumerate(policy["approved_regex"].items()):
            filename = f"regex-{i}.json"
            write_json(temp / filename, {"version": 2, "rules": [{"domain_regex": [expression]}]})
            run([binary, "rule-set", "compile", "--output", temp / f"regex-{i}.srs", temp / filename])
            for expected, hosts in ((True, tests["positive"]), (False, tests["negative"])):
                for host in hosts:
                    for ext in ("json", "srs"):
                        cases.append({"Name": "reviewed-regex:" + host, "File": f"regex-{i}.{ext}", "Domain": host, "Want": expected})
        write_json(temp / "cases.json", cases)
        native, harness_info = harness(root, temp, go)
        result = run([native, temp / "cases.json"])
        lines = [json.loads(s) for s in result.stdout.splitlines()]
        need(len(lines) == len(cases) and all(r.get("pass") is True for r in lines), "Native match results incomplete/failed")
        # Load three local SRS through the actual runtime constructor, without listeners.
        config = {"outbounds": [{"type": "direct", "tag": "direct"}], "route": {"rule_set": [{"type": "local", "tag": a, "format": "binary", "path": str(directory / (a + ".srs"))} for a in ARTIFACTS], "rules": [{"rule_set": a, "outbound": "direct"} for a in ARTIFACTS]}}
        write_json(temp / "check.json", config)
        run([binary, "check", "-c", temp / "check.json"])
        (directory / "matches.jsonl").write_text(result.stdout)
        write_json(directory / "cases.json", cases)
        manifest["validation"] = {"level": "local-source-binary-and-isolated-check", "cases": len(cases), "failures": 0, "clean_rebuild_equal": True, "baseline_complete": True, "upstream_crosscheck": "Native SRS baseline and DLC provenance equivalent", "native_result_sha256": sha(directory / "matches.jsonl"), "test_harness": harness_info}
    if for_release:
        manifest["validated_consumers"] = release_gate(root, manifest)
    write_json(directory / "manifest.json", manifest)
    return manifest


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory", nargs="?", type=Path, default=ROOT / "build/release")
    p.add_argument("--go", default="go")
    p.add_argument("--for-release", action="store_true", help="Check real UTC date and batch-bound integration evidence")
    a = p.parse_args()
    manifest = validate(a.directory, a.go, a.for_release)
    print(json.dumps({"mode": manifest["build_mode"], "cases": manifest["validation"]["cases"], "failures": 0, "release_gate_checked": a.for_release}))


if __name__ == "__main__":
    main()
