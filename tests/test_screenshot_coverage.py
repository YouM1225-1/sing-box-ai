"""The screenshot supplement adds only the two hosts and destination /16."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import ROOT, canonical, load, semantic_key, source_document
from validate import reference_match


class ScreenshotCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.selected = canonical(ROOT, "candidate")[0]

    def test_only_three_requested_destination_scopes_are_added(self):
        for artifact, rows in self.selected.items():
            expected = copy.deepcopy(load(ROOT / "artifacts/v0.1.9" / (artifact + ".json")))
            if artifact == "anthropic":
                expected["rules"][0]["domain"] += ["r.stripe.com", "fcmtoken.googleapis.com"]
                expected["rules"][0]["ip_cidr"].append("34.8.0.0/16")
            self.assertEqual(semantic_key(source_document(rows)), semantic_key(expected), artifact)
        additions = [r for r in self.selected["anthropic"] if r["value"] in {"r.stripe.com", "fcmtoken.googleapis.com", "34.8.0.0/16"}]
        self.assertEqual(len(additions), 3)
        for row in additions:
            self.assertEqual(row["status"], "user-requested")
            self.assertEqual(row["direction"], "destination")
            self.assertTrue(row["shared_dependency"])

    def test_domain_matches_are_exact(self):
        for host in ("r.stripe.com", "fcmtoken.googleapis.com"):
            for artifact, rows in self.selected.items():
                self.assertEqual(reference_match(rows, domain=host), artifact == "anthropic")
                for near in ("a." + host, "not" + host, host + ".invalid"):
                    self.assertFalse(reference_match(rows, domain=near), (artifact, near))
        for host in ("stripe.com", "googleapis.com", "other.stripe.com", "other.googleapis.com"):
            self.assertFalse(reference_match(self.selected["anthropic"], domain=host), host)

    def test_network_boundaries_and_source_direction(self):
        for artifact, rows in self.selected.items():
            for ip in ("34.8.0.0", "34.8.0.1", "34.8.128.1", "34.8.255.255"):
                self.assertEqual(reference_match(rows, destination=ip), artifact == "anthropic", (artifact, ip))
                self.assertFalse(reference_match(rows, source=ip), (artifact, ip))
            for ip in ("34.7.255.255", "34.9.0.0"):
                self.assertFalse(reference_match(rows, destination=ip), (artifact, ip))
                self.assertFalse(reference_match(rows, source=ip), (artifact, ip))


if __name__ == "__main__":
    unittest.main()
