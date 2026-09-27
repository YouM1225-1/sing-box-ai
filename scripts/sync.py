"""Classify pinned discovery inputs; never edits canonical rules or dist/."""
import argparse
import json
from pathlib import Path
import urllib.request

from common import ARTIFACTS, ROOT, archives, canonical, covered, discovery_entries, load, local_path, need, normalize, parse_dlc, sha, write_json


def report(root=ROOT, previous=None):
    registry = archives(root)
    selected, policy, _ = canonical(root)
    output = {"schema": 2, "discovery": [], "removed_upstream": [], "canonical": selected, "canonical_diff": {}, "baselines": policy["baseline_inputs"], "baseline_rules": {name: [r for r in rows if r["origin"] == "baseline"] for name, rows in selected.items()}, "supplements": {}, "baseline_diff": {}, "supplement_diff": {}, "upstream_hashes": {k: v["sha256"] for k, v in registry.items()}}
    for artifact in ("openai", "anthropic"):
        ref = "dlc-" + artifact
        for candidate in parse_dlc(local_path(root, registry[ref]["path"]).read_text()):
            typ = candidate["type"]
            classification = "TOO_BROAD" if typ == "domain_keyword" else "ALREADY_COVERED" if covered(candidate, selected[artifact]) else "ADD_CANDIDATE"
            output["discovery"].append({"artifact": artifact, "upstream": ref, **candidate, "classification": classification})
    history = load(local_path(root, registry["legacy-anthropic"]["path"]))
    for entry in history["entries"]:
        if entry["value"] in {"cdn.growthbook.io", "cdn.usefathom.com", "challenges.cloudflare.com", "clau.de"}:
            candidate = {"type": "domain_suffix" if entry["type"] == "DOMAIN-SUFFIX" else "domain", "value": entry["value"]}
            output["discovery"].append({"artifact": "anthropic", "upstream": "legacy-anthropic", **candidate, "classification": "ALREADY_COVERED" if covered(candidate, selected["anthropic"]) else "ADD_CANDIDATE"})
    for artifact in ("openai", "anthropic", "anthropic-ip"):
        rows = load(root / f"sources/{artifact}.yaml")
        output["supplements"][artifact] = rows
        for row in rows:
            if row["status"] in {"optional", "feature-required"}:
                output["discovery"].append({"artifact": artifact, "upstream": "official", "type": row["type"], "value": row["value"], "classification": "OPTIONAL_OFFICIAL" if row["status"] == "optional" else "FEATURE_REQUIRED"})
    for row in discovery_entries(root):
        output["discovery"].append({**row, "upstream": row["sources"][0]["reference"], "selected": row["id"] in policy.get("selected_pending", []), "classification": "ALREADY_COVERED" if covered(row, selected[row["artifact"]]) else "ADD_CANDIDATE"})
    if previous:
        old = load(previous)
        need(old.get("schema") in (1, 2) and "discovery" in old and "canonical" in old, "Invalid previous sync report")
        key = lambda r: (r["artifact"], r["upstream"], r["type"], r["value"])
        current_keys = {key(r) for r in output["discovery"]}
        output["removed_upstream"] = [{**r, "classification": "REMOVED_UPSTREAM"} for r in old["discovery"] if key(r) not in current_keys]
        for artifact, rows in output["canonical"].items():
            identify = lambda r: (r["type"], r["value"], r["direction"])
            before = {identify(r): r for r in old["canonical"].get(artifact, [])}
            after = {identify(r): r for r in rows}
            output["canonical_diff"][artifact] = {"added": [after[k] for k in sorted(after.keys() - before.keys())], "removed": [before[k] for k in sorted(before.keys() - after.keys())], "changed": [{"before": before[k], "after": after[k]} for k in sorted(before.keys() & after.keys()) if before[k] != after[k]]}
        for artifact in ("openai", "anthropic"):
            identify = lambda r: (r["type"], r["value"], r["direction"])
            before = {identify(r): r for r in old.get("baseline_rules", {}).get(artifact, [])}
            after = {identify(r): r for r in output["baseline_rules"][artifact]}
            output["baseline_diff"][artifact] = {"before_input": old.get("baselines", {}).get(artifact), "after_input": output["baselines"][artifact], "added": [after[k] for k in sorted(after.keys() - before.keys())], "removed": [before[k] for k in sorted(before.keys() - after.keys())], "changed": [{"before": before[k], "after": after[k]} for k in sorted(before.keys() & after.keys()) if before[k] != after[k]]}
        for artifact in ARTIFACTS:
            identify = lambda r: (r["type"], r["value"], r["direction"])
            before = {identify(r): r for r in old.get("supplements", old["canonical"]).get(artifact, [])}
            after = {identify(r): r for r in output["supplements"][artifact]}
            output["supplement_diff"][artifact] = {"added": [after[k] for k in sorted(after.keys() - before.keys())], "removed": [before[k] for k in sorted(before.keys() - after.keys())], "changed": [{"before": before[k], "after": after[k]} for k in sorted(before.keys() & after.keys()) if before[k] != after[k]]}
        output["changed_upstream_hashes"] = {k: {"before": old.get("upstream_hashes", {}).get(k), "after": v} for k, v in output["upstream_hashes"].items() if old.get("upstream_hashes", {}).get(k) != v}
    return output


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, default=ROOT / "build/sync.json")
    p.add_argument("--previous", type=Path)
    p.add_argument("--fetch", action="store_true", help="Restore missing pinned archives only; never update hashes")
    a = p.parse_args()
    if a.fetch:
        for entry in load(ROOT / "sources/upstreams.yaml")["archives"]:
            path = local_path(ROOT, entry["path"])
            if path.exists():
                continue
            need(entry["kind"] not in {"official", "official-source-record"}, "Structured facts/source records must be restored from Git, not overwritten with HTML")
            need(entry["url"].startswith("https://"), "HTTPS required")
            with urllib.request.urlopen(entry["url"], timeout=30) as response:
                content = response.read(2_000_001)
            import hashlib
            need(len(content) <= 2_000_000 and hashlib.sha256(content).hexdigest() == entry["sha256"], "Downloaded archive hash mismatch")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    write_json(a.output, report(previous=a.previous))
    print(f"Discovery report: {a.output}")


if __name__ == "__main__":
    main()
