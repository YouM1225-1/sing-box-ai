"""Publication metadata tests in disposable repositories, never real approvals."""
import copy
import datetime as dt
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import ROOT, Invalid, input_files, load, run, sha, write_json
from validate import consumer_integration_gate, release_gate


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ("sources", "scripts", "tests"):
            shutil.copytree(ROOT / folder, self.root / folder, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for name in ("VERSION", "tools.lock.json", "requirements.txt"):
            shutil.copyfile(ROOT / name, self.root / name)
        (self.root / ".tools").mkdir()
        (self.root / ".tools/sing-box").symlink_to(ROOT / ".tools/sing-box")
        self.version = (self.root / "VERSION").read_text().strip()
        candidate = load(ROOT / "artifacts/v0.1.0-rc.2/manifest.json")
        self.artifacts = {a["path"]: a["sha256"] for a in candidate["artifacts"]}
        evidence_path = "sources/evidence/publication-unit-proof.json"
        write_json(self.root / evidence_path, {"purpose": "synthetic unit fixture, not real validation"})
        self.authorization = {"schema": 1, "kind": "operator-authorization", "scope": "artifact-publication", "authorized_on": "2026-09-28", "project_version": self.version, "artifacts": self.artifacts, "instruction": "Synthetic unit fixture; no publication authorized", "deployment_authorized": False, "limitations": ["Synthetic fixture only; no N100 actions or consumer acceptance"]}
        self.semantic = {"schema": 1, "kind": "semantic-diff-review", "scope": "artifact-publication", "status": "approved", "reviewed_on": "2026-09-28", "project_version": self.version, "artifacts": self.artifacts, "unresolved_conflicts": [], "conclusion": "Synthetic fixture, not a review of a real publication", "evidence": [{"path": evidence_path, "sha256": sha(self.root / evidence_path)}]}
        self.review = {"schema": 2, "scope": "artifact-publication", "status": "approved", "project_version": self.version, "artifacts": self.artifacts, "deployment_status": "pending", "integration_evidence": []}
        self.record("operator_authorization", self.authorization)
        self.record("semantic_diff_review", self.semantic)
        # A real local Git object verifies the input-binding branch without mocks.
        run(["git", "init", "-q"], cwd=self.root)
        run(["git", "add", "VERSION", "tools.lock.json", "requirements.txt", "sources", "scripts", "tests"], cwd=self.root)
        run(["git", "-c", "core.hooksPath=/dev/null", "-c", "user.name=Unit fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "--no-verify", "-qm", "Synthetic test inputs"], cwd=self.root)
        self.manifest = {"build_mode": "release", "project_version": self.version, "artifacts": candidate["artifacts"], "source_commit": run(["git", "rev-parse", "HEAD"], cwd=self.root).stdout.strip(), "inputs": input_files(self.root), "validated_consumers": [], "integration_evidence": [], "deployment_status": "pending", "enabled_optional": [], "review_as_of": "2026-09-27"}
        self.clock = patch("validate.today", return_value=dt.date(2026, 9, 28))
        self.clock.start()
        self.addCleanup(self.clock.stop)

    def record(self, field, document):
        path = "sources/evidence/unit-" + field + ".json"
        write_json(self.root / path, document)
        self.review[field] = {"path": path, "sha256": sha(self.root / path)}
        write_json(self.root / "sources/release-review.json", self.review)

    def test_artifact_approval_leaves_consumers_and_deployment_pending(self):
        approval = release_gate(self.root, self.manifest)
        self.assertEqual(approval["scope"], "artifact-publication")
        self.assertEqual(approval["level"], "artifact-only")
        self.assertEqual(approval["deployment_status"], "pending")
        self.assertEqual(self.manifest["validated_consumers"], [])
        self.assertEqual(self.manifest["integration_evidence"], [])

    def test_missing_authorization_or_wrong_hash_is_rejected(self):
        for mutate in (lambda r: r.pop("operator_authorization"), lambda r: r["operator_authorization"].update(sha256="0" * 64)):
            with self.subTest(mutate=mutate):
                review = copy.deepcopy(self.review)
                mutate(review)
                write_json(self.root / "sources/release-review.json", review)
                with self.assertRaisesRegex(Invalid, "operator_authorization"):
                    release_gate(self.root, self.manifest)

    def test_operator_instruction_cannot_authorize_other_bytes_or_runtime(self):
        for changes in ({"kind": "runtime-validation"}, {"scope": "consumer-integration"}, {"project_version": "different"}, {"artifacts": {}}, {"authorized_on": "2026-09-29"}, {"instruction": " "}, {"deployment_authorized": True}, {"deployment_authorized": 0}, {"limitations": []}):
            with self.subTest(changes=changes):
                self.record("operator_authorization", {**self.authorization, **changes})
                with self.assertRaisesRegex(Invalid, "authorization"):
                    release_gate(self.root, self.manifest)

    def test_semantic_record_is_a_batch_review_not_just_a_hashed_file(self):
        for changes in ({"kind": "operator-authorization"}, {"scope": "consumer-integration"}, {"status": "pending"}, {"project_version": "different"}, {"artifacts": {}}, {"reviewed_on": "2026-09-29"}, {"unresolved_conflicts": ["unresolved"]}, {"conclusion": " "}, {"evidence": []}):
            with self.subTest(changes=changes):
                self.record("semantic_diff_review", {**self.semantic, **changes})
                with self.assertRaisesRegex(Invalid, "[Ss]emantic"):
                    release_gate(self.root, self.manifest)

    def test_current_utc_expiry_cannot_borrow_old_review_date(self):
        with patch("validate.today", return_value=dt.date(2026, 10, 27)):
            with self.assertRaisesRegex(Invalid, "expired"):
                release_gate(self.root, self.manifest)

    def test_candidate_runtime_claims_and_uncommitted_inputs_are_rejected(self):
        for changes in ({"build_mode": "candidate"}, {"validated_consumers": [{"result": "passed"}]}, {"integration_evidence": [{"result": "passed"}]}, {"deployment_status": "approved"}, {"source_commit": "0" * 40}, {"inputs": {"VERSION": "0" * 64}}):
            with self.subTest(changes=changes):
                with self.assertRaises(Invalid):
                    release_gate(self.root, {**self.manifest, **changes})
        for changes in ({"integration_evidence": [{"result": "passed"}]}, {"deployment_status": "approved"}):
            with self.subTest(review_changes=changes):
                write_json(self.root / "sources/release-review.json", {**self.review, **changes})
                with self.assertRaisesRegex(Invalid, "Artifact review cannot claim"):
                    release_gate(self.root, self.manifest)

    def test_consumer_gate_still_requires_real_scope_and_all_runtime_fields(self):
        with self.assertRaisesRegex(Invalid, "Consumer integration approval"):
            consumer_integration_gate(self.root, self.manifest, self.review)
        coverage = ["openai-login", "claude-login", "challenge", "stable-egress", "dns-routing", "voice", "artifacts", "plugins", "startup", "restart", "consumer-composition"]
        proof = {"result": "passed", "artifacts": self.artifacts, "coverage": coverage, "platform": "synthetic fixture", "version": "fixture", "environment": "synthetic fixture", "method": "unit fixture, not actual runtime", "address_families": ["IPv4"], "actual_egress": "synthetic", "consumer_config_sha256": "0" * 64, "verified_on": "2026-09-28"}
        path = self.root / "runtime-unit-fixture.json"
        review = {"scope": "consumer-integration", "status": "approved", "artifacts": self.artifacts}
        for changes in ({"coverage": [c for c in coverage if c != "restart"]}, {"actual_egress": None}, {"consumer_config_sha256": "invalid"}, {"artifacts": {}}, {"verified_on": "2026-09-29"}, {}):
            with self.subTest(changes=changes):
                write_json(path, {**proof, **changes})
                review["integration_evidence"] = [{"path": path.name, "sha256": sha(path)}]
                if changes:
                    with self.assertRaises(Invalid):
                        consumer_integration_gate(self.root, self.manifest, review)
                else:
                    self.assertEqual(len(consumer_integration_gate(self.root, self.manifest, review)), 1)


if __name__ == "__main__":
    unittest.main()
