"""Native fixed-tag remote SRS cold start; no production/system changes."""
import datetime
import hashlib
import json
import pathlib
import re
import socket
import struct
import subprocess
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = pathlib.Path(__file__).resolve().parent
BIN = ROOT / ".tools/sing-box"
EXPECTED = {
    "openai": "a910767e3f07dfe89e2f72639960612872361d9ae1c8553ddd4a59c8f154778f",
    "anthropic": "864149211a66da97603b62367f19209e5de2e1b52905faee503501fc37a4c08b",
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
    out = BASE / (sys.argv[1] if len(sys.argv) > 1 else "run")
    out.mkdir(exist_ok=False)
    result = {
        "schema": 1,
        "version": "0.1.1",
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "method": "Native sing-box alpha.9 with fixed GitHub release URLs, empty initial cache, default HTTP client and no download_detour; all test business destinations rejected on loopback SOCKS.",
        "boundary": "Actual HTTPS fetch via existing Mac network. No N100, TUN, system DNS/routes/firewall or production configuration/service changes. Does not prove production startup or authenticated product functionality.",
        "binary_sha256": sha(BIN.read_bytes()),
        "binary_version": subprocess.check_output([str(BIN), "version"], text=True),
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
    sets = [{"type": "remote", "tag": product, "format": "binary", "url": f"https://github.com/YouM1225-1/sing-box-ai/releases/download/v0.1.1/{product}.srs", "update_interval": "24h"} for product in EXPECTED]
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
    checked = subprocess.run([str(BIN), "check", "-c", str(config_path)], capture_output=True, text=True)
    result["config_check"] = {"exit": checked.returncode, "stderr": checked.stderr}
    assert checked.returncode == 0, checked.stderr
    child = None
    try:
        with log_path.open("w") as log:
            child = subprocess.Popen([str(BIN), "run", "-c", str(config_path)], stdout=log, stderr=subprocess.STDOUT)
            deadline = time.monotonic() + 120
            while child.poll() is None and time.monotonic() < deadline and "sing-box started" not in log_path.read_text():
                time.sleep(.1)
            trace = log_path.read_text()
            assert child.poll() is None and "sing-box started" in trace, trace
            result["native_started"] = True
            for host, index in [("api.github.com", 0), ("fonts.googleapis.com", 1), ("unmatched.audit-review.invalid", 2)]:
                offset = log_path.stat().st_size
                response = request(port, host)
                time.sleep(.05)
                trace = re.sub(r"\x1b\[[0-9;]*m", "", log_path.read_text()[offset:])
                matches = [{"index": int(i), "description": desc} for i, desc in re.findall(r"router: match\[(\d+)\] (.*)", trace)]
                row = {"host": host, "expected_index": index, "matches": matches, **response}
                result["requests"].append(row)
                assert not response["connected"] and matches and matches[-1]["index"] == index, row
                assert "reject" in matches[-1]["description"], row
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
        write(out / "results.json", result)
    assert result["process"]["exited"] and result["listener"]["closed"], result
    cached = cache.read_bytes()
    native_log = re.sub(r"\x1b\[[0-9;]*m", "", log_path.read_text())
    for item in sets:
        product = item["tag"]
        with urllib.request.urlopen(item["url"], timeout=30) as response:
            data = response.read(2 * 1024 * 1024)
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
