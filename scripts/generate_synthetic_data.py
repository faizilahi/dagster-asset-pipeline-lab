from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"; DATA.mkdir(parents=True, exist_ok=True)
RNG = np.random.default_rng(937)
stores = [f"S{i:02d}" for i in range(1, 41)]
skus = [f"K{i:03d}" for i in range(1, 26)]
pos = []
for d in pd.date_range("2024-08-12", "2024-09-08", freq="D"):
    for s in stores:
        for k in skus:
            pos.append({"sale_date": d.strftime("%Y-%m-%d"), "store_id": s, "sku_id": k,
                        "units": int(RNG.integers(0, 12))})
pd.DataFrame(pos).to_csv(DATA / "raw_pos.csv", index=False)
onhand = []
for s in stores:
    for k in skus:
        onhand.append({"store_id": s, "sku_id": k, "on_hand": int(RNG.integers(0, 40)),
                       "as_of_ts": "2024-09-09T08:12:00Z"})
pd.DataFrame(onhand).to_csv(DATA / "on_hand_late.csv", index=False)
# fresh copy
fresh = pd.DataFrame(onhand)
fresh["as_of_ts"] = "2024-09-09T01:30:00Z"
# bump on_hand so proposals differ by 1284 units total target
fresh["on_hand"] = (fresh["on_hand"] + 1).clip(upper=50)
fresh.to_csv(DATA / "on_hand_fresh.csv", index=False)
print("pos", len(pos), "onhand", len(onhand))
