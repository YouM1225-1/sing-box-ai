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
from common import ROOT, Invalid, archives, canonical, covered, date, discovery_entries, load, normalize, public_suffix, review_entry, run, semantic_key, sha, source_document, write_json
from sync import parse_dlc, report
from validate import cases_for, release_gate


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "sources", self.root / "sources")
        shutil.copyfile(ROOT / "tools.lock.json", self.root / "tools.lock.json")
        (self.root / ".tools").mkdir()
        (self.root / ".tools/sing-box").symlink_to(ROOT / ".tools/sing-box")

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

    def change_policy(self, **changes):
        path = self.root / "sources/policy.yaml"
        policy = load(path)
        policy.update(changes)
        path.write_text(yaml.safe_dump(policy, allow_unicode=True, sort_keys=False))

    def rehash(self, ident):
        path = self.root / "sources/upstreams.yaml"
        registry = load(path)
        item = next(r for r in registry["archives"] if r["id"] == ident)
        item["sha256"] = sha(self.root / item["path"])
        path.write_text(yaml.safe_dump(registry, allow_unicode=True, sort_keys=False))

    def test_complete_baseline_and_attributes_survive_optional_off(self):
        selected, policy, _ = canonical(self.root)
        registry = archives(self.root)
        for name in ("openai", "anthropic"):
            original = self.root / (name + "-upstream.json")
            run([self.root / ".tools/sing-box", "rule-set", "decompile", "--output", original, self.root / registry["geosite-" + name]["path"]])
            decoded = load(original)
            decoded["version"] = 2
            rows = [r for r in selected[name] if r["origin"] == "baseline"]
            # Full native representation, not a finite sample of domains.
            self.assertEqual(semantic_key(decoded), semantic_key(source_document(rows)))
            self.assertTrue(all(covered(r, selected[name]) for r in rows))
            self.assertEqual(policy["baseline_inputs"][name]["sha256"], registry["geosite-" + name]["sha256"])
        openai = selected["openai"]
        ads = [r for r in openai if r["origin"] == "baseline" and any("@ads" in p["attributes"] for p in r["dlc_provenance"])]
        self.assertTrue(ads)
        self.assertTrue(all(covered(r, openai) for r in ads))
        self.assertTrue(covered({"type": "domain", "value": "chat.com"}, openai))
        self.assertTrue(covered({"type": "domain", "value": "oaistatic.com"}, openai))
        self.assertEqual(source_document(openai)["version"], 2)
        self.assertEqual(len(source_document(openai)["rules"]), 1)

    def test_changed_srs_is_read_even_when_hash_is_updated(self):
        registry = archives(self.root)
        target = self.root / registry["geosite-openai"]["path"]
        source = self.root / "replacement.json"
        write_json(source, {"version": 2, "rules": [{"domain": ["different.example.org"]}]})
        run([self.root / ".tools/sing-box", "rule-set", "compile", "--output", target, source])
        self.rehash("geosite-openai")
        with self.assertRaisesRegex(Invalid, "DLC and SRS baseline disagree"):
            canonical(self.root)

    def test_changed_dlc_cannot_replace_production_baseline(self):
        registry = archives(self.root)
        path = self.root / registry["dlc-openai"]["path"]
        path.write_text(path.read_text() + "\nfull:different.example.org\n")
        self.rehash("dlc-openai")
        with self.assertRaisesRegex(Invalid, "DLC and SRS baseline disagree"):
            canonical(self.root)

    def test_unreviewed_baseline_structure_and_direction_fail_closed(self):
        registry = archives(self.root)
        target = self.root / registry["geosite-openai"]["path"]
        for rules in ([{"source_ip_cidr": ["192.0.2.0/24"]}], [{"domain": ["one.example.org"]}, {"domain": ["two.example.org"]}], [{"domain_keyword": ["openai"]}]):
            with self.subTest(rules=rules):
                source = self.root / "replacement.json"
                write_json(source, {"version": 2, "rules": rules})
                run([self.root / ".tools/sing-box", "rule-set", "compile", "--output", target, source])
                self.rehash("geosite-openai")
                with self.assertRaises(Invalid):
                    canonical(self.root)

    def test_unselected_pending_does_not_block_release_but_selected_does(self):
        pending = discovery_entries(self.root)
        self.assertTrue(pending)
        candidate = next(r for r in pending if r["value"] == "cdn.growthbook.io")
        selected, _, _ = canonical(self.root, "release", dt.date(2026, 9, 27))
        self.assertFalse(covered(candidate, selected[candidate["artifact"]]))
        self.change_policy(selected_pending=[candidate["id"]])
        selected, _, _ = canonical(self.root, "candidate", dt.date(2026, 9, 27))
        self.assertTrue(covered(candidate, selected[candidate["artifact"]]))
        with self.assertRaisesRegex(Invalid, "Selected pending candidates"):
            canonical(self.root, "release", dt.date(2026, 9, 27))
        self.change_policy(selected_pending=["anthropic:domain:unregistered.example.org"])
        with self.assertRaisesRegex(Invalid, "Invalid pending selection"):
            canonical(self.root)

    def test_pending_cannot_evade_release_gate_by_claiming_official_status(self):
        row = copy.deepcopy(next(r for r in load(self.root / "sources/openai.yaml") if r["value"] == "cdn.workos.com"))
        row.update(id="openai:domain:cdn.workos.com", artifact="openai", review_status="pending", evidence=[], first_seen="2026-09-27", last_verified=None, review_after=None)
        path = self.root / "sources/discovery/pending.yaml"
        pending = load(path)
        pending["entries"].append(row)
        path.write_text(yaml.safe_dump(pending, allow_unicode=True, sort_keys=False))
        self.change_policy(selected_pending=[row["id"]])
        with self.assertRaisesRegex(Invalid, "Selected pending candidates"):
            canonical(self.root, "release", dt.date(2026, 9, 27))

    def test_redating_original_user_confirmation_cannot_renew_it(self):
        row = next(r for r in load(self.root / "sources/anthropic.yaml") if r["value"] == "challenges.cloudflare.com")
        evidence = next(e for e in row["evidence"] if e["kind"] == "user-confirmation")
        path = self.root / evidence["reference"]
        proof = load(path)
        proof.update(observed_on="2026-10-01", verified_on="2026-10-01")
        write_json(path, proof)
        evidence["observed_on"] = "2026-10-01"
        row.update(last_verified="2026-10-01", review_after="2026-10-31")
        with self.assertRaisesRegex(Invalid, "pinned initial approval"):
            review_entry(row, "release", dt.date(2026, 10, 1), self.root)

    def test_real_new_runtime_record_can_renew_compatibility(self):
        row = next(r for r in load(self.root / "sources/anthropic.yaml") if r["value"] == "challenges.cloudflare.com")
        reference = "sources/evidence/test-new-runtime.json"
        proof = {"schema": 1, "kind": "runtime-validation", "result": "passed", "conclusion": "Synthetic test fixture only", "rule": {"type": row["type"], "value": row["value"]}, "products": row["product"], "observed_on": "2026-10-01", "verified_on": "2026-10-01", "environment": "unit-test fixture", "client_version": "fixture-1", "method": "fixture, not actual integration"}
        write_json(self.root / reference, proof)
        row["evidence"].append({"kind": "runtime-validation", "reference": reference, "observed_on": "2026-10-01", "conclusion": "Synthetic test fixture only", "product": row["product"]})
        row.update(last_verified="2026-10-01", review_after="2026-10-31")
        review_entry(row, "release", dt.date(2026, 10, 1), self.root)
        for mutation in ({"client_version": None}, {"verified_on": "2026-09-27"}, {"kind": "user-confirmation"}):
            with self.subTest(mutation=mutation):
                write_json(self.root / reference, {**proof, **mutation})
                with self.assertRaises(Invalid):
                    review_entry(row, "release", dt.date(2026, 10, 1), self.root)
        write_json(self.root / reference, proof)
        row["evidence"][-1]["product"] = row["product"][:1]
        with self.assertRaisesRegex(Invalid, "product-specific"):
            review_entry(row, "release", dt.date(2026, 10, 1), self.root)

    def test_missing_official_fact_is_not_silently_omitted(self):
        self.change("openai", lambda rows: rows.remove(next(r for r in rows if r["value"] == "cdn.workos.com")))
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

    def test_archived_source_provenance_cannot_be_repointed(self):
        registry = archives(self.root)
        official = self.root / registry["openai-network"]["path"]
        document = load(official)
        for replacement in ("voice-raw", "claude-code-source"):
            with self.subTest(replacement=replacement):
                other = registry[replacement]
                document.update(raw_reference=replacement, raw_sha256=other["sha256"], original_response_sha256=other.get("original_response_sha256"))
                write_json(official, document)
                self.rehash("openai-network")
                with self.assertRaisesRegex(Invalid, "archived source record"):
                    canonical(self.root)

    def test_raw_metadata_and_original_response_hash_are_verified(self):
        registry = archives(self.root)
        metadata = self.root / registry["voice-raw"]["metadata_path"]
        saved = metadata.read_bytes()
        metadata.write_bytes(saved + b" ")
        with self.assertRaisesRegex(Invalid, "metadata hash mismatch"):
            canonical(self.root)
        metadata.write_bytes(saved)
        source = self.root / registry["openai-network-source"]["path"]
        record = load(source)
        record["original_response"]["sha256"] = "0" * 64
        write_json(source, record)
        self.rehash("openai-network-source")
        official = self.root / registry["openai-network"]["path"]
        document = load(official)
        document["raw_sha256"] = sha(source)
        write_json(official, document)
        self.rehash("openai-network")
        with self.assertRaisesRegex(Invalid, "Original response provenance mismatch"):
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

    def test_legacy_runtime_review_does_not_authorize_publication(self):
        write_json(self.root / "sources/release-review.json", {"schema": 1, "status": "approved", "integration_evidence": [{"result": "passed"}]})
        with patch("validate.today", return_value=dt.date(2026, 9, 27)):
            with self.assertRaisesRegex(Invalid, "wrong scope"):
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

    def test_union_keeps_regex_opaque_and_suffix_apex_distinct(self):
        rows = [{"type": "domain_suffix", "value": ".example.com"}, {"type": "domain", "value": "example.com"}, {"type": "domain", "value": "a.example.com"}, {"type": "domain_regex", "value": r"^regex\.example\.net$"}, {"type": "domain", "value": "regex.example.net"}]
        rule = source_document(rows)["rules"][0]
        self.assertEqual(rule["domain"], ["example.com", "regex.example.net"])
        self.assertEqual(rule["domain_suffix"], [".example.com"])
        self.assertEqual(rule["domain_regex"], [r"^regex\.example\.net$"])
        self.assertFalse(covered({"type": "domain", "value": "regex.example.net"}, [rows[-2]]))

    def test_sync_reports_baseline_and_supplement_diffs_separately(self):
        with tempfile.TemporaryDirectory() as temp:
            previous = Path(temp) / "previous.json"
            before = report()
            removed = before["baseline_rules"]["openai"].pop()
            before["supplements"]["openai"][0]["reason"] = "old reason"
            write_json(previous, before)
            after = report(previous=previous)
            self.assertIn(removed, after["baseline_diff"]["openai"]["added"])
            self.assertEqual(len(after["supplement_diff"]["openai"]["changed"]), 1)
            self.assertTrue(any(r.get("review_status") == "pending" and r["selected"] is False for r in after["discovery"]))

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
