from pathlib import Path

EQ_PATH = Path("server/src/equity-curve.log")
OUT_PATH = Path("server/src/daily-drawdown.log")

def main():
    if not EQ_PATH.exists():
        print("No equity-curve.log.")
        return

    lines = EQ_PATH.read_text(encoding="utf-8").strip().splitlines()
    if len(lines) < 2:
        print("Not enough equity data.")
        return

    values = []
    for line in lines:
        ts, rest = line.split(",", 1)
        eq = float(rest.split("equity=")[1])
        values.append((ts, eq))

    peak = max(v for _, v in values)
    ts_last, eq_last = values[-1]
    dd = (eq_last - peak) / peak if peak != 0 else 0.0
    out = f"{ts_last},drawdown_from_peak={dd:.4f}\n"

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("a", encoding="utf-8") as f:
        f.write(out)
    print("Appended daily drawdown:", out.strip())

if __name__ == "__main__":
    main()
