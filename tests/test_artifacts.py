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
