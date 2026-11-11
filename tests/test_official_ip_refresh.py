"""Official November IP snapshots retain exact coverage and traffic direction."""
import copy
import ipaddress
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import ROOT, canonical, load, semantic_key, source_document
from validate import reference_match


class OfficialIPRefreshTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.selected = canonical(ROOT, "candidate")[0]

    def test_all_423_official_voice_hosts_and_only_the_official_delta(self):
        raw = load(ROOT / "sources/official/chatgpt-voice.json")
        addresses = [row["ipv4Prefix"] for row in raw["prefixes"]]
        self.assertEqual(len(addresses), 423)
        self.assertEqual(len(set(addresses)), 423)
        self.assertTrue(all(ipaddress.ip_network(value).prefixlen == 32 for value in addresses))
        for artifact, rows in self.selected.items():
            expected = copy.deepcopy(load(ROOT / "artifacts/v0.1.11" / (artifact + ".json")))
            rule = expected["rules"][0]
            if artifact == "openai":
                self.assertEqual(len(set(addresses) - set(rule["ip_cidr"])), 400)
                self.assertTrue(set(rule["ip_cidr"]) <= set(addresses))
                rule["ip_cidr"] = sorted(addresses)
            elif artifact == "anthropic":
                rule["ip_cidr"].append("153.61.224.0/22")
            else:
                rule["source_ip_cidr"].append("153.61.208.0/20")
            self.assertEqual(semantic_key(source_document(rows)), semantic_key(expected), artifact)
        for value in addresses:
            host = str(ipaddress.ip_network(value).network_address)
            self.assertTrue(reference_match(self.selected["openai"], destination=host), host)
            self.assertFalse(reference_match(self.selected["openai"], source=host), host)

    def test_new_anthropic_boundaries_and_directions(self):
        witnesses = {
            "153.61.207.255": (False, False),
            "153.61.208.0": (False, True),
            "153.61.223.255": (False, True),
            "153.61.224.0": (True, False),
            "153.61.227.255": (True, False),
            "153.61.228.0": (False, False),
        }
        for host, (destination, source) in witnesses.items():
            self.assertEqual(reference_match(self.selected["anthropic"], destination=host), destination, host)
            self.assertEqual(reference_match(self.selected["anthropic-ip"], source=host), source, host)
            self.assertFalse(reference_match(self.selected["anthropic"], source=host), host)
            self.assertFalse(reference_match(self.selected["anthropic-ip"], destination=host), host)
            self.assertFalse(reference_match(self.selected["openai"], destination=host), host)


if __name__ == "__main__":
    unittest.main()
