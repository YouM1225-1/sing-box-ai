"""验证 claude.dev 新增后缀的真实隔离消费者行为；仅监听回环地址。"""
import argparse
import hashlib
import http.server
import json
from pathlib import Path
import socket
import sys

from consumer_durability import Harness, QTYPES, ROOT, serve, sha, write

sys.path.insert(0, str(ROOT / "scripts"))
from common import compiler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, default=ROOT / "artifacts/v0.1.1")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    binary, identity = compiler()
    args.binary = str(binary)
    harness = Harness(args)
    positives = ["claude.dev", "a.claude.dev", "a.b.claude.dev"]
    negatives = ["notclaude.dev", "claude.dev.invalid", "a.claude.dev.invalid", "claude-dev.invalid"]
    body = (args.candidate / "anthropic.srs").read_bytes()
    requests = []
    cleanup = []
    passed = False
    server = None

    def probe(label, cfg, selected):
        with harness.running(label, cfg) as log:
            for host in positives + negatives:
                matched = selected and host in positives
                for qt in QTYPES:
                    suppressed = qt == 65 or matched and qt == 28
                    resolver = None if suppressed else "dns_proxy" if matched else "dns_direct"
                    harness.dns(label, log, host, qt, resolver)
                for family in [None, 4, 6]:
                    expected = "reject" if matched and family == 6 else "proxy" if matched else "direct"
                    harness.route(label, log, host, expected, family)

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            assert self.path == "/anthropic.srs", self.path
            requests.append({"path": self.path, "sha256": hashlib.sha256(body).hexdigest()})
            self.send_response(200)
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *_):
            pass

    try:
        probe("old-anthropic", harness.product("anthropic", args.baseline), False)
        probe("new-anthropic", harness.product("anthropic", args.candidate), True)
        probe("openai-negative", harness.product("openai", args.candidate), False)
        # 两产品的新旧组合；保留 OpenAI 在 Anthropic 前的产品顺序。
        for oa_new, an_new in [(False, False), (True, False), (False, True), (True, True)]:
            cfg = harness.product("anthropic", args.candidate if an_new else args.baseline)
            oa = harness.product("openai", args.candidate if oa_new else args.baseline)
            cfg["route"]["rule_set"] = oa["route"]["rule_set"] + cfg["route"]["rule_set"]
            cfg["route"]["rules"][2:2] = oa["route"]["rules"][2:]
            cfg["dns"]["rules"][1:1] = oa["dns"]["rules"][1:]
            probe("combination-" + str(int(oa_new)) + str(int(an_new)), cfg, an_new)
        server = serve(http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler))
        cfg = harness.product("anthropic", args.candidate)
        cfg["http_clients"] = [{"tag": "bootstrap-http"}]
        cfg["route"]["default_http_client"] = "bootstrap-http"
        cfg["route"]["rule_set"] = [{"type": "remote", "tag": "geosite-anthropic", "format": "binary", "url": "http://127.0.0.1:" + str(server.server_address[1]) + "/anthropic.srs"}]
        cache = args.output / "cold.db"
        assert not cache.exists()
        cfg["experimental"] = {"cache_file": {"enabled": True, "path": str(cache.resolve())}}
        probe("cold-remote-anthropic", cfg, True)
        assert cache.exists() and len(requests) == 1, requests
        passed = True
    finally:
        if server:
            server.shutdown()
            server.server_close()
        harness.close()
        tcp = [(k, "::1" if k == "tls6" else "127.0.0.1", p) for k, p in harness.ports.items() if k != "dns"]
        tcp += [(s.tag, "127.0.0.1", s.server_address[1]) for s in harness.observers]
        if server:
            tcp.append(("http-fixture", "127.0.0.1", server.server_address[1]))
        for name, address, number in tcp:
            with socket.socket(socket.AF_INET6 if address == "::1" else socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(.2)
                cleanup.append({"listener": name, "closed": sock.connect_ex((address, number)) != 0})
        for name, number in [("dns-inbound", harness.ports["dns"])] + [(s.tag, s.server_address[1]) for s in harness.dns_servers]:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.bind(("127.0.0.1", number))
                cleanup.append({"listener": name, "closed": True})
        passed = passed and all(x["closed"] for x in cleanup) and all(x["exited"] for x in harness.processes)
        report = {"passed": passed, "compiler": identity, "script_sha256": sha(Path(__file__)), "baseline": {p: sha(args.baseline / (p + ".srs")) for p in ["openai", "anthropic"]}, "candidate": {p: sha(args.candidate / (p + ".srs")) for p in ["openai", "anthropic"]}, "requests": len(harness.rows), "rows": harness.rows, "processes": harness.processes, "cleanup": cleanup, "remote_downloads": requests, "limitations": ["仅隔离产品规则及其组合，未验证完整生产配置顺序。", "仅回环观察器、受控DNS与IPv6元数据，不证明公网出口或账户功能。", "未改系统网络、未连接N100、未发布新规则。"]}
        write(args.output / "results.json", report)
    assert passed, "消费者断言或清理失败"
    print(json.dumps({"passed": passed, "requests": len(harness.rows), "processes": len(harness.processes), "listeners_closed": len(cleanup)}))


if __name__ == "__main__":
    main()
