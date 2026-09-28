"""Real alpha.9 consumers, with loopback-only packet and outbound fixtures.

Usage: python3 tests/consumer_durability.py --candidate DIR --config CONFIG
  --output NEW_DIRECTORY [--binary .tools/sing-box] [--baseline dist]

No system settings, TUN, production processes, or N100 are accessed. Complete
external SRS inputs are downloaded read-only; client traffic ends at local SOCKS
observers. The production direct/proxy *tags* are preserved, but their transports
are observers: these tests prove selection, not Internet connectivity.
"""
import argparse
import contextlib
import copy
import hashlib
import http.server
import ipaddress
import json
import pathlib
import re
import socket
import socketserver
import ssl
import struct
import subprocess
import sys
import threading
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "docs/evidence/round3/consumer"))
import loopback_dns as dns_fixture

ADDITIONS = {
    "openai": ["github.com", "api.github.com", "release-assets.githubusercontent.com", "registry.npmjs.org"],
    "anthropic": ["fonts.googleapis.com", "fonts.gstatic.com"],
}
QTYPES = {1: "A", 28: "AAAA", 16: "TXT", 15: "MX", 64: "SVCB", 5: "CNAME", 65: "HTTPS"}
REVISION = "132b38e9caaba1a1959354d518e54d2d08419afe"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def recv(sock, size):
    value = b""
    while len(value) < size:
        chunk = sock.recv(size - len(value))
        if not chunk:
            raise EOFError("short SOCKS packet")
        value += chunk
    return value


class Observer(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True


class Observe(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(2)
        try:
            ver, count = recv(self.request, 2)
            assert ver == 5
            recv(self.request, count)
            self.request.sendall(b"\x05\x00")
            ver, command, _, kind = recv(self.request, 4)
            if kind == 3:
                host = recv(self.request, recv(self.request, 1)[0]).decode()
            else:
                host = str(ipaddress.ip_address(recv(self.request, 4 if kind == 1 else 16)))
            port = struct.unpack("!H", recv(self.request, 2))[0]
            self.server.events.append({"outbound": self.server.tag, "host": host, "port": port, "address_type": kind})
            self.request.sendall(b"\x05\x00\x00\x01\x7f\x00\x00\x01\x00\x00")
            # Wait for payload to ensure the caller consumes the SOCKS response first.
            recv(self.request, 1)
            self.request.sendall(b"AUDIT-" + self.server.tag.encode())
        except (OSError, EOFError):
            pass


def serve(server):
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def port(family=socket.AF_INET, kind=socket.SOCK_STREAM):
    with socket.socket(family, kind) as sock:
        sock.bind(("::1" if family == socket.AF_INET6 else "127.0.0.1", 0))
        return sock.getsockname()[1]


def hello(host):
    incoming, outgoing = ssl.MemoryBIO(), ssl.MemoryBIO()
    client = ssl.create_default_context().wrap_bio(incoming, outgoing, server_hostname=host)
    try:
        client.do_handshake()
    except ssl.SSLWantReadError:
        pass
    return outgoing.read()


def send_socks(listen_port, host):
    with socket.create_connection(("127.0.0.1", listen_port), timeout=2) as sock:
        sock.sendall(b"\x05\x01\x00")
        assert recv(sock, 2) == b"\x05\x00"
        try:
            address = ipaddress.ip_address(host)
            target = bytes([1 if address.version == 4 else 4]) + address.packed
        except ValueError:
            target = bytes([3, len(host)]) + host.encode()
        sock.sendall(b"\x05\x01\x00" + target + struct.pack("!H", 443))
        try:
            response = recv(sock, 4)
            if response[1] != 0:
                return {"connected": False, "reply": response[1]}
            recv(sock, (4 if response[3] == 1 else 16) + 2)
            sock.sendall(b"test")
            return {"connected": True, "marker": sock.recv(128).decode()}
        except (OSError, EOFError):
            return {"connected": False}


def send_tls(listen_port, host, family):
    with socket.socket(socket.AF_INET6 if family == 6 else socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(2)
        sock.connect(("::1" if family == 6 else "127.0.0.1", listen_port))
        sock.sendall(hello(host))
        try:
            return {"marker": sock.recv(128).decode(), "ingress_family": family}
        except (OSError, UnicodeDecodeError):
            return {"marker": "", "ingress_family": family}


class Harness:
    def __init__(self, args):
        self.args = args
        self.out = args.output
        self.out.mkdir(parents=True, exist_ok=False)
        self.rows, self.processes, self.inputs = [], [], []
        self.observers = []
        self.dns_servers = []
        for tag in ["direct", "proxy", "bridge"]:
            server = Observer(("127.0.0.1", 0), Observe)
            server.tag, server.events = tag, []
            self.observers.append(serve(server))
        for tag in ["dns_proxy", "dns_direct", "dns_local", "dns_mdns"]:
            self.dns_servers.append(dns_fixture.upstream(tag, {1: "198.51.100.10", 28: "2001:db8::10"}))
        self.ports = {"socks": port(), "dns": port(kind=socket.SOCK_DGRAM), "tls4": port(), "tls6": port(socket.AF_INET6)}

    def close(self):
        for server in self.observers + self.dns_servers:
            server.shutdown()
            server.server_close()

    def base(self):
        return {
            "log": {"level": "debug", "timestamp": False},
            "dns": {"disable_cache": True, "servers": [
                {"type": "udp", "tag": s.tag, "server": "127.0.0.1", "server_port": s.server_address[1]}
                for s in self.dns_servers if s.tag != "dns_mdns"
            ] + [{"type": "hosts", "tag": tag, "path": []} for tag in ["hosts", "dns_mdns"]], "rules": [], "final": "dns_direct"},
            "inbounds": [
                {"type": "socks", "tag": "audit-socks", "listen": "127.0.0.1", "listen_port": self.ports["socks"]},
                {"type": "direct", "tag": "audit-dns", "listen": "127.0.0.1", "listen_port": self.ports["dns"], "network": "udp", "override_address": "127.0.0.1", "override_port": 53},
                {"type": "direct", "tag": "audit-tls4", "listen": "127.0.0.1", "listen_port": self.ports["tls4"], "network": "tcp", "override_address": "198.51.100.200", "override_port": 443},
                {"type": "direct", "tag": "audit-tls6", "listen": "::1", "listen_port": self.ports["tls6"], "network": "tcp", "override_address": "2001:db8:ffff::200", "override_port": 443},
            ],
            "outbounds": [{"type": "socks", "tag": s.tag, "server": "127.0.0.1", "server_port": s.server_address[1], "version": "5"} for s in self.observers],
            "route": {"final": "direct", "default_domain_resolver": "dns_direct", "rules": [
                {"port": 53, "action": "hijack-dns"}, {"action": "sniff", "sniffer": ["tls"], "timeout": "80ms"}
            ], "rule_set": []},
        }

    def product(self, product, directory):
        cfg = self.base()
        tag = "geosite-" + product
        cfg["route"]["rule_set"] = [{"type": "local", "tag": tag, "format": "binary", "path": str((directory / (product + ".srs")).resolve())}]
        cfg["route"]["rules"] += [{"rule_set": tag, "ip_version": 6, "action": "reject", "no_drop": True}, {"rule_set": tag, "outbound": "proxy"}]
        cfg["dns"]["rules"] = [{"query_type": "HTTPS", "action": "predefined"}, {"rule_set": tag, "query_type": "AAAA", "action": "predefined"}, {"rule_set": tag, "server": "dns_proxy"}]
        return cfg

    @contextlib.contextmanager
    def running(self, label, cfg):
        path, log = self.out / (label + ".json"), self.out / (label + ".log")
        write(path, cfg)
        check = subprocess.run([self.args.binary, "check", "-c", str(path)], capture_output=True, text=True)
        assert check.returncode == 0, check.stderr
        with log.open("w") as stream:
            process = subprocess.Popen([self.args.binary, "run", "-c", str(path)], stdout=stream, stderr=subprocess.STDOUT)
            try:
                for _ in range(100):
                    if process.poll() is not None or "sing-box started" in log.read_text():
                        break
                    time.sleep(.02)
                assert process.poll() is None and "sing-box started" in log.read_text(), log.read_text()
                yield log
            finally:
                if process.poll() is None:
                    process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)
                self.processes.append({"case": label, "pid": process.pid, "exited": True, "exit": process.returncode})

    def dns(self, case, log, host, qt, expected_server, expected_index=None):
        before = [len(s.events) for s in self.dns_servers]
        offset = log.stat().st_size
        answer = dns_fixture.query(self.ports["dns"], host, qt)
        time.sleep(.005)
        events = sum([s.events[n:] for s, n in zip(self.dns_servers, before)], [])
        trace = re.sub(r"\x1b\[[0-9;]*m", "", log.read_text()[offset:])
        matches = [{"index": int(i), "description": d} for i, d in re.findall(r"dns: match\[(\d+)\] (.*)", trace)]
        row = {"case": case, "kind": "dns", "host": host, "qtype": QTYPES[qt], "events": events, "matches": matches, **answer}
        self.rows.append(row)
        assert answer["rcode"] == 0, row
        expected_events = expected_server if isinstance(expected_server, list) else [] if expected_server is None else [expected_server]
        assert sorted(e["server"] for e in events) == sorted(expected_events), row
        if expected_server is None:
            assert answer["answer_count"] == 0 and answer["answers"] == [], row
        elif qt in (1, 28):
            final_server = "dns_proxy" if "dns_proxy" in expected_events else expected_events[-1]
            expected_address = next(s.addresses[qt] for s in self.dns_servers if s.tag == final_server)
            assert answer["answer_count"] == 1 and answer["answers"] == [{"type": qt, "value": expected_address}], row
        if expected_index is not None:
            assert matches and matches[0]["index"] == expected_index, row
        return row

    def route(self, case, log, host, expected, family=None, expected_index=None):
        before = [len(s.events) for s in self.observers]
        offset = log.stat().st_size
        result = send_tls(self.ports["tls" + str(family)], host, family) if family else send_socks(self.ports["socks"], host)
        time.sleep(.005)
        events = sum([s.events[n:] for s, n in zip(self.observers, before)], [])
        trace = re.sub(r"\x1b\[[0-9;]*m", "", log.read_text()[offset:])
        matches = [{"index": int(i), "description": d} for i, d in re.findall(r"router: match\[(\d+)\] (.*)", trace)]
        row = {"case": case, "kind": "route", "host": host, "family": family, "events": events, "matches": matches, **result}
        self.rows.append(row)
        assert [e["outbound"] for e in events] == ([] if expected == "reject" else [expected]), row
        if expected == "reject":
            assert "reject" in trace, trace
            assert not result.get("marker"), row
        else:
            assert result.get("marker") == "AUDIT-" + expected, row
        if expected_index is not None:
            terminal = [m for m in matches if "=> sniff" not in m["description"] and "route-options" not in m["description"]]
            assert terminal and terminal[-1]["index"] == expected_index, row
        return row

    def independent(self):
        for product, hosts in ADDITIONS.items():
            cfg = self.product(product, self.args.candidate)
            case = "independent-" + product
            with self.running(case, cfg) as log:
                for host in hosts:
                    for qt in QTYPES:
                        self.dns(case, log, host, qt, None if qt in (28, 65) else "dns_proxy", 0 if qt == 65 else 1 if qt == 28 else 2)
                    for family in [None, 4, 6]:
                        self.route(case, log, host, "reject" if family == 6 else "proxy", family)
                    for negative in ["probe." + host, host + ".invalid", host.replace(".", "-", 1) + ".invalid"]:
                        self.dns(case, log, negative, 1, "dns_direct")
                        self.route(case, log, negative, "direct")
                for host in ["auth.openai.com"] if product == "openai" else ["api.anthropic.com", "challenges.cloudflare.com"]:
                    self.route(case, log, host, "proxy")
                # Real IP destinations; observer prevents network egress.
                ips = [("23.79.201.0", "direct"), ("198.51.100.1", "direct")]
                if product == "anthropic":
                    ips += [("160.79.104.0", "proxy"), ("160.79.105.255", "proxy"), ("160.79.106.0", "direct"), ("2607:6bc0::1", "reject"), ("2607:6bc1::1", "direct")]
                else:
                    source = self.out / "openai-decompiled.json"
                    subprocess.run([self.args.binary, "rule-set", "decompile", "--output", str(source), str(self.args.candidate / "openai.srs")], check=True, capture_output=True)
                    ip = json.loads(source.read_text())["rules"][0]["ip_cidr"][0].split("/")[0]
                    ips += [(ip, "proxy")]
                for host, expected in ips:
                    self.route(case, log, host, expected)
            for mutation in ["removed", "early-direct", "early-reject"]:
                changed = copy.deepcopy(cfg)
                if mutation == "removed":
                    changed["route"]["rule_set"] = []
                    changed["route"]["rules"] = changed["route"]["rules"][:2]
                    changed["dns"]["rules"] = changed["dns"]["rules"][:1]
                else:
                    changed["route"]["rules"].insert(2, {"domain": hosts, **({"outbound": "direct"} if mutation == "early-direct" else {"action": "reject", "no_drop": True})})
                    changed["dns"]["rules"].insert(1, {"domain": hosts, "server": "dns_direct"})
                label = product + "-" + mutation
                with self.running(label, changed) as log:
                    for host in hosts:
                        self.route(label, log, host, "reject" if mutation == "early-reject" else "direct")
                        self.dns(label, log, host, 1, "dns_direct")

    def full_order(self):
        original = json.loads(self.args.config.read_text())
        fixture = self.out / "fixtures"
        fixture.mkdir()
        full_sets = []
        cached_inputs = {}
        if self.args.fixture_cache:
            cached_inputs = {i["tag"]: i for i in json.loads((self.args.fixture_cache.parent / "external-inputs.json").read_text())}
        for entry in original["route"]["rule_set"]:
            tags = entry["tag"] if isinstance(entry["tag"], list) else [entry["tag"]]
            for tag in tags:
                if tag in ["geosite-openai", "geosite-anthropic"]:
                    continue
                url = entry["url"].replace("{tag}", tag)
                destination = fixture / (tag + ".srs")
                if self.args.fixture_cache and (self.args.fixture_cache / destination.name).exists():
                    destination.write_bytes((self.args.fixture_cache / destination.name).read_bytes())
                    assert cached_inputs[tag]["sha256"] == sha(destination) and cached_inputs[tag]["url"] == url
                else:
                    with urllib.request.urlopen(url, timeout=45) as response:
                        destination.write_bytes(response.read())
                self.inputs.append({"tag": tag, "url": url, "sha256": sha(destination), "bytes": destination.stat().st_size})
                full_sets.append({"type": "local", "format": "binary", "tag": tag, "path": str(destination.resolve())})
        write(self.out / "external-inputs.json", self.inputs)
        for oa_new, an_new in [(False, False), (True, False), (False, True), (True, True)]:
            cfg = self.base()
            cfg["dns"]["rules"] = copy.deepcopy(original["dns"]["rules"])
            cfg["dns"]["final"] = original["dns"]["final"]
            cfg["route"]["rules"] = copy.deepcopy(original["route"]["rules"])
            assert cfg["route"]["rules"][0] == {"network": "icmp", "preferred_by": "bridge", "outbound": "bridge"}
            # No real bridge/interface is started. Keep slot 0, outside TCP scope.
            cfg["route"]["rules"][0] = {"network": "icmp", "action": "reject", "no_drop": True}
            cfg["route"]["final"] = original["route"]["final"]
            cfg["route"]["rule_set"] = full_sets + [
                {"type": "local", "tag": "geosite-" + product, "format": "binary", "path": str(((self.args.candidate if new else self.args.baseline) / (product + ".srs")).resolve())}
                for product, new in [("openai", oa_new), ("anthropic", an_new)]
            ]
            case = "original-order-" + str(int(oa_new)) + str(int(an_new))
            assert cfg["route"]["rules"][1:] == original["route"]["rules"][1:]
            assert cfg["dns"]["rules"] == original["dns"]["rules"]
            if not oa_new and not an_new:
                # Values from production transports/inbounds are intentionally omitted.
                transforms = []
                def changed_paths(before, after, path=""):
                    if isinstance(before, dict) and isinstance(after, dict):
                        for key in sorted(before.keys() | after.keys()):
                            target = path + "/" + key
                            if key not in before:
                                transforms.append({"op": "add", "path": target})
                            elif key not in after:
                                transforms.append({"op": "remove", "path": target})
                            else:
                                changed_paths(before[key], after[key], target)
                    elif before != after:
                        transforms.append({"op": "replace", "path": path})
                changed_paths(original, cfg)
                write(self.out / "fixture-transform.json", {
                    "changed_objects_values_omitted": transforms,
                    "dns_rules_byte_value_equal": True,
                    "route_rules_1_onward_value_equal": True,
                    "route_slot_0": {"before": original["route"]["rules"][0], "after": cfg["route"]["rules"][0]},
                    "outbound_tag_mapping": [{"tag": s.tag, "fixture_type": "socks", "fixture_address": "127.0.0.1", "fixture_port": s.server_address[1]} for s in self.observers],
                    "hosts_and_mdns": "empty hosts resolvers; no preferred match for public test witnesses",
                    "external_rule_sets": "Complete binaries in fixtures, bound by external-inputs.json; no witness projection.",
                    "unchanged_dns_final": cfg["dns"]["final"], "unchanged_route_final": cfg["route"]["final"],
                    "excluded": ["ICMP bridge", "mDNS discovery", "TUN", "production outbound transport", "public IPv6 connectivity"],
                })
            with self.running(case, cfg) as log:
                for product, hosts in ADDITIONS.items():
                    for host in hosts:
                        font = product == "anthropic"
                        dns_index = 14 if font else 16 if oa_new or host in ["github.com", "registry.npmjs.org"] else 17
                        route_index = 19 if font else 21 if oa_new else 23 if host in ["github.com", "registry.npmjs.org"] else 25
                        for qt in QTYPES:
                            suppressed = qt == 65 or qt == 28 and (font or oa_new or host in ["github.com", "registry.npmjs.org"])
                            index = 0 if qt == 65 else (13 if font else 15) if suppressed else dns_index
                            self.dns(case, log, host, qt, None if suppressed else "dns_proxy", index)
                        self.route(case, log, host, "proxy", expected_index=route_index)
                        self.route(case, log, host, "proxy", family=4, expected_index=route_index)
                        ipv6_reject = font or oa_new or host in ["github.com", "registry.npmjs.org"]
                        self.route(case, log, host, "reject" if ipv6_reject else "proxy", family=6, expected_index=route_index - 1 if ipv6_reject else route_index)

    def response_ip(self):
        direct = next(s for s in self.dns_servers if s.tag == "dns_direct")
        original = direct.addresses.copy()
        try:
            for product in ADDITIONS:
                cfg = self.product(product, self.args.candidate)
                source = self.out / (product + "-ip-decompiled.json")
                subprocess.run([self.args.binary, "rule-set", "decompile", "--output", str(source), str(self.args.candidate / (product + ".srs"))], check=True, capture_output=True)
                cidrs = json.loads(source.read_text())["rules"][0]["ip_cidr"]
                for cidr in cidrs[:1] + [c for c in cidrs if ":" in c]:
                    address = ipaddress.ip_network(cidr).network_address
                    qt = 1 if address.version == 4 else 28
                    for matches in [False, True]:
                        direct.addresses = original.copy()
                        if matches:
                            direct.addresses[qt] = str(address)
                        cfg["dns"]["rules"] = [
                            {"action": "evaluate", "server": "dns_direct"},
                            {"match_response": True, "rule_set": "geosite-" + product, "server": "dns_proxy"},
                            {"match_response": True, "action": "respond"},
                        ]
                        case = "response-ip-" + product + "-" + str(qt) + "-" + str(int(matches))
                        with self.running(case, cfg) as log:
                            row = self.dns(case, log, "unmatched-destination.audit.invalid", qt, ["dns_direct", "dns_proxy"] if matches else ["dns_direct"], 0)
                            assert any(m["index"] == (1 if matches else 2) for m in row["matches"]), row
        finally:
            direct.addresses = original

    def remote(self):
        requests = []
        payloads = {"/" + p + ".srs": (self.args.candidate / (p + ".srs")).read_bytes() for p in ADDITIONS}
        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                body = payloads.get(self.path)
                requests.append({"path": self.path, "sha256": hashlib.sha256(body).hexdigest() if body else None})
                self.send_response(200 if body else 404)
                self.end_headers()
                self.wfile.write(body or b"missing")
            def log_message(self, *_):
                pass
        server = serve(http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler))
        try:
            for product, hosts in ADDITIONS.items():
                cfg = self.product(product, self.args.candidate)
                cfg["http_clients"] = [{"tag": "bootstrap-http"}]
                cfg["route"]["default_http_client"] = "bootstrap-http"
                cfg["route"]["rule_set"] = [{"type": "remote", "tag": "geosite-" + product, "format": "binary", "url": "http://127.0.0.1:" + str(server.server_address[1]) + "/" + product + ".srs"}]
                cache = self.out / ("cold-" + product + ".db")
                assert not cache.exists()
                cfg["experimental"] = {"cache_file": {"enabled": True, "path": str(cache.resolve())}}
                case = "cold-remote-" + product
                with self.running(case, cfg) as log:
                    self.route(case, log, hosts[0], "proxy")
                    self.dns(case, log, hosts[0], 1, "dns_proxy", 2)
                assert cache.exists()
            assert [r["path"] for r in requests] == ["/openai.srs", "/anthropic.srs"], requests
            write(self.out / "remote-requests.json", requests)
        finally:
            server.shutdown()
            server.server_close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=pathlib.Path, required=True)
    parser.add_argument("--config", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--baseline", type=pathlib.Path, default=ROOT / "dist")
    parser.add_argument("--binary", default=str(ROOT / ".tools/sing-box"))
    parser.add_argument("--fixture-cache", type=pathlib.Path)
    args = parser.parse_args()
    version = subprocess.check_output([args.binary, "version"], text=True)
    assert "1.15.0-alpha.9" in version and REVISION in version, version
    lock = json.loads((ROOT / "tools.lock.json").read_text())["sing_box"]["platforms"]
    assert sha(pathlib.Path(args.binary)) in {p["binary_sha256"] for p in lock.values()}, "binary hash mismatch"
    harness = Harness(args)
    passed = False
    try:
        harness.independent()
        harness.full_order()
        harness.response_ip()
        harness.remote()
        passed = True
    finally:
        harness.close()
        cleanup = []
        for name, address, number in [(k, "::1" if k == "tls6" else "127.0.0.1", p) for k, p in harness.ports.items() if k != "dns"] + [(s.tag, "127.0.0.1", s.server_address[1]) for s in harness.observers]:
            with socket.socket(socket.AF_INET6 if address == "::1" else socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(.2)
                cleanup.append({"listener": name, "port": number, "closed": sock.connect_ex((address, number)) != 0})
        for name, number in [("dns-inbound", harness.ports["dns"])] + [(s.tag, s.server_address[1]) for s in harness.dns_servers]:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.bind(("127.0.0.1", number))
                cleanup.append({"listener": name, "port": number, "closed": True})
        passed = passed and all(c["closed"] for c in cleanup)
        report = {
            "assertions_passed": passed, "binary_version": version, "binary_sha256": sha(pathlib.Path(args.binary)),
            "config_sha256": sha(args.config), "candidate": {p: sha(args.candidate / (p + ".srs")) for p in ADDITIONS},
            "rows": harness.rows, "processes": harness.processes, "external_inputs": harness.inputs,
            "cleanup": cleanup,
            "counts": {group: sum(r["case"].startswith(group) for r in harness.rows) for group in ["independent-", "original-order-", "openai-", "anthropic-", "response-ip-", "cold-remote-"]},
            "limitations": [
                "Local observer transports replace production outbounds; direct/proxy labels test routing selection, not Internet connectivity.",
                "IPv6 uses real ::1 ingress and synthetic public destination metadata; no public IPv6 business connection is claimed.",
                "Original DNS rules and route rules 1..27 are unchanged and in original order. ICMP-only route slot 0 becomes ICMP reject to avoid a real bridge; ICMP is not tested.",
                "hosts and dns_mdns use empty hosts transports so preferred_by is false for the public witnesses; local hosts/mDNS discovery is outside scope.",
                "Controlled HTTP cold-start fixture has no production proxy credentials or GitHub bootstrap. Actual candidate URL follows upload in step 3.",
                "No N100 access, config write, reload, restart, TUN, system DNS, routes, or firewall changes.",
            ],
        }
        write(args.output / "results.json", report)
    assert passed, "consumer assertions or listener cleanup failed; see results.json"
    print(json.dumps({"passed": passed, "requests": len(harness.rows), "processes": len(harness.processes), "results": str(args.output / "results.json")}))


if __name__ == "__main__":
    main()
