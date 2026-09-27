"""Adversarial policy checks; native source/binary tests run in validate.py."""
import copy
import datetime as dt
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import ROOT, Invalid, canonical, date, load, normalize, public_suffix, review_entry, semantic_key, write_json
from sync import parse_dlc, report
from validate import cases_for, release_gate


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "sources", self.root / "sources")

    def change(self, artifact, mutate):
        path = self.root / f"sources/{artifact}.yaml"
        rows = load(path)
        mutate(rows)
        path.write_text(yaml.safe_dump(rows, allow_unicode=True, sort_keys=False))

    def test_baseline_and_user_confirmation(self):
        selected, policy, _ = canonical(self.root, "release", dt.date(2026, 9, 27))
        challenge = next(r for r in selected["anthropic"] if r["value"] == "challenges.cloudflare.com")
        self.assertEqual(challenge["review_status"], "approved")
        self.assertEqual(len([r for r in selected["openai"] if r["type"] == "ip_cidr"]), 23)
        self.assertTrue(len(cases_for(selected)) > 500)
        self.assertEqual(policy["enabled_optional"], [])

    def test_missing_official_fact_is_not_silently_omitted(self):
        self.change("openai", lambda r: r.pop(0))
        with self.assertRaisesRegex(Invalid, "Missing official baseline"):
            canonical(self.root)

    def test_claiming_official_provenance_does_not_authorize_new_host(self):
        self.change("openai", lambda r: r[0].update(value=".unrelated.example.org"))
        with self.assertRaisesRegex(Invalid, "No matching official fact"):
            canonical(self.root)

    def test_source_cannot_become_destination(self):
        self.change("anthropic-ip", lambda r: r[0].update(type="ip_cidr", direction="destination"))
        with self.assertRaises(Invalid):
            canonical(self.root)

    def test_unknown_type_and_status(self):
        for key, value in (("type", "domain_keyword"), ("status", "trusted"), ("direction", "both")):
            with self.subTest(key=key):
                path = self.root / "sources/openai.yaml"
                saved = path.read_text()
                self.change("openai", lambda r: r[0].update({key: value}))
                with self.assertRaises(Invalid):
                    canonical(self.root)
                path.write_text(saved)

    def test_broad_domains_and_networks(self):
        for value in (".cloudflare.com", ".amazonaws.com", ".co.uk", ".azurewebsites.net"):
            with self.subTest(value=value):
                path = self.root / "sources/openai.yaml"
                saved = path.read_text()
                self.change("openai", lambda r: r[0].update(value=value))
                with self.assertRaises(Invalid):
                    canonical(self.root)
                path.write_text(saved)
        for value in ("0.0.0.0/0", "::/0"):
            with self.assertRaises(Invalid):
                normalize("ip_cidr", value)

    def test_shared_marker_and_feature_cannot_be_silently_changed(self):
        self.change("anthropic", lambda rows: next(r for r in rows if r["value"] == "cdnjs.cloudflare.com").update(shared_dependency=False))
        with self.assertRaises(Invalid):
            canonical(self.root)

    def test_archive_mutation_detected(self):
        with (self.root / "sources/official/chatgpt-voice.json").open("a") as f:
            f.write(" ")
        with self.assertRaisesRegex(Invalid, "hash mismatch"):
            canonical(self.root)

    def test_pending_expiry_and_both_compatibility_classes(self):
        original = next(r for r in load(self.root / "sources/anthropic.yaml") if r["value"] == "challenges.cloudflare.com")
        for status in ("compatibility", "compatibility-critical"):
            row = copy.deepcopy(original)
            row["status"] = status
            with self.subTest(status=status, test="before-expiry"):
                review_entry(row, "release", dt.date(2026, 10, 26), self.root)
            for as_of in (dt.date(2026, 10, 27), dt.date(2026, 10, 28)):
                with self.subTest(status=status, date=as_of):
                    with self.assertRaisesRegex(Invalid, "expired"):
                        review_entry(row, "release", as_of, self.root)
                    review_entry(row, "candidate", as_of, self.root)
            row.update(review_status="pending", last_verified=None, review_after=None)
            review_entry(row, "candidate", dt.date(2026, 9, 27), self.root)
            with self.assertRaises(Invalid):
                review_entry(row, "release", dt.date(2026, 9, 27), self.root)

    def test_review_metadata_attacks(self):
        original = next(r for r in load(self.root / "sources/anthropic.yaml") if r["value"] == "challenges.cloudflare.com")
        mutations = [
            lambda r: r.pop("evidence"),
            lambda r: r.update(review_status="trusted"),
            lambda r: r.update(last_verified="2026-09-28"),
            lambda r: r.update(review_after="2026-10-28"),
            lambda r: r.update(first_seen="2026-09-28"),
            lambda r: r.update(last_verified=None),
            lambda r: r.update(last_verified="2026-02-30"),
            lambda r: r.update(evidence=[r["evidence"][0]]),
            lambda r: r["evidence"][-1].update(product=["openai"]),
            lambda r: r["evidence"][-1].update(reference="../../outside.json"),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                row = copy.deepcopy(original)
                mutate(row)
                with self.assertRaises(Invalid):
                    review_entry(row, "candidate", dt.date(2026, 9, 27), self.root)

    def test_bad_regex_is_not_approved_by_anchors(self):
        self.change("openai", lambda rows: rows[0].update(type="domain_regex", value=r"^(?:allowed\.example\.com|.*)$"))
        with self.assertRaisesRegex(Invalid, "Regex"):
            canonical(self.root)

    def test_candidate_cannot_be_published(self):
        with self.assertRaisesRegex(Invalid, "Candidate batches"):
            release_gate(self.root, {"build_mode": "candidate"})

    def test_previous_validation_is_not_new_batch_integration(self):
        with patch("validate.today", return_value=dt.date(2026, 9, 27)):
            with self.assertRaisesRegex(Invalid, "still pending"):
                release_gate(self.root, {"build_mode": "release"})


class FormatTests(unittest.TestCase):
    def test_domain_and_idna_boundaries(self):
        self.assertEqual(normalize("domain_suffix", ".EXAMPLE.COM."), ".example.com")
        self.assertEqual(normalize("domain_suffix", "EXAMPLE.COM."), "example.com")
        self.assertEqual(normalize("domain", "bücher.example"), "xn--bcher-kva.example")
        for value in ("*.example.com", "bad..example", "-bad.example", "1.2.3.4", "https://example.com", "a_b.example"):
            with self.assertRaises(Invalid):
                normalize("domain", value)

    def test_psl_exact_wildcard_exception(self):
        psl = {"com", "uk", "co.uk", "*.ck", "!www.ck"}
        self.assertEqual(public_suffix("foo.co.uk", psl), "co.uk")
        self.assertEqual(public_suffix("a.ck", psl), "a.ck")
        self.assertEqual(public_suffix("www.ck", psl), "ck")

    def test_shape_and_semantic_equivalence(self):
        root = {"version": 2, "rules": [{"domain_suffix": ["example.com"]}]}
        expanded = {"version": 2, "rules": [{"domain": ["example.com", "a.example.com"], "domain_suffix": [".example.com"]}]}
        wildcard = {"version": 2, "rules": [{"domain_suffix": [".example.com"]}]}
        self.assertEqual(semantic_key(root), semantic_key(expanded))
        self.assertNotEqual(semantic_key(root), semantic_key(wildcard))
        for rule in ({}, {"invert": True, "domain": "example.com"}, {"type": "logical", "rules": []}, {"domain_keyword": ["openai"]}):
            with self.assertRaises(Invalid):
                semantic_key({"version": 2, "rules": [rule]})

    def test_duplicate_yaml_and_empty_data(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "invalid.yaml"
            path.write_text("status: pending\nstatus: approved\n")
            with self.assertRaises(Invalid):
                load(path)

    def test_dlc_attributes_and_unsupported_syntax(self):
        parsed = parse_dlc("example.com\nfull:exact.example.com @ads\nregexp:^a\\.example\\.com$\n")
        self.assertEqual(parsed[0]["type"], "domain_suffix")
        self.assertEqual(parsed[1]["attributes"], ["@ads"])
        for text in ("", "include:google @cn", "&google", "bad:example.com", "example.com mystery"):
            with self.assertRaises(Invalid):
                parse_dlc(text)

    def test_discovery_retains_historical_dependencies(self):
        result = report()
        found = {r["value"]: r["classification"] for r in result["discovery"] if r["upstream"] == "legacy-anthropic"}
        self.assertEqual(found["cdn.growthbook.io"], "ADD_CANDIDATE")
        self.assertEqual(found["cdn.usefathom.com"], "ADD_CANDIDATE")
        self.assertEqual(found["challenges.cloudflare.com"], "ALREADY_COVERED")


if __name__ == "__main__":
    unittest.main()
