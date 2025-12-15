from pathlib import Path
from datetime import datetime

EQ_PATH = Path("server/src/equity-curve.log")
OUT_PATH = Path("server/src/max-drawdown.log")

def main():
    if not EQ_PATH.exists():
        print("No equity-curve.log yet.")
        return

    lines = EQ_PATH.read_text(encoding="utf-8").strip().splitlines()
    if not lines:
        return

    equity = []
    for line in lines:
        parts = line.split(",")
        eq = float(parts[1].split("equity=")[1])
        equity.append(eq)

    peak = equity[0]
    max_dd = 0.0
    for v in equity:
        if v > peak:
            peak = v
        dd = (v - peak) / peak if peak != 0 else 0.0
        if dd < max_dd:
            max_dd = dd

    ts = datetime.utcnow().isoformat()
    line = f"{ts},max_drawdown={max_dd:.4f}\n"
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("a", encoding="utf-8") as f:
        f.write(line)
    print("Appended max drawdown:", line.strip())

if __name__ == "__main__":
    main()
