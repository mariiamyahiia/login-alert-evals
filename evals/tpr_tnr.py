import sys

mine = [int(x) for x in sys.argv[1].split(",")]
judge = [int(x) for x in sys.argv[2].split(",")]
if len(mine) != len(judge):
    sys.exit("the two lists must have the same length")

tp = sum(m == 1 and j == 1 for m, j in zip(mine, judge))
fn = sum(m == 1 and j == 0 for m, j in zip(mine, judge))
tn = sum(m == 0 and j == 0 for m, j in zip(mine, judge))
fp = sum(m == 0 and j == 1 for m, j in zip(mine, judge))

print(f"my PASS: {tp + fn}   my FAIL: {tn + fp}")
print(f"judge passed my PASS: {tp}   judge failed my FAIL: {tn}")
print("TPR =", f"{tp}/{tp + fn} = {tp / (tp + fn):.2f}" if tp + fn else "not defined (I labelled no PASS)")
print("TNR =", f"{tn}/{tn + fp} = {tn / (tn + fp):.2f}" if tn + fp else "not defined (I labelled no FAIL)")
print(f"raw agreement = {tp + tn}/{len(mine)}")
