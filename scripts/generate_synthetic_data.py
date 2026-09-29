import pandas as pd, numpy as np
from pathlib import Path
RNG=np.random.default_rng(2)
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"; DATA.mkdir(parents=True, exist_ok=True)
pd.DataFrame({"order_id":range(1,151),"day":RNG.choice(pd.date_range("2024-07-01","2024-07-07"),150),
  "amount":RNG.uniform(5,100,150).round(2)}).to_csv(DATA/"raw_orders.csv",index=False)
print("Wrote dagster raw asset source")

