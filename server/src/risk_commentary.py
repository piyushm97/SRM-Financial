from pathlib import Path
from datetime import datetime

ROOT = Path("server/src")
OUT = ROOT / "risk-commentary.txt"

def last_val(path: Path, key: str):
    if not path.exists():
        return None
    line = path.read_text(encoding="utf-8").strip().splitlines()[-1]
    if key not in line:
        return None
    return float(line.split(key + "=")[1].split(",")[0])

def main():
    sharpe = last_val(ROOT / "sharpe-ratio.log", "sharpe_daily")
    mdd = last_val(ROOT / "max-drawdown.log", "max_drawdown")
    now = datetime.utcnow().isoformat()

    parts = [f"Risk commentary at {now}", ""]
    if sharpe is not None:
        parts.append(f"- Daily Sharpe: {sharpe:.3f}")
    if mdd is not None:
        parts.append(f"- Max drawdown: {mdd:.2%}")

    if sharpe is not None and mdd is not None:
        if sharpe > 1 and mdd > -0.2:
            parts.append("- Interpretation: attractive risk-adjusted profile.")
        elif sharpe < 0 and mdd < -0.3:
            parts.append("- Interpretation: weak performance with deep losses.")
        else:
            parts.append("- Interpretation: mixed risk metrics.")
    else:
        parts.append("- Not enough data for interpretation yet.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print("Updated risk-commentary.txt")

if __name__ == "__main__":
    main()
