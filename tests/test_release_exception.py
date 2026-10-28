"""The v0.1.8 carry-forward permission cannot renew or expand old validation."""
import copy
import datetime as dt
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import ROOT, Invalid, canonical, load, review_entry, sha, write_json
from validate import release_gate


class UnchangedReleaseExceptionTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        shutil.copytree(ROOT / "sources", self.root / "sources")
        shutil.copyfile(ROOT / "tools.lock.json", self.root / "tools.lock.json")
        (self.root / "VERSION").write_text("0.1.8\n")
        (self.root / ".tools").mkdir()
        (self.root / ".tools/sing-box").symlink_to(ROOT / ".tools/sing-box")
        self.row = next(r for r in load(self.root / "sources/anthropic.yaml") if r["value"] == "challenges.cloudflare.com")
        self.reference = load(self.root / "sources/policy.yaml")["unchanged_release_exception"]

    def test_approved_exception_preserves_dates_and_sources(self):
        before = copy.deepcopy(self.row)
        selected = canonical(self.root, "release", dt.date(2026, 10, 28))[0]
        row = next(r for r in selected["anthropic"] if r["value"] == self.row["value"])
        self.assertEqual({k: v for k, v in row.items() if k != "origin"}, before)
        self.assertEqual(row["review_after"], "2026-10-27")
        self.assertEqual(row["last_verified"], "2026-09-27")

    def test_exception_does_not_apply_to_another_date_or_version(self):
        for day in (27, 29):
            with self.assertRaisesRegex(Invalid, "expired"):
                review_entry(self.row, "release", dt.date(2026, 10, day), self.root)
        (self.root / "VERSION").write_text("0.1.9\n")
        with self.assertRaisesRegex(Invalid, "expired"):
            review_entry(self.row, "release", dt.date(2026, 10, 28), self.root)

    def test_exception_requires_pinned_proof_and_unchanged_sources(self):
        proof = self.root / self.reference["path"]
        original = proof.read_bytes()
        proof.write_bytes(original + b"\n")
        with self.assertRaisesRegex(Invalid, "exception hash mismatch"):
            review_entry(self.row, "release", dt.date(2026, 10, 28), self.root)
        proof.write_bytes(original)
        with (self.root / "sources/anthropic.yaml").open("a") as stream:
            stream.write("\n# changed input\n")
        with self.assertRaisesRegex(Invalid, "unchanged sources"):
            review_entry(self.row, "release", dt.date(2026, 10, 28), self.root)

    def test_exception_cannot_claim_runtime_validation(self):
        path = self.root / self.reference["path"]
        proof = load(path)
        proof["runtime_validation"] = True
        write_json(path, proof)
        policy = load(self.root / "sources/policy.yaml")
        policy["unchanged_release_exception"]["sha256"] = sha(path)
        write_json(self.root / "sources/policy.yaml", policy)
        with self.assertRaisesRegex(Invalid, "cannot claim runtime"):
            review_entry(self.row, "release", dt.date(2026, 10, 28), self.root)

    def test_publication_rejects_changed_anthropic_bytes(self):
        review = load(self.root / "sources/release-review.json")
        review["artifacts"]["anthropic.srs"] = "0" * 64
        write_json(self.root / "sources/release-review.json", review)
        manifest = {"build_mode": "release", "project_version": "0.1.8", "artifacts": [{"path": k, "sha256": v} for k, v in review["artifacts"].items()], "validated_consumers": [], "integration_evidence": [], "deployment_status": "pending"}
        with patch("validate.today", return_value=dt.date(2026, 10, 28)):
            with self.assertRaisesRegex(Invalid, "unchanged artifact bytes"):
                release_gate(self.root, manifest)


if __name__ == "__main__":
    unittest.main()
