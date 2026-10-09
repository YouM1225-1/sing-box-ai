"""Exact network coverage approval must not become a general CIDR bypass."""
import datetime as dt
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import ROOT, Invalid, canonical, load, review_entry, sha, write_json


class NetworkReviewTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        shutil.copytree(ROOT / "sources", self.root / "sources")
        shutil.copyfile(ROOT / "tools.lock.json", self.root / "tools.lock.json")
        (self.root / ".tools").mkdir()
        (self.root / ".tools/sing-box").symlink_to(ROOT / ".tools/sing-box")
        self.reference = "sources/evidence/anthropic-network-coverage-2026-10-09.json"

    def save(self, path, document):
        (self.root / path).write_text(yaml.safe_dump(document, allow_unicode=True, sort_keys=False))

    def alter_row(self, **changes):
        rows = load(self.root / "sources/anthropic.yaml")
        row = next(r for r in rows if r.get("product") == ["claude-network-coverage"])
        row.update(changes)
        self.save("sources/anthropic.yaml", rows)

    def alter_proof(self, **changes):
        path = self.root / self.reference
        proof = load(path)
        proof.update(changes)
        write_json(path, proof)
        policy = load(self.root / "sources/policy.yaml")
        anchor = next(a for a in policy["initial_confirmations"] if a["reference"] == self.reference)
        anchor["sha256"] = sha(path)
        self.save("sources/policy.yaml", policy)

    def alter_snapshot(self, ident, mutate):
        registry = load(self.root / "sources/upstreams.yaml")
        item = next(r for r in registry["archives"] if r["id"] == ident)
        path = self.root / item["path"]
        document = load(path)
        mutate(document)
        write_json(path, document)
        item["sha256"] = sha(path)
        self.save("sources/upstreams.yaml", registry)

    def validate(self, as_of=dt.date(2026, 10, 9)):
        return canonical(self.root, "release", as_of)

    def test_exact_network_approval_and_expiry(self):
        selected, _, _ = self.validate()
        row = next(r for r in selected["anthropic"] if r["value"] == "2607:6bc0:11::/48")
        self.assertEqual(row["direction"], "destination")
        self.assertEqual(row["status"], "compatibility")
        self.assertNotIn("official", {s["kind"] for s in row["sources"]})
        with self.assertRaisesRegex(Invalid, "Unapproved/expired compatibility: 2607:6bc0:11::/48"):
            review_entry(row, "release", dt.date(2026, 11, 8), self.root)

    def test_changed_confirmation_cannot_skip_policy_hash(self):
        path = self.root / self.reference
        proof = load(path)
        proof["statement"] += " edited"
        write_json(path, proof)
        with self.assertRaisesRegex(Invalid, "pinned initial approval"):
            self.validate()

    def test_reauthorized_broad_or_unannounced_prefix_still_fails(self):
        for prefix in ("2607:6bc0::/32", "2607:6bc0:10::/47", "160.79.104.0/21", "2607:6bc0:12::/48", "2607:6bc1:11::/48"):
            with self.subTest(prefix=prefix):
                self.alter_row(value=prefix)
                self.alter_proof(rule={"type": "ip_cidr", "value": prefix})
                with self.assertRaises(Invalid):
                    self.validate()

    def test_network_approval_cannot_claim_service_or_consumer_validation(self):
        for field in ("service_usage_verified", "consumer_validation"):
            with self.subTest(field=field):
                self.alter_proof(**{field: True})
                with self.assertRaisesRegex(Invalid, "must not claim"):
                    self.validate()
                self.alter_proof(**{field: False})

    def test_network_confirmation_binds_artifact_direction_and_scope(self):
        for field, value in (("artifact", "openai"), ("direction", "source"), ("scope", "runtime-integration")):
            with self.subTest(field=field):
                original = load(self.root / self.reference)[field]
                self.alter_proof(**{field: value})
                with self.assertRaisesRegex(Invalid, "scope/rule mismatch"):
                    self.validate()
                self.alter_proof(**{field: original})

    def test_untrusted_registry_url_cannot_masquerade_as_primary(self):
        registry = load(self.root / "sources/upstreams.yaml")
        item = next(r for r in registry["archives"] if r["id"] == "as399358-rdap")
        item["url"] = "https://example.invalid/copied-rdap.json"
        self.save("sources/upstreams.yaml", registry)
        with self.assertRaisesRegex(Invalid, "primary source mismatch"):
            self.validate()

    def test_rehashed_routing_snapshot_must_attest_exact_prefix_and_date(self):
        original = load(self.root / "sources/network/as399358-announced-prefixes-2026-10-09.json")
        mutations = [
            lambda d: d["data"].update(resource="12345"),
            lambda d: d["data"].update(latest_time="2026-10-08T00:00:00"),
            lambda d: d["data"].update(prefixes=[r for r in d["data"]["prefixes"] if r["prefix"] != "2607:6bc0:11::/48"]),
            lambda d: d["data"].update(prefixes=[{"prefix": "2607:6bc0:11::/48", "timelines": [{"starttime": "2026-09-25T00:00:00", "endtime": "2026-10-08T00:00:00"}]}]),
        ]
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.alter_snapshot("as399358-announced-prefixes", mutation)
                with self.assertRaises(Invalid):
                    self.validate()
                self.alter_snapshot("as399358-announced-prefixes", lambda d: (d.clear(), d.update(original)))

    def test_rehashed_arin_snapshot_must_preserve_anthropic_ownership(self):
        cases = [
            ("as399358-rdap", lambda d: d.update(startAutnum=12345)),
            ("anthropic-ipv6-rdap", lambda d: d.update(entities=[])),
            ("anthropic-ipv6-rdap", lambda d: d.update(endAddress="2607:6bc0::ffff")),
        ]
        registry = load(self.root / "sources/upstreams.yaml")
        for ident, mutation in cases:
            with self.subTest(ident=ident):
                path = next(r["path"] for r in registry["archives"] if r["id"] == ident)
                original = load(self.root / path)
                self.alter_snapshot(ident, mutation)
                with self.assertRaises(Invalid):
                    self.validate()
                self.alter_snapshot(ident, lambda d: (d.clear(), d.update(original)))


if __name__ == "__main__":
    unittest.main()
