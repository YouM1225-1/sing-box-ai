"""Website coverage is explicit, complete, and distinct from service validation."""
import copy
import datetime as dt
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import ROOT, Invalid, canonical, covered, load, normalize, semantic_key, sha, source_document, write_json
from validate import cases_for, reference_match


WEBSITE_SUFFIXES = (
    "anthropic.com", "claude.ai", "claude.com", "clau.de",
    "claudemcpclient.com", "claudemcpcontent.com", "claudeusercontent.com",
    "servd-anthropic-website.b-cdn.net", "anthropic.com.cdn.cloudflare.net",
    "anthropic.auth0.com", "anthropic-com.ghost.io", "sentry.io",
    "statsigapi.net", "intercom.io", "intercomcdn.com",
)


class RequestedCoverageTests(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        shutil.copytree(ROOT / "sources", self.root / "sources")
        shutil.copyfile(ROOT / "tools.lock.json", self.root / "tools.lock.json")
        (self.root / ".tools").mkdir()
        (self.root / ".tools/sing-box").symlink_to(ROOT / ".tools/sing-box")
        self.reference = "sources/evidence/net-coffee-coverage-request-2026-10-15.json"

    def save(self, path, document):
        (self.root / path).write_text(yaml.safe_dump(document, allow_unicode=True, sort_keys=False))

    def validate(self):
        return canonical(self.root, "release", dt.date(2026, 10, 21))[0]

    def test_complete_website_union_and_previous_release_are_preserved(self):
        selected = self.validate()
        expected = {
            "domain_suffix": WEBSITE_SUFFIXES,
            "domain": ("browser-intake-us5-datadoghq.com", "cdn.usefathom.com"),
            "domain_keyword": ("datadog", "sentry", "sift"),
            "ip_cidr": ("160.79.104.0/21", "2607:6bc0::/32"),
        }
        for typ, values in expected.items():
            for value in values:
                with self.subTest(typ=typ, value=value):
                    self.assertTrue(covered({"type": typ, "value": value}, selected["anthropic"]))
        for artifact, rows in selected.items():
            previous = load(ROOT / "artifacts/v0.1.4" / (artifact + ".json"))
            for typ, values in previous["rules"][0].items():
                for value in values:
                    self.assertTrue(covered({"type": typ, "value": value}, rows), (artifact, typ, value))
            if artifact != "anthropic":
                if artifact == "openai":
                    previous["rules"][0]["domain"] = sorted(set(previous["rules"][0]["domain"]) | {"frontend-apps-multi-region.workos.com"})
                self.assertEqual(semantic_key(source_document(rows)), semantic_key(previous))
        rule = source_document(selected["anthropic"])["rules"][0]
        self.assertEqual(set(rule["ip_cidr"]), {"160.79.104.0/21", "2607:6bc0::/32"})
        self.assertEqual(set(rule["domain_keyword"]), {"datadog", "sentry", "sift"})

    def test_one_exit_adds_only_five_suffixes_to_published_016(self):
        suffixes = {"growthbook.io", "hcaptcha.com", "stripe.network", "stripecdn.com", "segment.io"}
        selected = self.validate()
        for artifact, rows in selected.items():
            previous = load(ROOT / "artifacts/v0.1.6" / (artifact + ".json"))
            for typ, values in previous["rules"][0].items():
                for value in values:
                    self.assertTrue(covered({"type": typ, "value": value}, rows), (artifact, typ, value))
            expected = copy.deepcopy(previous)
            if artifact == "anthropic":
                expected["rules"][0]["domain_suffix"] = sorted(set(expected["rules"][0]["domain_suffix"]) | suffixes)
            self.assertEqual(semantic_key(source_document(rows)), semantic_key(expected), artifact)
        for suffix in sorted(suffixes):
            for host in (suffix, "probe." + suffix, "nested.probe." + suffix):
                with self.subTest(host=host):
                    self.assertTrue(reference_match(selected["anthropic"], domain=host))
            for host in ("not" + suffix, suffix + ".invalid"):
                with self.subTest(host=host):
                    self.assertFalse(reference_match(selected["anthropic"], domain=host))

    def test_fixed_native_witnesses_cover_boundaries_directions_keywords_and_ntp(self):
        selected = self.validate()
        cases = [case for case in cases_for(selected) if case["Name"].startswith(("anthropic:website-", "anthropic:excluded-ntp:"))]
        self.assertGreater(len(cases), 100)
        for case in cases:
            with self.subTest(case=case["Name"]):
                self.assertEqual(reference_match(selected["anthropic"], case["Domain"] or case["FQDN"], case["Source"], case["Destination"]), case["Want"])
        baseline = {"baseline-anthropic": [r for r in selected["anthropic"] if r["origin"] == "baseline"]}
        for case in cases_for(baseline):
            if "adjacent-ipv6:" in case["Name"]:
                self.assertFalse(case["Want"])

    def test_instruction_hash_cannot_be_skipped(self):
        path = self.root / self.reference
        proof = load(path)
        proof["statement"] += " changed"
        write_json(path, proof)
        with self.assertRaisesRegex(Invalid, "hash mismatch"):
            self.validate()

    def test_rehashed_instruction_still_binds_scope_and_exclusions(self):
        original = load(self.root / self.reference)
        for changes in ({"kind": "runtime-validation"}, {"scope": "consumer-integration"}, {"artifact": "openai"}, {"direction": "source"}, {"products": ["claude-code"]}, {"excluded": []}, {"service_usage_verified": True}, {"consumer_validation": True}, {"approved_on": "2026-10-22"}, {"rules": []}, {"website_url": "https://example.invalid/"}):
            with self.subTest(changes=changes):
                path = self.root / self.reference
                write_json(path, {**original, **changes})
                registry = load(self.root / "sources/upstreams.yaml")
                next(r for r in registry["archives"] if r["id"] == "net-coffee-coverage-request")["sha256"] = sha(path)
                self.save("sources/upstreams.yaml", registry)
                with self.assertRaises(Invalid):
                    self.validate()

    def test_requested_rows_cannot_expand_beyond_instruction_or_claim_review(self):
        original = load(self.root / "sources/anthropic.yaml")
        for changes in ({"value": "unrequested.example.org"}, {"product": ["claude-code"]}, {"direction": "source"}, {"shared_dependency": False}, {"review_status": "approved"}, {"features": ["claude-support"]}, {"sources": [{"kind": "official", "reference": "claude-code"}]}):
            with self.subTest(changes=changes):
                rows = copy.deepcopy(original)
                row = next(r for r in rows if r["status"] == "user-requested" and r["type"] == "domain_suffix")
                row.update(changes)
                self.save("sources/anthropic.yaml", rows)
                with self.assertRaises(Invalid):
                    self.validate()

    def test_keyword_cannot_borrow_official_or_compatibility_status(self):
        original = load(self.root / "sources/anthropic.yaml")
        for status in ("required", "optional", "compatibility"):
            with self.subTest(status=status):
                rows = copy.deepcopy(original)
                next(r for r in rows if r["type"] == "domain_keyword")["status"] = status
                self.save("sources/anthropic.yaml", rows)
                with self.assertRaisesRegex(Invalid, "explicit user instruction"):
                    self.validate()


class KeywordSemanticsTests(unittest.TestCase):
    def test_literal_normalization_and_matching(self):
        self.assertEqual(normalize("domain_keyword", "DataDog"), "datadog")
        for value in ("", " datadog", "datadog ", "data.dog", "*", "数据", "sentry|sift"):
            with self.subTest(value=value), self.assertRaises(Invalid):
                normalize("domain_keyword", value)
        rows = [{"type": "domain_keyword", "value": "datadog"}]
        for typ, value in (("domain", "prefixdatadogsuffix.example"), ("domain_suffix", "datadog.example"), ("domain_keyword", "datadoghq")):
            self.assertTrue(covered({"type": typ, "value": value}, rows))
        for typ, value in (("domain", "datado.example"), ("domain_keyword", "data"), ("domain_suffix", "example.org"), ("ip_cidr", "192.0.2.0/24")):
            self.assertFalse(covered({"type": typ, "value": value}, rows))
        self.assertTrue(reference_match(rows, domain="BEFOREDATADOGAFTER.EXAMPLE"))
        self.assertFalse(reference_match(rows, source="192.0.2.1", destination="198.51.100.1"))

    def test_keyword_subsumption_and_semantic_field_are_retained(self):
        rows = [{"type": "domain_keyword", "value": "datadog"}, {"type": "domain_keyword", "value": "datadoghq"}, {"type": "domain", "value": "browser-intake-us5-datadoghq.com"}, {"type": "domain_suffix", "value": "datadoghq.com"}]
        document = source_document(rows)
        self.assertEqual(document["rules"], [{"domain_keyword": ["datadog"]}])
        self.assertEqual(semantic_key(document)["domain_keyword"], ["datadog"])
        self.assertNotEqual(semantic_key(document), semantic_key({"version": 2, "rules": [{"domain_suffix": ["datadog.com"]}]}))


if __name__ == "__main__":
    unittest.main()
