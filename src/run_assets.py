import json, sys
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from assets import demand_28d, replenishment, ASSET_GRAPH
from checks import on_hand_fresh_within_2h
DATA, OUT = ROOT / "data", ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    pos = pd.read_csv(DATA / "raw_pos.csv")
    late = pd.read_csv(DATA / "on_hand_late.csv")
    fresh = pd.read_csv(DATA / "on_hand_fresh.csv")
    dem = demand_28d(pos, "2024-09-08")
    check_late = on_hand_fresh_within_2h(late, "2024-09-09T02:00:00")
    check_fresh = on_hand_fresh_within_2h(fresh, "2024-09-09T02:00:00")
    unsafe = replenishment(dem, late)
    safe = replenishment(dem, fresh)
    dem.to_csv(OUT / "demand_28d.csv", index=False)
    safe.to_csv(OUT / "replenishment_proposal.csv", index=False)
    summary = {
        "assets": list(ASSET_GRAPH),
        "partition": "2024-W37",
        "check_failed": not check_late["passed"],
        "check_detail": check_late,
        "unsafe_units": int(unsafe["propose_units"].sum()),
        "safe_units": int(safe["propose_units"].sum()),
        "unit_gap": int(safe["propose_units"].sum() - unsafe["propose_units"].sum()),
        "fresh_check_passed": check_fresh["passed"],
    }
    pd.DataFrame([summary]).to_csv(OUT / "asset_run_summary.csv", index=False)
    print(json.dumps(summary, indent=2, default=str))
if __name__ == "__main__":
    main()
