"""Pinned inputs for historical release assertions, independent of new supplements."""
from pathlib import Path
import shutil
import yaml


def restore_anthropic_v018(root):
    shutil.copyfile(Path(__file__).with_name("anthropic-v0.1.8.yaml"), root / "sources/anthropic.yaml")
    path = root / "sources/upstreams.yaml"
    registry = yaml.safe_load(path.read_text())
    registry["archives"] = [r for r in registry["archives"] if r["id"] not in {"claude-identity", "claude-identity-source"}]
    path.write_text(yaml.safe_dump(registry, sort_keys=False))
