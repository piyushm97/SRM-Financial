from pathlib import Path
from collections import Counter

RET_PATH = Path("server/src/daily-returns.log")
OUT_PATH = Path("server/src/returns-histogram.csv")

BUCKETS = [-0.05, -0.02, -0.01, 0.0, 0.01, 0.02, 0.05]  # edges

def bucket_for(r):
    for i in range(len(BUCKETS) - 1):
        if BUCKETS[i] <= r < BUCKETS[i + 1]:
            return f"[{BUCKETS[i]:.2f},{BUCKETS[i+1]:.2f})"
    return "out_of_range"

def main():
    if not RET_PATH.exists():
        print("No daily-returns.log.")
        return

    lines = RET_PATH.read_text(encoding="utf-8").strip().splitlines()
    vals = [float(l.split("ret=")[1]) for l in lines]
    counts = Counter(bucket_for(r) for r in vals)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        f.write("bucket,count\n")
        for b in sorted(counts.keys()):
            f.write(f"{b},{counts[b]}\n")
    print("Wrote returns-histogram.csv")

if __name__ == "__main__":
    main()
