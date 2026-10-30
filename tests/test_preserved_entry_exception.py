"""A single approved addition cannot renew or widen preserved compatibility evidence."""
import copy
import datetime as dt
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import ROOT, Invalid, load, preserved_entry_release_exception, review_entry, sha, write_json
from validate import release_gate


class PreservedEntryExceptionTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        shutil.copytree(ROOT / "sources", self.root / "sources")
        for relative in ("VERSION", "tests/fixtures/anthropic-v0.1.8.yaml", "artifacts/v0.1.8/manifest.json"):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        self.reference = load(self.root / "sources/policy.yaml")["preserved_entry_release_exception"]
        self.proof = load(self.root / self.reference["path"])
        self.row = self.proof["entries"][0]
        self.day = dt.date(2026, 10, 30)

    def update_proof(self, proof):
        path = self.root / self.reference["path"]
        write_json(path, proof)
        policy = load(self.root / "sources/policy.yaml")
        policy["preserved_entry_release_exception"]["sha256"] = sha(path)
        write_json(self.root / "sources/policy.yaml", policy)

    def test_exact_approved_delta_preserves_old_dates(self):
        review_entry(self.row, "release", self.day, self.root)
        self.assertEqual(self.row["last_verified"], "2026-09-27")
        self.assertEqual(self.row["review_after"], "2026-10-27")
        self.assertEqual(self.proof["additions"][0]["value"], "withpersona.com")

    def test_cannot_renew_another_date_or_version(self):
        with self.assertRaisesRegex(Invalid, "expired"):
            review_entry(self.row, "release", self.day + dt.timedelta(days=1), self.root)
        (self.root / "VERSION").write_text("0.1.10\n")
        with self.assertRaisesRegex(Invalid, "expired"):
            review_entry(self.row, "release", self.day, self.root)

    def test_rehashed_proof_cannot_claim_runtime_or_change_baseline(self):
        for mutate, message in (
            (lambda p: p.update(runtime_validation=True), "cannot claim runtime"),
            (lambda p: p["baseline_source"].update(sha256="0" * 64), "baseline hash"),
            (lambda p: p["entries"][0].update(last_verified="2026-10-30"), "unchanged review metadata"),
            (lambda p: p["additions"].append(copy.deepcopy(p["additions"][0])), "only the bound addition"),
            (lambda p: p["source_hashes"].update({"sources/openai.yaml": "0" * 64}), "source hash"),
        ):
            with self.subTest(message=message):
                proof = copy.deepcopy(self.proof)
                mutate(proof)
                self.update_proof(proof)
                with self.assertRaisesRegex(Invalid, message):
                    preserved_entry_release_exception(self.root, self.day)

    def test_extra_rule_or_changed_old_entry_is_rejected(self):
        path = self.root / "sources/anthropic.yaml"
        original = load(path)
        for rows in (original + [self.proof["additions"][0]], original[1:]):
            write_json(path, rows)
            with self.assertRaisesRegex(Invalid, "only the bound addition"):
                preserved_entry_release_exception(self.root, self.day)

    def test_publication_rejects_a_different_artifact_batch(self):
        review = load(self.root / "sources/release-review.json")
        review["artifacts"]["anthropic.srs"] = "0" * 64
        write_json(self.root / "sources/release-review.json", review)
        manifest = {"build_mode": "release", "project_version": "0.1.9", "artifacts": [{"path": k, "sha256": v} for k, v in review["artifacts"].items()], "inputs": {}, "validated_consumers": [], "integration_evidence": [], "deployment_status": "pending"}
        with patch("validate.canonical"), patch("validate.today", return_value=self.day):
            with self.assertRaisesRegex(Invalid, "exact artifact batch"):
                release_gate(self.root, manifest)


if __name__ == "__main__":
    unittest.main()
