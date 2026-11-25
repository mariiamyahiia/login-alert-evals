import json
from pathlib import Path

here = Path(__file__).parent
truth = json.loads((here / "truth.json").read_text())
rows, invalid = {}, 0
for line in (here / "outputs.jsonl").read_text().splitlines():
    line = line.strip()
    if not line or line.startswith("```"):
        continue
    try:
        obj = json.loads(line)
        rows[obj["id"]] = obj
    except Exception:
        invalid += 1
        print("INVALID JSON LINE:", line[:70])

print(f"{'id':4} {'label':11} {'truth':11} {'valid':6} {'right':6} {'words':5} {'<=40':5}")
valid_n = right_n = short_n = misses = alarms = 0
for i, t in truth.items():
    o = rows.get(i)
    if o is None:
        print(f"{i:4} MISSING")
        continue
    lab = o.get("label")
    words = len(str(o.get("reason", "")).split())
    valid = lab in ("benign", "suspicious")
    right = lab == t
    valid_n += valid
    right_n += right
    short_n += words <= 40
    misses += (t == "suspicious" and lab == "benign")
    alarms += (t == "benign" and lab == "suspicious")
    print(f"{i:4} {str(lab):11} {t:11} {str(valid):6} {str(right):6} {words:<5} {str(words <= 40):5}")

print()
print("invalid JSON lines:", invalid)
print("allowed label:", valid_n, "/ 16")
print("label matches truth:", right_n, "/ 16")
print("reason <= 40 words:", short_n, "/ 16")
print("MISSES (suspicious called benign):", misses)
print("FALSE ALARMS (benign called suspicious):", alarms)
