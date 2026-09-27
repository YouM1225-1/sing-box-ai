"""Run after generation with SINGBOX_TEST_BATCH=build/candidate."""
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import Invalid, sha, write_json
from validate import validate


@unittest.skipUnless(os.environ.get("SINGBOX_TEST_BATCH"), "Generate a batch first")
class ArtifactAdversaries(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.batch = Path(self.temp.name) / "batch"
        shutil.copytree(os.environ["SINGBOX_TEST_BATCH"], self.batch)

    def forge_hash(self):
        path = self.batch / "manifest.json"
        manifest = json.loads(path.read_text())
        item = next(a for a in manifest["artifacts"] if a["path"] == "openai.srs")
        item.update(sha256=sha(self.batch / "openai.srs"), bytes=(self.batch / "openai.srs").stat().st_size)
        write_json(path, manifest)

    def test_manifest_cannot_forge_baseline_provenance_or_build_contract(self):
        path = self.batch / "manifest.json"
        original = json.loads(path.read_text())
        mutations = {
            "baseline/provenance": lambda m: m["baseline_inputs"]["openai"].update(sha256="0" * 64),
            "provenance": lambda m: m["provenance"]["openai"].pop(),
            "field counts": lambda m: m["field_counts"]["openai"].update(domain=999),
            "harness dependencies": lambda m: m["harness_dependencies"].update(go_version="unverified"),
            "pending selection": lambda m: m.update(selected_pending=["openai:domain:unknown.example.org"]),
            "project version": lambda m: m.update(project_version="forged"),
            "input provenance": lambda m: m["upstreams"].pop(),
            "runtime integration": lambda m: m.update(validated_consumers=[{"result": "passed"}]),
            "cannot claim runtime": lambda m: m.update(integration_evidence=[{"result": "passed"}]),
        }
        for message, mutate in mutations.items():
            with self.subTest(message=message):
                modified = json.loads(json.dumps(original))
                mutate(modified)
                write_json(path, modified)
                with self.assertRaisesRegex(Invalid, message):
                    validate(self.batch)
        write_json(path, original)

    def test_plain_text_is_not_an_srs_even_with_matching_manifest_hash(self):
        (self.batch / "openai.srs").write_bytes(b"not a ruleset")
        self.forge_hash()
        with self.assertRaisesRegex(Invalid, "Invalid SRS header"):
            validate(self.batch)

    def test_magic_and_hash_cannot_hide_a_corrupt_payload(self):
        (self.batch / "openai.srs").write_bytes(b"SRS\x02invalid-zlib-data")
        self.forge_hash()
        with self.assertRaisesRegex(Invalid, "Command failed"):
            validate(self.batch)

    def test_parseable_but_wrong_binary_is_rejected(self):
        shutil.copyfile(self.batch / "anthropic.srs", self.batch / "openai.srs")
        self.forge_hash()
        with self.assertRaisesRegex(Invalid, "semantic mismatch"):
            validate(self.batch)


if __name__ == "__main__":
    unittest.main()
