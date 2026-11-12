"""Full user-requested expression coverage preserves earlier rules and directions."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import ROOT, canonical, covered, load, source_document
from validate import cases_for, reference_match

EXPECTED = {("domain_keyword", value) for value in ("anthropic", "claude", "browser-intake")}
EXPECTED |= {("domain_suffix", value) for value in ("stripe.com", "usefathom.com", "challenges.cloudflare.com")}


class SixScopeCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.selected = canonical(ROOT, "candidate")[0]

    def test_only_six_authorized_additions_preserve_original_evidence(self):
        before = load(ROOT / "tests/fixtures/anthropic-v0.1.12.yaml")
        after = load(ROOT / "sources/anthropic.yaml")
        self.assertEqual(after[:len(before)], before)
        additions = after[len(before):]
        self.assertEqual(len(additions), 6)
        self.assertEqual({(r["type"], r["value"]) for r in additions}, EXPECTED)
        for row in additions:
            self.assertEqual(row["status"], "user-requested")
            self.assertEqual(row["direction"], "destination")
            self.assertTrue(row["shared_dependency"])
            self.assertEqual(row["sources"], [{"kind": "user-instruction", "reference": "claude-six-scopes-coverage-request"}])

    def test_prior_coverage_and_other_artifacts_survive_normalization(self):
        old = load(ROOT / "artifacts/v0.1.12/anthropic.json")["rules"][0]
        current = self.selected["anthropic"]
        for kind, values in old.items():
            for value in values:
                self.assertTrue(covered({"type": kind, "value": value}, current), (kind, value))
        for name in ("openai", "anthropic-ip"):
            self.assertEqual(source_document(self.selected[name]), load(ROOT / f"artifacts/v0.1.12/{name}.json"))
        self.assertEqual(source_document(current)["rules"][0]["ip_cidr"], old["ip_cidr"])

    def test_keyword_width_suffix_boundaries_and_unrelated_scopes(self):
        positive = ["anthropic-probe.invalid", "notclaude.ai", "claude-fan.example.org", "browser-intake.other.invalid",
                    "stripe.com", "hooks.stripe.com", "a.js.stripe.com", "usefathom.com", "a.b.usefathom.com",
                    "challenges.cloudflare.com", "a.b.challenges.cloudflare.com"]
        negative = ["anthro-pic.invalid", "clau-de.invalid", "browser_intake.other.invalid", "notstripe.com",
                    "stripe.com.invalid", "notusefathom.com", "usefathom.com.invalid", "notchallenges.cloudflare.com",
                    "challenges.cloudflare.com.invalid", "cloudflare.com", "google.com", "modelcontextprotocol.io", "webshare.io", "pool.ntp.org"]
        for host in positive:
            self.assertTrue(reference_match(self.selected["anthropic"], domain=host), host)
        for host in negative:
            self.assertFalse(reference_match(self.selected["anthropic"], domain=host), host)

    def test_fixed_witnesses_distinguish_old_and_expanded_scopes(self):
        legacy = {name: [r for r in rows if not any(s.get("reference") == "claude-six-scopes-coverage-request" for s in r.get("sources", []))]
                  for name, rows in self.selected.items()}
        old = {c["Name"]: c["Want"] for c in cases_for(legacy)}
        new = {c["Name"]: c["Want"] for c in cases_for(self.selected)}
        for name in ("anthropic:website-boundary:notclaude.ai", "anthropic:website-boundary:anthropic.com.invalid",
                     "anthropic:website-negative:probe.cdn.usefathom.com"):
            self.assertFalse(old[name], name)
            self.assertTrue(new[name], name)
        for name in ("anthropic:website-boundary:notintercom.io", "anthropic:website-negative:cdn.usefathom.com.invalid"):
            self.assertFalse(old[name], name)
            self.assertFalse(new[name], name)


if __name__ == "__main__":
    unittest.main()
