"""验证固定 v0.1.2 GitHub 制品的真实空缓存加载；仅回环业务探测。"""
import argparse
import datetime
import hashlib
import json
import pathlib
import re
import socket
import struct
import subprocess
import time
import urllib.parse
import urllib.request

EXPECTED = {
    "openai": "a910767e3f07dfe89e2f72639960612872361d9ae1c8553ddd4a59c8f154778f",
    "anthropic": "c6a885e65031be291cf2b3c09170bbdb1ef5aa1eb1bc18003cf1dc07bb196a80",
}


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
        sock.sendall(b"\x05\x01\x00\x03" + bytes([len(host)]) + host.encode() + struct.pack("!H", 443))
        try:
            response = recv(sock, 4)
            return {"connected": response[1] == 0, "reply": response[1]}
        except (OSError, EOFError) as error:
            return {"connected": False, "result": type(error).__name__}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    binary, out = args.binary.resolve(), args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    result = {
        "schema": 1,
        "version": "0.1.2",
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "method": "Native sing-box alpha.9 with fixed GitHub release URLs, empty initial cache, default HTTP client and no download_detour; all test business destinations rejected on loopback SOCKS.",
        "boundary": "Actual HTTPS fetch via existing Mac network. No N100, TUN, system DNS/routes/firewall or production configuration/service changes. Does not prove production startup or authenticated product functionality.",
        "script_sha256": sha(pathlib.Path(__file__).read_bytes()),
        "binary_sha256": sha(binary.read_bytes()),
        "binary_version": subprocess.check_output([str(binary), "version"], text=True),
        "assets": {}, "requests": [], "passed": False,
    }
    assert "1.15.0-alpha.9" in result["binary_version"]
    assert "132b38e9caaba1a1959354d518e54d2d08419afe" in result["binary_version"]
    assert result["binary_sha256"] == "fcb47f341e6660a35385ceeffc0cebb2daca3fed4d35c729b7d45f7b66555f9a"
    with socket.socket() as reservation:
        reservation.bind(("127.0.0.1", 0))
        port = reservation.getsockname()[1]
    cache = out / "cold-cache.db"
    assert not cache.exists()
    sets = [{"type": "remote", "tag": product, "format": "binary", "url": f"https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.2/{product}.srs", "update_interval": "24h"} for product in EXPECTED]
    config = {
        "log": {"level": "debug", "disabled": False, "timestamp": True},
        "dns": {"servers": [{"type": "local", "tag": "bootstrap-dns"}], "final": "bootstrap-dns"},
        "inbounds": [{"type": "socks", "tag": "audit-socks", "listen": "127.0.0.1", "listen_port": port}],
        "outbounds": [{"type": "direct", "tag": "unused-direct"}],
        "http_clients": [{"tag": "bootstrap-http"}],
        "route": {"default_http_client": "bootstrap-http", "default_domain_resolver": "bootstrap-dns", "rule_set": sets, "rules": [{"rule_set": product, "action": "reject", "no_drop": True} for product in EXPECTED] + [{"action": "reject", "no_drop": True}]},
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
            cases = [
                ("api.github.com", 0), ("fonts.googleapis.com", 1),
                ("claude.dev", 1), ("a.claude.dev", 1), ("a.b.claude.dev", 1),
                ("notclaude.dev", 2), ("claude.dev.invalid", 2),
                ("a.claude.dev.invalid", 2), ("claude-dev.invalid", 2),
                ("unmatched.audit-review.invalid", 2),
            ]
            for host, index in cases:
                offset = log_path.stat().st_size
                response = request(port, host)
                time.sleep(.05)
                trace = re.sub(r"\x1b\[[0-9;]*m", "", log_path.read_bytes()[offset:].decode("utf-8", errors="replace"))
                matches = [{"index": int(i), "description": desc} for i, desc in re.findall(r"router: match\[(\d+)\] (.*)", trace)]
                expected_description = ["rule_set=openai => reject", "rule_set=anthropic => reject", "=> reject"][index]
                inbound_seen = "inbound connection to " + host + ":443" in trace
                row = {"host": host, "expected_index": index, "inbound_host_logged": inbound_seen, "matches": matches, **response}
                result["requests"].append(row)
                # 拒绝响应本身不能证明命中产品；必须关联本请求主机和唯一规则索引。
                assert not response["connected"] and inbound_seen, row
                assert matches == [{"index": index, "description": expected_description}], row
            assert len(result["requests"]) == len(cases) == 10
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
        with socket.socket() as sock:
            sock.settimeout(.2)
            result["listener"] = {"host": "127.0.0.1", "port": port, "closed": sock.connect_ex(("127.0.0.1", port)) != 0}
        result["config_sha256"] = sha(config_path.read_bytes())
        result["runtime_log_sha256"] = sha(log_path.read_bytes())
        write(out / "results.json", result)
    assert result["process"]["exited"] and result["process"]["exit"] == 0 and result["listener"]["closed"], result
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
    print(json.dumps({"passed": True, "requests": len(result["requests"]), "assets": result["assets"], "results": str(out / "results.json")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
