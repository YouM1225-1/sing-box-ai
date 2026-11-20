"""从同批目的规则派生 UniFi 文本；不联网、不部署、不授予发布资格。"""
import argparse
import hashlib
import ipaddress
import json
from pathlib import Path
import re

from common import ROOT, load, need, sha

EXPORT_VERSION = 1
NAMES = ("domains.txt", "ipv4.txt", "ipv6.txt", "manifest.json")


def render(batch, manifest):
    batch = Path(batch)
    domains, networks, mappings, omitted, sources = set(), set(), [], [], {}
    artifacts = manifest.get("artifacts", [])
    for name in ("openai", "anthropic"):
        records = [a for a in artifacts if a.get("path") == name + ".srs"]
        need(len(records) == 1, "Missing/duplicate destination artifact")
        record = records[0]
        need(record.get("direction") == "destination" and record.get("source_path") == name + ".json", "UniFi requires destination artifacts")
        for filename, digest in ((name + ".json", record.get("source_sha256")), (name + ".srs", record.get("sha256"))):
            need(sha(batch / filename) == digest, "UniFi source hash mismatch")
            sources[filename] = digest
        doc = load(batch / (name + ".json"))
        need(isinstance(doc, dict) and set(doc) == {"version", "rules"} and doc["version"] == 2, "Unknown UniFi source document")
        need(isinstance(doc["rules"], list) and len(doc["rules"]) == 1, "UniFi requires one default rule")
        rule = doc["rules"][0]
        need(isinstance(rule, dict) and rule and set(rule) <= {"domain", "domain_suffix", "domain_regex", "domain_keyword", "ip_cidr"}, "Unknown/source-only UniFi field")
        for kind, values in sorted(rule.items()):
            need(isinstance(values, list) and values and all(isinstance(v, str) and v for v in values), "Invalid UniFi source values")
            for value in sorted(set(values)):
                entry = {"artifact": name, "type": kind, "value": value}
                if kind in {"domain_regex", "domain_keyword"}:
                    omitted.append(entry)
                elif kind == "ip_cidr":
                    network = ipaddress.ip_network(value, strict=True)
                    need(network.is_global, "Non-global UniFi destination")
                    networks.add(network)
                else:
                    host = value[1:] if kind == "domain_suffix" and value.startswith(".") else value
                    need(len(host) <= 253 and re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", host), "Invalid UniFi domain")
                    need("." in host and all(0 < len(label) <= 63 and not label.startswith("-") and not label.endswith("-") for label in host.split(".")), "Invalid UniFi label")
                    domains.add(host)
                    mappings.append(dict(entry, output=host))
    lines = {"domains.txt": sorted(domains)}
    for family in (4, 6):
        ordered = sorted((n for n in networks if n.version == family), key=lambda n: (int(n.network_address), n.prefixlen))
        lines[f"ipv{family}.txt"] = [str(n.network_address) if n.prefixlen == n.max_prefixlen else str(n) for n in ordered]
    # 空表不能作为有效阻断清单发布；新地址族无内容时须单独审阅契约。
    need(all(lines.values()), "Empty UniFi export")
    payloads = {name: ("\n".join(values) + "\n").encode("utf-8") for name, values in lines.items()}
    metadata = {
        "schema": 1, "export_version": EXPORT_VERSION,
        "source_project_version": manifest["project_version"],
        "source_build_mode": manifest["build_mode"], "source_artifacts": sources,
        "files": {name: {"entries": len(lines[name]), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()} for name, data in payloads.items()},
        "domain_mappings": mappings, "omitted": omitted,
        "excluded_source_artifact": "anthropic-ip.srs",
        "limitations": [
            "域名文本不能保留 exact、suffix、regex、keyword 的完整匹配语义。",
            "suffix 前导点去除；可能扩大 apex 范围；regex/keyword 明列为未导出。",
            "保留目的规则的共享依赖与宽网段；不是纯官方最窄 IP 集合。",
            "静态导入需要手动同步；外部列表是否自动更新须在目标环境验证。",
            "生成、发布或控制器接受不代表实际阻断、DNS、IPv6、防绕过或重启验收。",
        ],
    }
    payloads["manifest.json"] = (json.dumps(metadata, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    return payloads


def write_exports(batch, manifest, output):
    payloads = render(batch, manifest)
    output = Path(output)
    need(not output.exists(), "UniFi output exists; choose a new directory")
    output.mkdir(parents=True)
    for name, data in payloads.items():
        (output / name).write_bytes(data)


def check_exports(batch, manifest, output):
    output = Path(output)
    expected = render(batch, manifest)
    need(output.is_dir() and {p.name for p in output.iterdir()} == set(NAMES), "Missing/extra UniFi export files")
    for name, data in expected.items():
        need((output / name).read_bytes() == data, "Stale/tampered UniFi export: " + name)


def check_current(root=ROOT, output=None):
    version = (root / "VERSION").read_text().strip()
    batch = root / "artifacts" / ("v" + version)
    manifest = load(batch / "manifest.json")
    need(manifest["project_version"] == version and manifest["build_mode"] == "release", "UniFi requires current release")
    need((manifest.get("validation") or {}).get("failures") == 0 and (manifest.get("publication_approval") or {}).get("scope") == "artifact-publication", "Unvalidated source release")
    for name in ("openai", "anthropic", "anthropic-ip"):
        need((root / "dist" / (name + ".srs")).read_bytes() == (batch / (name + ".srs")).read_bytes(), "Current SRS differs from archive")
    check_exports(batch, manifest, output if output is not None else root / "dist/unifi")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check-current", action="store_true")
    args = parser.parse_args()
    if args.check_current:
        need(args.batch is None, "Choose check-current or export")
        check_current(output=args.output)
    else:
        need(args.batch is not None and args.output is not None, "Specify batch and output")
        need(not any(args.output.resolve().is_relative_to(ROOT / folder) for folder in ("dist", "artifacts")), "Generate outside dist and archived artifacts")
        write_exports(args.batch, load(args.batch / "manifest.json"), args.output)
    print("UniFi export check passed")


if __name__ == "__main__":
    main()
