"""Download only a hash-pinned official compiler into this checkout."""
import hashlib
import io
from pathlib import Path
import platform
import tarfile
import urllib.request

from common import ROOT, compiler, load, need


def main():
    target = ROOT / ".tools/sing-box"
    if target.exists():
        compiler()
        print("Pinned compiler already present")
        return
    machine = {"aarch64": "arm64", "arm64": "arm64", "x86_64": "amd64"}.get(platform.machine())
    key = platform.system().lower() + "-" + str(machine)
    lock = load(ROOT / "tools.lock.json")["sing_box"]
    need(key in lock["platforms"], f"Unsupported bootstrap platform: {key}")
    entry = lock["platforms"][key]
    with urllib.request.urlopen(entry["url"], timeout=60) as response:
        data = response.read(50_000_001)
    need(len(data) <= 50_000_000 and hashlib.sha256(data).hexdigest() == entry["archive_sha256"], "Compiler archive hash mismatch")
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        member = archive.getmember(f"sing-box-{lock['version']}-{key}/sing-box")
        need(member.isfile(), "Compiler archive member is not a file")
        content = archive.extractfile(member).read()
    need(hashlib.sha256(content).hexdigest() == entry["binary_sha256"], "Compiler member hash mismatch")
    target.parent.mkdir(exist_ok=True)
    with target.open("xb") as f:
        f.write(content)
    target.chmod(0o755)
    compiler()
    print(f"Verified official compiler: {key} {lock['version']}")


if __name__ == "__main__":
    main()
