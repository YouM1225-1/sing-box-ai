"""UniFi 派生输出的方向、语义损失和同步边界。"""
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import ROOT, Invalid, load, sha, write_json
from export_unifi import check_current, check_exports, render, write_exports


class UniFiExports(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.batch = Path(self.temp.name) / "batch"
        version = (ROOT / "VERSION").read_text().strip()
        shutil.copytree(ROOT / "artifacts" / ("v" + version), self.batch)
        self.manifest = load(self.batch / "manifest.json")

    def change_rule(self, mutate):
        path = self.batch / "anthropic.json"
        doc = load(path)
        mutate(doc["rules"][0])
        write_json(path, doc)
        next(a for a in self.manifest["artifacts"] if a["path"] == "anthropic.srs")["source_sha256"] = sha(path)

    def test_current_exports_follow_source_release(self):
        check_current()

    def test_source_only_ranges_excluded_and_broad_destinations_preserved(self):
        data = render(self.batch, self.manifest)
        v4 = data["ipv4.txt"].decode().splitlines()
        self.assertNotIn("153.61.208.0/20", v4)
        self.assertIn("153.61.224.0/22", v4)
        self.assertIn("160.79.104.0/21", v4)
        self.assertIn("34.8.0.0/16", v4)
        self.assertEqual(data["ipv6.txt"], b"2607:6bc0::/32\n")
        self.assertFalse(any(x.endswith("/32") for x in v4))

    def test_omissions_and_leading_dot_are_explicit(self):
        data = render(self.batch, self.manifest)
        meta = json.loads(data["manifest.json"])
        self.assertEqual(len(meta["omitted"]), 7)
        self.assertEqual(
            {x["value"] for x in meta["omitted"] if x["type"] == "domain_keyword"},
            {"anthropic", "browser-intake", "claude", "datadog", "sentry", "sift"},
        )
        self.assertTrue(any(x["value"] == ".ct.sendgrid.net" and x["output"] == "ct.sendgrid.net" for x in meta["domain_mappings"]))
        self.assertNotIn(b"*", data["domains.txt"])

    def test_unknown_source_fields_and_directions_fail_closed(self):
        self.change_rule(lambda r: r.update(source_ip_cidr=["153.61.208.0/20"]))
        with self.assertRaisesRegex(Invalid, "Unknown/source-only"):
            render(self.batch, self.manifest)
        other = copy.deepcopy(self.manifest)
        next(a for a in other["artifacts"] if a["path"] == "openai.srs")["direction"] = "source"
        with self.assertRaisesRegex(Invalid, "destination"):
            render(self.batch, other)

    def test_non_domain_and_empty_labels_are_rejected(self):
        for bad in ("https://example.com", "*.example.com", "a..example.com", "-a.example.com", "example.com."):
            self.change_rule(lambda r: r.update(domain=[bad]))
            with self.assertRaisesRegex(Invalid, "Invalid UniFi"):
                render(self.batch, self.manifest)

    def test_tampered_or_stale_exports_and_metadata_are_rejected(self):
        out = Path(self.temp.name) / "unifi"
        write_exports(self.batch, self.manifest, out)
        check_exports(self.batch, self.manifest, out)
        for name in ("domains.txt", "ipv4.txt", "ipv6.txt", "manifest.json"):
            original = (out / name).read_bytes()
            (out / name).write_bytes(original + b"\n")
            with self.assertRaisesRegex(Invalid, "Stale/tampered"):
                check_exports(self.batch, self.manifest, out)
            (out / name).write_bytes(original)

    def test_source_bytes_and_duplicate_artifact_records_checked(self):
        (self.batch / "openai.srs").write_bytes(b"tampered")
        with self.assertRaisesRegex(Invalid, "source hash"):
            render(self.batch, self.manifest)
        self.manifest["artifacts"].append(copy.deepcopy(self.manifest["artifacts"][0]))
        with self.assertRaisesRegex(Invalid, "duplicate"):
            render(self.batch, self.manifest)

    def test_existing_export_directory_not_overwritten(self):
        out = Path(self.temp.name) / "unifi"
        write_exports(self.batch, self.manifest, out)
        with self.assertRaisesRegex(Invalid, "exists"):
            write_exports(self.batch, self.manifest, out)


if __name__ == "__main__":
    unittest.main()
