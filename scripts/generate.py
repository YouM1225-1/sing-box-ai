"""Compile one isolated batch. Never writes dist/; validation publishes it later."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from common import ARTIFACTS, ROOT, archives, canonical, compiler, date, input_files, load, need, run, sha, source_document, write_json


def build(output, mode="release", review_as_of=None, root=ROOT):
    output = Path(output).resolve()
    need(output != root / "dist" and not output.is_relative_to(root / "dist"), "Generation into dist is forbidden")
    need(not output.exists(), "Output already exists; choose a new batch directory")
    selected, policy, normalization = canonical(root, mode, review_as_of)
    binary, compiler_info = compiler(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".batch-", dir=output.parent))
    try:
        artifacts = []
        for name in ARTIFACTS:
            source = stage / f"{name}.json"
            target = stage / f"{name}.srs"
            write_json(source, source_document(selected[name]))
            run([binary, "rule-set", "compile", "--output", target, source])
            need(target.read_bytes()[:4] == b"SRS\x02", "Unexpected binary format/version")
            artifacts.append({"path": target.name, "sha256": sha(target), "source_path": source.name, "source_sha256": sha(source), "bytes": target.stat().st_size, "binary_version": 2, "direction": "source" if name == "anthropic-ip" else "destination"})
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True)
        manifest = {
            "schema": 1, "build_mode": mode, "project_version": (root / "VERSION").read_text().strip(),
            "review_as_of": str(review_as_of or date(policy["review_as_of"])),
            "source_commit": commit.stdout.strip() if commit.returncode == 0 else None,
            "inputs": input_files(root), "upstreams": list(archives(root).values()), "compiler": compiler_info,
            "features": sorted(policy["features"]), "enabled_optional": sorted(policy["enabled_optional"]),
            "source_format_version": 2, "format_min_reader_version": "1.10.0", "rule_shape": "one-default",
            "normalization": normalization, "artifacts": artifacts,
            "validation": None, "validated_consumers": [], "integration_evidence": [],
        }
        write_json(stage / "manifest.json", manifest)
        os.rename(stage, output)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return manifest


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mode", choices=["candidate", "release"], default="release")
    p.add_argument("--output", type=Path)
    p.add_argument("--review-as-of")
    a = p.parse_args()
    output = a.output or ROOT / "build" / a.mode
    build(output, a.mode, date(a.review_as_of) if a.review_as_of else None)
    print(f"Generated {a.mode} batch: {output}")


if __name__ == "__main__":
    main()
