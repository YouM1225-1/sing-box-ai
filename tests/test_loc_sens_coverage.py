"""The requested Stripe and RevenueCat hosts retain exact destination scope."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import ROOT, canonical, load, semantic_key, source_document
from validate import reference_match


HOSTS = ("js.stripe.com", "api.stripe.com", "checkout.stripe.com",
         "billing.stripe.com", "m.stripe.com", "api.revenuecat.com")


class LocSensCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.selected = canonical(ROOT, "candidate")[0]

    def test_only_six_requested_hosts_are_added_to_previous_release(self):
        for artifact, rows in self.selected.items():
            expected = copy.deepcopy(load(ROOT / "artifacts/v0.1.10" / (artifact + ".json")))
            if artifact == "anthropic":
                expected["rules"][0]["domain"] += list(HOSTS)
            self.assertEqual(semantic_key(source_document(rows)), semantic_key(expected), artifact)
        additions = [r for r in self.selected["anthropic"] if r["value"] in HOSTS]
        self.assertEqual(len(additions), len(HOSTS))
        for row in additions:
            self.assertEqual((row["type"], row["direction"], row["status"]),
                             ("domain", "destination", "user-requested"))
            self.assertTrue(row["shared_dependency"])

    def test_exact_hosts_without_parent_subdomain_or_keyword_expansion(self):
        for host in HOSTS:
            for artifact, rows in self.selected.items():
                expected = artifact == "anthropic" or (artifact == "openai" and host == "js.stripe.com")
                self.assertEqual(reference_match(rows, domain=host), expected, (artifact, host))
                for near in ("a." + host, "b.a." + host, "not" + host, host + ".invalid"):
                    self.assertFalse(reference_match(rows, domain=near), (artifact, near))
        for parent in ("stripe.com", "other.stripe.com", "revenuecat.com", "other.revenuecat.com"):
            for artifact, rows in self.selected.items():
                self.assertFalse(reference_match(rows, domain=parent), (artifact, parent))


if __name__ == "__main__":
    unittest.main()
