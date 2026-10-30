"""Current Persona coverage preserves the previous release and domain boundaries."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import ROOT, canonical, load, semantic_key, source_document
from validate import reference_match


class PersonaCoverageTests(unittest.TestCase):
    def test_only_persona_suffix_is_added_and_scope_is_documented(self):
        selected, policy, _ = canonical(ROOT, "candidate")
        for artifact, rows in selected.items():
            expected = copy.deepcopy(load(ROOT / "artifacts/v0.1.8" / (artifact + ".json")))
            if artifact == "anthropic":
                expected["rules"][0]["domain_suffix"].append("withpersona.com")
            self.assertEqual(semantic_key(source_document(rows)), semantic_key(expected), artifact)
        row = next(r for r in selected["anthropic"] if r["value"] == "withpersona.com")
        self.assertEqual(row["status"], "feature-required")
        self.assertTrue(row["shared_dependency"])
        self.assertIn("claude-identity-verification", policy["features"])
        for host in ("withpersona.com", "inquiry.withpersona.com", "cdn.withpersona.com", "sdk.withpersona.com", "files.withpersona.com", "a.b.withpersona.com"):
            self.assertTrue(reference_match(selected["anthropic"], domain=host), host)
            self.assertFalse(reference_match(selected["openai"], domain=host), host)
        for host in ("notwithpersona.com", "withpersona.com.invalid", "with-persona.com"):
            self.assertFalse(reference_match(selected["anthropic"], domain=host), host)


if __name__ == "__main__":
    unittest.main()
