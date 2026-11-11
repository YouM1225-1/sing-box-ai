"""Pinned inputs for historical release assertions, independent of new supplements."""
from pathlib import Path
import json
import shutil
import yaml


def restore_official_ips_v011(root):
    """Keep historical assertions bound to their original IP snapshots."""
    snapshot = json.loads(Path(__file__).with_name("official-ip-v0.1.11.json").read_text())
    for relative, content in snapshot["files"].items():
        (root / relative).write_text(content)
    path = root / "sources/upstreams.yaml"
    registry = yaml.safe_load(path.read_text())
    previous = {row["id"]: row for row in snapshot["archives"]}
    registry["archives"] = [previous.get(row["id"], row) for row in registry["archives"]]
    path.write_text(yaml.safe_dump(registry, sort_keys=False))


def restore_anthropic_v018(root):
    restore_official_ips_v011(root)
    shutil.copyfile(Path(__file__).with_name("anthropic-v0.1.8.yaml"), root / "sources/anthropic.yaml")
    path = root / "sources/upstreams.yaml"
    registry = yaml.safe_load(path.read_text())
    registry["archives"] = [r for r in registry["archives"] if r["id"] not in {"claude-identity", "claude-identity-source"}]
    path.write_text(yaml.safe_dump(registry, sort_keys=False))


def restore_anthropic_v019(root):
    restore_official_ips_v011(root)
    shutil.copyfile(Path(__file__).with_name("anthropic-v0.1.9.yaml"), root / "sources/anthropic.yaml")
