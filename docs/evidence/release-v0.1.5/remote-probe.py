"""验证固定 v0.1.5 GitHub 制品的真实空缓存加载；仅回环业务探测。"""
import argparse
import datetime
import hashlib
import ipaddress
import json
import pathlib
import re
import socket
import struct
import subprocess
import time
import urllib.parse
import urllib.request

EXPECTED = {'anthropic': '0d8e26718c663ffdb03d0d32a2cf42bf61be540787c46fa7684bf1a70a23c5f1', 'openai': 'a910767e3f07dfe89e2f72639960612872361d9ae1c8553ddd4a59c8f154778f', 'anthropic-ip': '9f3f914eb510bd19892581295400cc42f07199e6045a8718e81d0c8a0b7f684c'}

# 主监听保持 Anthropic、OpenAI、来源集、默认规则的 0/1/2/3 顺序。
# 第二监听绕开前两条目的集合，单独验证来源集合不会误把目的地址命中。
SUFFIXES = (
    "anthropic-com.ghost.io", "anthropic.auth0.com", "anthropic.com",
    "anthropic.com.cdn.cloudflare.net", "clau.de", "claude.ai", "claude.app",
    "claude.com", "claude.dev", "claudemcpclient.com", "claudemcpcontent.com",
    "claudeusercontent.com", "intercom.io", "intercomcdn.com",
    "servd-anthropic-website.b-cdn.net", "statsigapi.net",
)
CASES = [(host, 0) for suffix in SUFFIXES for host in
         (suffix, "a." + suffix, "a.b." + suffix)]
CASES += [(host, 3) for suffix in SUFFIXES for host in
          ("not" + suffix, suffix + ".invalid")]
CASES += [(host, 0) for keyword in ("datadog", "sentry", "sift") for host in
          (keyword + "-probe.invalid", "probe-" + keyword + "-probe.invalid", "probe-" + keyword + ".invalid")]
CASES += [(host, 0) for host in (
    "http-intake.logs.us5.datadoghq.com", "browser-intake-us5-datadoghq.com",
    "api-iam.intercom.io", "widget.intercom.io", "js.intercomcdn.com",
    "downloads.intercomcdn.com", "static.intercomassets.com",
    "cdn.usefathom.com", "fonts.googleapis.com", "fonts.gstatic.com",
    "sentry.io", "a.sentry.io", "a.b.sentry.io", "unrelated.datadoghq.com",
    "a.browser-intake-us5-datadoghq.com", "a.http-intake.logs.us5.datadoghq.com",
    "cdn.anthropic.com", "api.anthropic.com", "mcp.anthropic.com",
    "console.anthropic.com", "workbench.anthropic.com",
)]
CASES += [(host, 1) for host in ("api.github.com", "chatgpt.com", "api.openai.com")]
CASES += [(host, 3) for host in (
    "unmatched.audit-review.invalid", "claude-dev.invalid",
    "unrelated.intercomassets.com", "a.static.intercomassets.com",
    "a.cdn.usefathom.com", "notcdn.usefathom.com", "cdn.usefathom.com.invalid",
    "data-dog.audit-review.invalid", "sen-try.audit-review.invalid", "si-ft.audit-review.invalid",
    "time.apple.com", "time.windows.com", "pool.ntp.org", "0.pool.ntp.org",
    "time.google.com", "time.cloudflare.com", "ntp.aliyun.com", "ntp.org",
)]
# IP 作为 SOCKS 目的地址直接传入，不经 DNS、不连接真实业务目标。
CASES += [
    ("160.79.104.0", 0), ("160.79.105.255", 0),
    ("160.79.106.0", 0), ("160.79.111.255", 0),
    ("160.79.103.255", 3), ("160.79.112.0", 3),
    ("2607:6bc0::", 0), ("2607:6bc0:0:ffff:ffff:ffff:ffff:ffff", 0),
    ("2607:6bc0:1::", 0), ("2607:6bc0:11::", 0),
    ("2607:6bc0:11:ffff:ffff:ffff:ffff:ffff", 0), ("2607:6bc0:12::", 0),
    ("2607:6bc0:ffff:ffff:ffff:ffff:ffff:ffff", 0),
    ("2607:6bbf:ffff:ffff:ffff:ffff:ffff:ffff", 3), ("2607:6bc1::", 3),
]
SOURCE_DIRECTION_CASES = [(host, 3) for host in (
    "160.79.104.0", "160.79.111.255", "160.79.103.255", "160.79.112.0",
    "2607:6bc0::", "2607:6bc0:ffff:ffff:ffff:ffff:ffff:ffff",
)]
assert len(CASES) == len({host for host, index in CASES}) == 146
assert len(SOURCE_DIRECTION_CASES) == 6



def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def recv(sock, count):
    data = b""
    while len(data) < count:
        part = sock.recv(count - len(data))
        if not part:
            raise EOFError("socket closed")
        data += part
    return data


def request(port, host):
    with socket.create_connection(("127.0.0.1", port), timeout=3) as sock:
        sock.sendall(b"\x05\x01\x00")
        assert recv(sock, 2) == b"\x05\x00"
        try:
            address = ipaddress.ip_address(host)
        except ValueError:
            atyp, encoded = 3, bytes([len(host)]) + host.encode()
        else:
            atyp, encoded = (4 if address.version == 6 else 1), address.packed
        sock.sendall(bytes([5, 1, 0, atyp]) + encoded + struct.pack("!H", 443))
        try:
            response = recv(sock, 4)
            return {"connected": response[1] == 0, "reply": response[1], "socks_atyp": atyp}
        except (OSError, EOFError) as error:
            return {"connected": False, "result": type(error).__name__, "socks_atyp": atyp}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    binary, out = args.binary.resolve(), args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    result = {
        "schema": 1,
        "version": "0.1.5",
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "method": "Native sing-box alpha.9 with fixed GitHub release URLs, empty initial cache, default HTTP client and no download_detour; all test business destinations rejected on loopback SOCKS.",
        "boundary": "Actual HTTPS fetch via existing Mac network. No N100, TUN, system DNS/routes/firewall or production configuration/service changes. Does not prove production startup or authenticated product functionality.",
        "script_sha256": sha(pathlib.Path(__file__).read_bytes()),
        "binary_sha256": sha(binary.read_bytes()),
        "binary_version": subprocess.check_output([str(binary), "version"], text=True),
        "assets": {}, "requests": [], "source_direction_requests": [], "passed": False,
    }
    assert "1.15.0-alpha.9" in result["binary_version"]
    assert "132b38e9caaba1a1959354d518e54d2d08419afe" in result["binary_version"]
    assert result["binary_sha256"] == "fcb47f341e6660a35385ceeffc0cebb2daca3fed4d35c729b7d45f7b66555f9a"
    with socket.socket() as primary_reservation, socket.socket() as source_reservation:
        primary_reservation.bind(("127.0.0.1", 0))
        source_reservation.bind(("127.0.0.1", 0))
        port = primary_reservation.getsockname()[1]
        source_port = source_reservation.getsockname()[1]
    cache = out / "cold-cache.db"
    assert not cache.exists()
    sets = [{"type": "remote", "tag": product, "format": "binary", "url": f"https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.5/{product}.srs", "update_interval": "24h"} for product in EXPECTED]
    config = {
        "log": {"level": "debug", "disabled": False, "timestamp": True},
        "dns": {"servers": [{"type": "local", "tag": "bootstrap-dns"}], "final": "bootstrap-dns"},
        "inbounds": [
            {"type": "socks", "tag": "audit-socks", "listen": "127.0.0.1", "listen_port": port},
            {"type": "socks", "tag": "source-audit-socks", "listen": "127.0.0.1", "listen_port": source_port},
        ],
        "outbounds": [{"type": "direct", "tag": "unused-direct"}],
        "http_clients": [{"tag": "bootstrap-http"}],
        "route": {"default_http_client": "bootstrap-http", "default_domain_resolver": "bootstrap-dns", "rule_set": sets, "rules": [
            {"inbound": ["audit-socks"], "rule_set": "anthropic", "action": "reject", "no_drop": True},
            {"inbound": ["audit-socks"], "rule_set": "openai", "action": "reject", "no_drop": True},
            {"rule_set": "anthropic-ip", "action": "reject", "no_drop": True},
            {"action": "reject", "no_drop": True},
        ]},
        "experimental": {"cache_file": {"enabled": True, "path": str(cache.resolve())}},
    }
    config_path, log_path = out / "config.json", out / "runtime.log"
    write(config_path, config)
    checked = subprocess.run([str(binary), "check", "-c", str(config_path)], capture_output=True, text=True)
    result["config_check"] = {"exit": checked.returncode, "stderr": checked.stderr}
    assert checked.returncode == 0, checked.stderr
    child = None
    try:
        with log_path.open("w") as log:
            child = subprocess.Popen([str(binary), "run", "-c", str(config_path)], stdout=log, stderr=subprocess.STDOUT)
            deadline = time.monotonic() + 120
            while child.poll() is None and time.monotonic() < deadline and "sing-box started" not in log_path.read_text():
                time.sleep(.1)
            trace = log_path.read_text()
            assert child.poll() is None and "sing-box started" in trace, trace
            result["native_started"] = True
            for inbound, request_port, cases, result_key in (
                ("audit-socks", port, CASES, "requests"),
                ("source-audit-socks", source_port, SOURCE_DIRECTION_CASES, "source_direction_requests"),
            ):
                for host, index in cases:
                    offset = log_path.stat().st_size
                    response = request(request_port, host)
                    time.sleep(.05)
                    trace = re.sub(r"\x1b\[[0-9;]*m", "", log_path.read_bytes()[offset:].decode("utf-8", errors="replace"))
                    matches = [{"index": int(i), "description": desc} for i, desc in re.findall(r"router: match\[(\d+)\] (.*)", trace)]
                    expected_description = [
                        "inbound=audit-socks rule_set=anthropic => reject",
                        "inbound=audit-socks rule_set=openai => reject",
                        "rule_set=anthropic-ip => reject", "=> reject",
                    ][index]
                    destination = f"[{host}]:443" if ":" in host else f"{host}:443"
                    inbound_seen = f"inbound/socks[{inbound}]: inbound connection to {destination}" in trace
                    row = {"host": host, "inbound": inbound, "expected_index": index, "inbound_host_logged": inbound_seen, "matches": matches, **response}
                    result[result_key].append(row)
                    # 拒绝本身不证明匹配正确：同时核验本请求入口、主机和唯一规则索引及描述。
                    assert not response["connected"] and inbound_seen, row
                    try:
                        address = ipaddress.ip_address(host)
                    except ValueError:
                        expected_atyp = 3
                    else:
                        expected_atyp = 4 if address.version == 6 else 1
                    assert response["socks_atyp"] == expected_atyp, row
                    assert matches == [{"index": index, "description": expected_description}], row
            result["primary_request_count"] = len(result["requests"])
            result["source_direction_request_count"] = len(result["source_direction_requests"])
            assert result["primary_request_count"] == len(CASES) == 146
            assert result["source_direction_request_count"] == len(SOURCE_DIRECTION_CASES) == 6
            assert sum(row["socks_atyp"] == 3 for row in result["requests"]) == 131
            assert sum(row["socks_atyp"] == 4 for row in result["requests"]) == 9
            assert sum(row["socks_atyp"] == 1 for row in result["requests"]) == 6
            assert child.poll() is None, "探测期间原生进程提前退出"
    finally:
        if child is not None:
            if child.poll() is None:
                child.terminate()
            try:
                child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait(timeout=5)
            result["process"] = {"pid": child.pid, "exited": child.poll() is not None, "exit": child.returncode}
        result["listeners"] = []
        for inbound, listening_port in (("audit-socks", port), ("source-audit-socks", source_port)):
            with socket.socket() as sock:
                sock.settimeout(.2)
                result["listeners"].append({"inbound": inbound, "host": "127.0.0.1", "port": listening_port, "closed": sock.connect_ex(("127.0.0.1", listening_port)) != 0})
        result["config_sha256"] = sha(config_path.read_bytes())
        result["runtime_log_sha256"] = sha(log_path.read_bytes())
        write(out / "results.json", result)
    assert result["process"]["exited"] and result["process"]["exit"] == 0 and all(listener["closed"] for listener in result["listeners"]), result
    cached = cache.read_bytes()
    native_log = re.sub(r"\x1b\[[0-9;]*m", "", log_path.read_text())
    for item in sets:
        product = item["tag"]
        with urllib.request.urlopen(item["url"], timeout=30) as response:
            data = response.read(2 * 1024 * 1024 + 1)
            assert len(data) <= 2 * 1024 * 1024, "发行制品超出探测大小上限"
            asset = {"url": item["url"], "http_status": response.status, "final_hostname": urllib.parse.urlparse(response.url).hostname, "bytes": len(data), "sha256": sha(data)}
        assert asset["http_status"] == 200 and asset["sha256"] == EXPECTED[product], asset
        asset["cache_contains_complete_expected_srs"] = data in cached
        assert asset["cache_contains_complete_expected_srs"], product
        asset["native_update_logged"] = bool(re.search(r"router: updated rule-set " + product + r"(?:\n|$)", native_log))
        assert asset["native_update_logged"], native_log
        (out / (product + ".srs")).write_bytes(data)
        result["assets"][product] = asset
    result["cache_sha256"] = sha(cached)
    result["config_sha256"] = sha(config_path.read_bytes())
    result["runtime_log_sha256"] = sha(log_path.read_bytes())
    result["passed"] = True
    write(out / "results.json", result)
    print(json.dumps({"passed": True, "primary_requests": len(result["requests"]), "source_direction_requests": len(result["source_direction_requests"]), "assets": result["assets"], "results": str(out / "results.json")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
