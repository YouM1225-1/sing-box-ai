"""Download all published assets and compare exact bytes with the validated package."""
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import sys
import urllib.request

base = Path(__file__).resolve().parent
expected = json.loads((base / "package-assets.json").read_text())
mode = sys.argv[1]
assert mode in {"fixed", "latest"}
part = "download/v0.1.12" if mode == "fixed" else "latest/download"
def check(item):
    name, want = item
    url = f"https://github.com/YouM1225-1/sing-box-ai/releases/{part}/{name}"
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read(want["bytes"] + 1)
        status = response.status
    observed = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    assert status == 200 and observed == want, (name, observed, want)
    return name, {**observed, "http_status": status, "url": url, "passed": True}
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    assets = dict(pool.map(check, expected.items()))
result = {"version": "0.1.12", "mode": mode,
          "checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "assets": assets, "passed": True}
(base / (mode + "-downloads.json")).write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"mode": mode, "assets": len(assets), "passed": True}))
