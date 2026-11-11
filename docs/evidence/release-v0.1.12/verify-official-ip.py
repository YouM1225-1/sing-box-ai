"""Independent native checks for official IP coverage, boundaries and direction."""
import argparse
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from common import run, write_json
from validate import harness

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("batch", type=Path)
p.add_argument("--output", type=Path, required=True)
a = p.parse_args()
a.output.mkdir(parents=True, exist_ok=False)
for name in ("openai", "anthropic", "anthropic-ip"):
    for ext in ("json", "srs"):
        shutil.copyfile(a.batch / (name + "." + ext), a.output / (name + "." + ext))
cases = []
def add(artifact, host, direction, expected):
    for ext in ("json", "srs"):
        cases.append({"Name": f"{artifact}:{direction}:{host}", "File": artifact + "." + ext,
                      "Source": host if direction == "source" else "",
                      "Destination": host if direction == "destination" else "", "Want": expected})
voice = json.loads(Path(__file__).with_name("chatgpt-voice.json").read_text())
assert len(voice["prefixes"]) == 423
for row in voice["prefixes"]:
    host = row["ipv4Prefix"].split("/")[0]
    add("openai", host, "destination", True)
    add("openai", host, "source", False)
for host, destination, source in (
    ("153.61.207.255", False, False), ("153.61.208.0", False, True),
    ("153.61.223.255", False, True), ("153.61.224.0", True, False),
    ("153.61.227.255", True, False), ("153.61.228.0", False, False),
):
    for artifact in ("openai", "anthropic", "anthropic-ip"):
        add(artifact, host, "destination", destination if artifact == "anthropic" else False)
        add(artifact, host, "source", source if artifact == "anthropic-ip" else False)
write_json(a.output / "cases.json", cases)
executable, info = harness(ROOT, a.output.resolve(), "go")
output = run([executable, (a.output / "cases.json").resolve()]).stdout
results = [json.loads(line) for line in output.splitlines()]
assert len(results) == len(cases) == 1764 and all(r["pass"] for r in results)
(a.output / "matches.jsonl").write_text(output)
write_json(a.output / "results.json", {"cases": len(cases), "failures": 0, "passed": True, "harness": info})
print(json.dumps({"cases": len(cases), "failures": 0, "passed": True}))
