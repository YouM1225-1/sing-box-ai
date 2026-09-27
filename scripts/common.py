"""Shared, offline input checks. Network access belongs to bootstrap/sync only."""
from __future__ import annotations

import datetime as dt
import hashlib
import ipaddress
import json
from pathlib import Path
import re
import subprocess
import tempfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ("openai", "anthropic", "anthropic-ip")
TYPES = {"domain", "domain_suffix", "domain_regex", "ip_cidr", "source_ip_cidr"}
STATUSES = {"required", "feature-required", "optional", "compatibility", "compatibility-critical"}
COMMON_FIELDS = {"value", "type", "product", "direction", "status", "shared_dependency", "sources", "reason", "features"}
REVIEW_FIELDS = {"review_status", "evidence", "first_seen", "last_verified", "review_after"}
FORBIDDEN = {"amazonaws.com", "api.aws", "cloudflare.com", "cloudflare.net", "azure.com", "azureedge.net", "windows.net", "googleapis.com", "githubusercontent.com", "blob.core.windows.net", "webpubsub.azure.com", "googlesource.com", "imgix.net", "livekit.cloud", "b-cdn.net"}
OLD_IPS = ("34.162.46.92", "34.162.102.82", "34.162.136.91", "34.162.142.92", "34.162.183.95")


class Invalid(ValueError):
    pass


def need(condition, message):
    if not condition:
        raise Invalid(message)


class UniqueLoader(yaml.SafeLoader):
    def construct_mapping(self, node, deep=False):
        keys = [self.construct_object(k, deep=deep) for k, _ in node.value]
        need(all(isinstance(k, str) for k in keys), "YAML keys must be strings")
        need(len(set(keys)) == len(keys), "Duplicate YAML key")
        return super().construct_mapping(node, deep)


def load(path):
    path = Path(path)
    need(path.is_file() and path.stat().st_size <= 2_000_000, f"Missing/oversize input: {path}")
    with path.open(encoding="utf-8") as f:
        return yaml.load(f, Loader=UniqueLoader)


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def local_path(root, value):
    need(isinstance(value, str) and value and not Path(value).is_absolute(), "Expected a repository-relative path")
    path = (root / value).resolve()
    need(path.is_relative_to(root.resolve()), f"Path escapes repository: {value}")
    need(not (root / value).is_symlink(), f"Symlink input is not allowed: {value}")
    return path


def date(value):
    need(isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value), "Dates must be quoted YYYY-MM-DD strings")
    try:
        return dt.date.fromisoformat(value)
    except ValueError as e:
        raise Invalid(str(e)) from e


def today():
    return dt.datetime.now(dt.timezone.utc).date()


def normalize(typ, value):
    need(isinstance(value, str) and value and value == value.strip(), "Empty or whitespace-padded value")
    if typ in {"ip_cidr", "source_ip_cidr"}:
        try:
            net = ipaddress.ip_network(value, strict=False)
        except ValueError as e:
            raise Invalid(str(e)) from e
        need(net.prefixlen != 0, "Default-route CIDR is forbidden")
        return str(net)
    if typ == "domain_regex":
        return value
    need(typ in {"domain", "domain_suffix"}, f"Unknown type: {typ}")
    dot = typ == "domain_suffix" and value.startswith(".")
    base = value[1:] if dot else value
    base = base.removesuffix(".").lower()
    try:
        base = base.encode("idna").decode("ascii")
    except UnicodeError as e:
        raise Invalid("Invalid IDNA domain") from e
    labels = base.split(".")
    need(1 < len(labels) and len(base) <= 253, f"Invalid domain: {value}")
    need(all(re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", s) for s in labels), f"Invalid domain: {value}")
    try:
        ipaddress.ip_address(base)
    except ValueError:
        pass
    else:
        raise Invalid("IP literal in domain field")
    return ("." if dot else "") + base


def public_suffix(domain, psl):
    """PSL exact/wildcard/exception rules, including private suffixes."""
    labels = domain.split(".")
    best = labels[-1]
    for i in range(len(labels)):
        tail = ".".join(labels[i:])
        if "!" + tail in psl:
            return ".".join(labels[i + 1:])
        if tail in psl:
            best = tail if len(tail) > len(best) else best
        if i and "*." + tail in psl:
            wildcard = ".".join(labels[i - 1:])
            best = wildcard if len(wildcard) > len(best) else best
    return best


def input_files(root):
    paths = [root / "VERSION", root / "tools.lock.json", root / "requirements.txt"]
    for folder in ("sources", "scripts", "tests"):
        paths += [p for p in (root / folder).rglob("*") if p.is_file() and "__pycache__" not in p.parts and not p.name.endswith(".pyc")]
    return {str(p.relative_to(root)): sha(p) for p in sorted(paths)}


def parse_dlc(text):
    """Parse the pinned provenance sidecar, never the production baseline."""
    result = []
    for number, original in enumerate(text.splitlines(), 1):
        line = original.split("#", 1)[0].strip()
        if not line:
            continue
        token, *attrs = line.split()
        need(all(a.startswith("@") and len(a) > 1 for a in attrs), f"Unknown DLC syntax at line {number}")
        prefix, sep, value = token.partition(":")
        if not sep:
            prefix, value = "domain", token
        need(prefix != "include" and not token.startswith("&"), f"DLC include/affiliation not implemented: line {number}")
        need(prefix in {"domain", "full", "regexp", "keyword"}, f"Unknown DLC prefix at line {number}")
        typ = {"domain": "domain_suffix", "full": "domain", "regexp": "domain_regex", "keyword": "domain_keyword"}[prefix]
        result.append({"type": typ, "value": value if typ == "domain_keyword" else normalize(typ, value), "attributes": attrs, "line": number})
    need(result, "Empty DLC input")
    return result


def covered(candidate, rows):
    """Only exact, suffix and CIDR containment; never guess regex containment."""
    typ, value = candidate["type"], candidate["value"]
    for row in rows:
        if row["type"] == typ and row["value"] == value:
            return True
        if row["type"] == "domain_suffix" and typ in {"domain", "domain_suffix"}:
            parent, child = row["value"], value.lstrip(".")
            if parent.startswith("."):
                if child.endswith(parent) or typ == "domain_suffix" and value == parent:
                    return True
            elif child == parent or child.endswith("." + parent):
                return True
        if typ in {"ip_cidr", "source_ip_cidr"} and row["type"] == typ:
            child, parent = ipaddress.ip_network(value), ipaddress.ip_network(row["value"])
            if child.version == parent.version and child.subnet_of(parent):
                return True
    return False


def discovery_entries(root):
    path = root / "sources/discovery/pending.yaml"
    if not path.exists():
        return []
    document = load(path)
    need(isinstance(document, dict) and document.get("schema") == 1 and isinstance(document.get("entries"), list), "Invalid discovery registry")
    seen = set()
    for row in document["entries"]:
        need(isinstance(row, dict) and row.get("artifact") in ARTIFACTS, "Invalid discovery artifact")
        ident = f"{row['artifact']}:{row.get('type')}:{row.get('value')}"
        need(row.get("id") == ident and ident not in seen, "Invalid/duplicate discovery id")
        need(row.get("review_status") == "pending", "Discovery registry must contain pending candidates")
        seen.add(ident)
    return document["entries"]


def archives(root):
    document = load(root / "sources/upstreams.yaml")
    need(document.get("schema") == 1 and document.get("archives"), "Empty/unknown upstream registry")
    result = {}
    for item in document["archives"]:
        need(item["id"] not in result, "Duplicate upstream id")
        path = local_path(root, item["path"])
        need(path.is_file() and sha(path) == item["sha256"], f"Archive hash mismatch: {item['id']}")
        if "metadata_path" in item or "metadata_sha256" in item:
            metadata = local_path(root, item.get("metadata_path"))
            need(metadata.is_file() and sha(metadata) == item.get("metadata_sha256"), f"Archive metadata hash mismatch: {item['id']}")
        need(item["url"].startswith("https://"), "Upstream URL must be HTTPS")
        if item.get("commit"):
            need(re.fullmatch(r"[0-9a-f]{40}", item["commit"]), "Upstream commit must be full SHA")
            need(item["commit"] in item["url"], "Upstream URL is not pinned to commit")
        result[item["id"]] = item
    return result


def baseline_inputs(root, registry):
    """Read archived SRS bytes with the pinned native reader before adding rows."""
    binary, _ = compiler(root)
    rows, metadata = {}, {}
    commits = set()
    with tempfile.TemporaryDirectory(prefix="sing-box-ai-baseline-") as scratch:
        for artifact in ("openai", "anthropic"):
            item, sidecar = registry["geosite-" + artifact], registry["dlc-" + artifact]
            need(item["kind"] == "srs-baseline" and item.get("role") == "baseline" and item.get("artifact") == artifact, "SRS must be the declared product baseline")
            need(sidecar["kind"] == "dlc" and sidecar.get("role") == "crosscheck", "DLC must be a provenance crosscheck")
            need(item.get("commit") and item["url"] == f"https://raw.githubusercontent.com/SagerNet/sing-geosite/{item['commit']}/geosite-{artifact}.srs", "Baseline must be pinned SagerNet product SRS")
            commits.add(item["commit"])
            source = local_path(root, item["path"])
            need(source.stat().st_size <= 2_000_000 and source.read_bytes()[:4] in (b"SRS\x01", b"SRS\x02"), "Unsupported baseline SRS version")
            decoded = Path(scratch) / (artifact + ".json")
            run([binary, "rule-set", "decompile", "--output", decoded, source])
            document = load(decoded)
            need(isinstance(document, dict) and document.get("version") in (1, 2), "Unreviewed upstream format version")
            version = document["version"]
            document["version"] = 2
            key = semantic_key(document)
            rule = document["rules"][0]
            need("source_ip_cidr" not in rule, "Product baseline must have destination direction")
            dlc = parse_dlc(local_path(root, sidecar["path"]).read_text())
            need(key == semantic_key(source_document(dlc)), "Pinned DLC and SRS baseline disagree")
            baseline = []
            for typ, values in sorted(rule.items()):
                for value in ([values] if isinstance(values, str) else values):
                    need(normalize(typ, value) == value, "Baseline normalization requires review")
                    need(typ not in {"domain", "domain_suffix"} or value.lstrip(".") not in FORBIDDEN, "Unacceptable shared parent in baseline")
                    baseline.append({"type": typ, "value": value, "direction": "destination", "origin": "baseline", "sources": [{"kind": "srs-baseline", "reference": item["id"]}], "dlc_provenance": [{"reference": sidecar["id"], **r} for r in dlc if covered(r, [{"type": typ, "value": value}])]})
            rows[artifact] = baseline
            metadata[artifact] = {"repo": "SagerNet/sing-geosite", "ref": item["commit"], "path": item["path"], "sha256": item["sha256"], "input_binary_version": version, "semantic_sha256": hashlib.sha256(json.dumps(key, sort_keys=True).encode()).hexdigest(), "crosscheck": {"path": sidecar["path"], "sha256": sidecar["sha256"], "ref": sidecar["commit"], "equivalent": True}}
    need(len(commits) == 1, "Product baselines must come from the same SagerNet commit")
    return rows, metadata


def review_entry(entry, mode, as_of, root):
    need(REVIEW_FIELDS <= entry.keys(), "Missing compatibility review fields")
    state = entry["review_status"]
    need(state in {"pending", "approved"}, "Unknown review_status")
    first = date(entry["first_seen"])
    need(first <= as_of, "Future first_seen")
    evidence = entry["evidence"]
    need(isinstance(evidence, list) and evidence, "Missing compatibility evidence")
    verified_products = {}
    for e in evidence:
        need(all(e.get(k) for k in ("kind", "reference", "observed_on", "conclusion", "product")), "Incomplete evidence")
        observed = date(e["observed_on"])
        need(first <= observed <= as_of, "Evidence date is outside review period")
        ref = local_path(root, e["reference"])
        need(ref.is_file(), "Evidence reference does not exist")
        if e["kind"] in {"runtime-validation", "user-confirmation"}:
            proof = load(ref)
            need(proof.get("result") == "passed" and proof.get("conclusion"), "Evidence does not attest success")
            need(proof.get("kind") == e["kind"], "Evidence kind mismatch")
            need(proof.get("observed_on") == e["observed_on"], "Evidence observation date mismatch")
            need(set(e["product"]) <= set(proof.get("products", [])), "Evidence product mismatch")
            need(proof.get("rule") == {"type": entry["type"], "value": entry["value"]}, "Evidence rule mismatch")
            if e["kind"] == "runtime-validation":
                need(all(proof.get(k) for k in ("environment", "client_version", "method", "verified_on")), "Runtime evidence lacks environment/version/method/date")
                need(date(proof["verified_on"]) == observed, "Runtime verification date does not match observation")
            else:
                need(proof.get("confirmed_by") == "maintainer" and proof.get("statement"), "Missing maintainer confirmation")
                anchors = load(root / "sources/policy.yaml").get("initial_confirmations", [])
                need(any(a.get("reference") == e["reference"] and a.get("sha256") == sha(ref) and a.get("approved_on") == e["observed_on"] for a in anchors), "User confirmation is not the pinned initial approval; renewal needs runtime validation")
                need(date(proof.get("verified_on")) == observed, "Initial confirmation date mismatch")
            verified_products.setdefault(observed, set()).update(e["product"])
    last, after = entry["last_verified"], entry["review_after"]
    need((last is None) == (after is None), "Partial review dates")
    if last is None:
        need(state == "pending", "Approved entry needs review dates")
    else:
        last, after = date(last), date(after)
        need(first <= last <= as_of and last < after <= last + dt.timedelta(days=30), "Invalid 30-day review window")
    if state == "approved":
        need(set(entry["product"]) <= verified_products.get(last, set()), "History alone cannot approve compatibility; need product-specific validation/confirmation at last_verified")
    if mode == "release":
        need(state == "approved" and last is not None and as_of < after, f"Unapproved/expired compatibility: {entry['value']}")


def canonical(root=ROOT, mode="candidate", as_of=None):
    need(mode in {"candidate", "release"}, "Unknown build mode")
    policy = load(root / "sources/policy.yaml")
    as_of = as_of or date(policy["review_as_of"])
    need(policy.get("schema") == 1 and policy.get("features"), "Invalid policy")
    enabled = policy["enabled_optional"]
    need(isinstance(enabled, list) and len(enabled) == len(set(enabled)), "Invalid optional selection")
    pending = discovery_entries(root)
    chosen = policy.get("selected_pending", [])
    need(isinstance(chosen, list) and len(chosen) == len(set(chosen)) and set(chosen) <= {r["id"] for r in pending}, "Invalid pending selection")
    need(mode != "release" or not chosen, "Selected pending candidates cannot be released")
    registry = archives(root)
    baselines, baseline_info = baseline_inputs(root, registry)
    policy = {**policy, "baseline_inputs": baseline_info}
    facts = {}
    for ident, item in registry.items():
        if item["kind"] == "official":
            doc = load(local_path(root, item["path"]))
            need(doc.get("schema") == 1 and doc.get("facts") and doc.get("url") == item["url"], "Invalid official snapshot")
            raw = registry.get(doc.get("raw_reference"), {})
            need(raw.get("sha256") and doc.get("raw_sha256") == raw["sha256"] and doc.get("locators"), "Official facts lack archived source provenance")
            if ident == "openai-voice":
                need(raw.get("id") == "voice-raw" and raw.get("kind") == "voice-json", "Voice provenance must reference the original JSON")
            else:
                need(raw.get("kind") == "official-source-record" and raw.get("id") == ident + "-source", "Official provenance must reference its own archived source record")
                record = load(local_path(root, raw["path"]))
                need(record.get("schema") == 1 and record.get("id") == raw["id"] and record.get("kind") == raw["kind"] and record.get("url") == raw["url"], "Source record identity mismatch")
                response_hash = record.get("original_response", {}).get("sha256", "")
                need(re.fullmatch(r"[0-9a-f]{64}", response_hash) and response_hash == doc.get("original_response_sha256") == raw.get("original_response_sha256"), "Original response provenance mismatch")
                need(record.get("retrieved_at") and record.get("extraction_method") and record.get("facts") and all(r.get("value") and r.get("locator") for r in record["facts"]), "Source record lacks retrieval/fact locators")
            facts[ident] = doc["facts"]
    psl, icann_psl = set(), set()
    private_section = False
    for line in local_path(root, registry["psl"]["path"]).read_text().splitlines():
        if line == "// ===BEGIN PRIVATE DOMAINS===":
            private_section = True
        if line and not line.startswith("//"):
            marker = "!" if line.startswith("!") else "*." if line.startswith("*.") else ""
            body = line[len(marker):].encode("idna").decode("ascii")
            psl.add(marker + body)
            if not private_section:
                icann_psl.add(marker + body)
    result, normalization = {}, []
    optional_seen = set()
    for artifact in ARTIFACTS:
        rows = load(root / f"sources/{artifact}.yaml")
        need(isinstance(rows, list), f"Invalid supplements: {artifact}")
        need(all(isinstance(r, dict) and r.get("review_status") != "pending" for r in rows), "Pending candidates belong in the discovery registry")
        entries = [(r, True) for r in rows]
        entries += [({k: v for k, v in r.items() if k not in {"id", "artifact"}}, r["id"] in chosen) for r in pending if r["artifact"] == artifact]
        selected = list(baselines.get(artifact, []))
        for entry, include in entries:
            need(isinstance(entry, dict) and COMMON_FIELDS - {"features"} <= entry.keys(), "Missing canonical fields")
            need(set(entry) <= COMMON_FIELDS | REVIEW_FIELDS, "Unknown canonical field")
            typ, status = entry["type"], entry["status"]
            need(typ in TYPES and status in STATUSES, "Unknown type/status")
            direction = "source" if artifact == "anthropic-ip" else "destination"
            need(entry["direction"] == direction, f"Wrong direction: {artifact}")
            need((typ == "source_ip_cidr") == (artifact == "anthropic-ip"), "Source/destination type mismatch")
            need(isinstance(entry["shared_dependency"], bool), "shared_dependency must be boolean")
            need(isinstance(entry["product"], list) and entry["product"] and all(isinstance(p, str) and p for p in entry["product"]), "Missing product")
            need(isinstance(entry["reason"], str) and entry["reason"], "Missing reason")
            value = normalize(typ, entry["value"])
            if value != entry["value"]:
                normalization.append({"artifact": artifact, "type": typ, "input": entry["value"], "normalized": value})
            if typ in {"domain", "domain_suffix"}:
                domain = value.lstrip(".")
                need(domain not in FORBIDDEN and public_suffix(domain, icann_psl) != domain, f"Public/shared parent is forbidden: {value}")
                if public_suffix(domain, psl) == domain:
                    # Private PSL boundaries also contain official Claude product scopes.
                    exception = policy.get("official_private_suffix_exceptions", {}).get(value)
                    need(exception and status in {"required", "feature-required"} and any(s.get("kind") == "official" and s.get("reference") == exception for s in entry["sources"]), f"Unreviewed private suffix: {value}")
            if typ == "domain_regex":
                need(value in policy["approved_regex"], "Regex is not in reviewed expression allowlist")
            need(isinstance(entry["sources"], list) and entry["sources"], "Missing provenance")
            official_matches = []
            for source in entry["sources"]:
                ref = source.get("reference")
                need(ref in registry and source.get("kind") == registry[ref]["kind"], "Unknown/mismatched provenance")
                if source["kind"] == "official":
                    official_matches += [f for f in facts[ref] if f["artifact"] == artifact and f["type"] == typ and normalize(typ, f["value"]) == value and f["direction"] == direction]
            if status in {"required", "feature-required", "optional"}:
                need(any(f["status"] == status and set(entry["product"]) <= set(f["product"]) and f["shared_dependency"] == entry["shared_dependency"] and set(f.get("features", [])) == set(entry.get("features", [])) for f in official_matches), f"No matching official fact: {value}")
            else:
                review_entry(entry, mode if include else "candidate", as_of, root)
                need(typ in {"domain", "domain_regex"} or typ == "domain_suffix" and entry["review_status"] == "pending", "Non-official CIDR/suffix expansion requires a reviewed official fact")
            if status == "feature-required":
                need(entry.get("features") and set(entry["features"]) <= set(policy["features"]), "Feature dependency not enabled")
            if status == "optional":
                optional_seen.add(value)
                if value not in enabled:
                    continue
            if include:
                selected.append({**entry, "value": value, "origin": "supplement"})
        need(selected, f"Empty selected rules: {artifact}")
        result[artifact] = selected
    need(set(enabled) <= optional_seen, "Unknown optional selection")
    # A mandatory fact may be supplied by the full SRS or by an approved supplement.
    for rows in facts.values():
        for fact in rows:
            if fact["status"] in {"required", "feature-required"}:
                value = {"type": fact["type"], "value": normalize(fact["type"], fact["value"])}
                eligible = [r for r in result[fact["artifact"]] if r["origin"] == "baseline" or set(fact["product"]) <= set(r["product"])]
                need(covered(value, eligible), f"Missing official baseline: {fact['value']}")
    voice = load(local_path(root, registry["voice-raw"]["path"]))
    need(set(voice) == {"creationTime", "prefixes"} and voice["prefixes"], "Invalid/empty Voice JSON")
    voice_values = []
    for prefix in voice["prefixes"]:
        need(set(prefix) in ({"ipv4Prefix"}, {"ipv6Prefix"}), "Unknown Voice JSON prefix field")
        key, value = next(iter(prefix.items()))
        net = ipaddress.ip_network(value)
        need(net.version == (4 if key == "ipv4Prefix" else 6), "Voice IP family mismatch")
        voice_values.append(str(net))
    actual_voice = [r["value"] for r in result["openai"] if r["type"] == "ip_cidr" and "chatgpt-voice" in r.get("features", [])]
    need(sorted(actual_voice) == sorted(voice_values), "Voice JSON and canonical differ")
    return result, policy, normalization


def source_document(rows):
    rule = {}
    unique = [{"type": typ, "value": value} for typ, value in sorted({(r["type"], r["value"]) for r in rows})]
    for row in unique:
        if covered(row, [other for other in unique if other != row]):
            continue
        rule.setdefault(row["type"], set()).add(row["value"])
    return {"version": 2, "rules": [{k: sorted(v) for k, v in sorted(rule.items())}]}


def semantic_key(document):
    need(isinstance(document, dict) and set(document) == {"version", "rules"}, "Unknown source root")
    need(document["version"] == 2 and isinstance(document["rules"], list) and len(document["rules"]) == 1, "Expected v2, one default rule")
    rule = document["rules"][0]
    need(isinstance(rule, dict) and rule and set(rule) <= TYPES, "Unknown/logical/empty SRS rule")
    need(all(isinstance(v, str) or isinstance(v, list) and all(isinstance(s, str) for s in v) for v in rule.values()), "Invalid SRS field type")
    fields = {k: ({v} if isinstance(v, str) else set(v)) for k, v in rule.items()}
    need(all(v and all(isinstance(s, str) for s in v) for v in fields.values()), "Empty/invalid SRS field")
    exact = fields.get("domain", set()).copy()
    dots = set()
    for suffix in fields.get("domain_suffix", set()):
        if not suffix.startswith("."):
            exact.add(suffix)
        dots.add("." + suffix.lstrip("."))
    dots = {s for s in dots if not any(s != parent and s.endswith(parent) for parent in dots)}
    exact = {s for s in exact if not any(s.endswith(parent) for parent in dots)}
    key = {"domain": sorted(exact), "domain_suffix": sorted(dots), "domain_regex": sorted(fields.get("domain_regex", set()))}
    for typ in ("ip_cidr", "source_ip_cidr"):
        nets = [ipaddress.ip_network(s) for s in fields.get(typ, set())]
        key[typ] = [str(n) for family in (4, 6) for n in ipaddress.collapse_addresses(n for n in nets if n.version == family)]
    return key


def compiler(root=ROOT, binary=None):
    binary = Path(binary or root / ".tools/sing-box").resolve()
    lock = load(root / "tools.lock.json")["sing_box"]
    need(binary.is_file(), "Compiler missing; run python3 scripts/bootstrap.py")
    digest = sha(binary)
    matches = [p for p, data in lock["platforms"].items() if data["binary_sha256"] == digest]
    need(len(matches) == 1, "Compiler binary is not hash-pinned")
    version = subprocess.run([str(binary), "version"], check=True, capture_output=True, text=True).stdout.splitlines()[0]
    need(version == "sing-box version " + lock["version"], "Compiler version mismatch")
    return binary, {"version": lock["version"], "commit": lock["commit"], "platform": matches[0], "sha256": digest}


def run(args, **kwargs):
    completed = subprocess.run([str(a) for a in args], capture_output=True, text=True, **kwargs)
    need(completed.returncode == 0, f"Command failed: {args[0]}\n{completed.stderr[-4000:]}")
    return completed
