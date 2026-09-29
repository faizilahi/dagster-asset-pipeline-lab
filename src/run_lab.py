from pathlib import Path
import pandas as pd, json, time
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"output"; OUT.mkdir(parents=True, exist_ok=True)
assets={}
def materialize(name, fn):
  t=time.time(); df=fn(); path=OUT/f"{name}.csv"; df.to_csv(path,index=False)
  assets[name]={"path":str(path),"rows":len(df),"ts":time.time(),"seconds":round(time.time()-t,3)}
  return df
raw=materialize("raw_orders", lambda: pd.read_csv(ROOT/"data"/"raw_orders.csv"))
staged=materialize("staged_orders", lambda: raw.assign(amount=raw["amount"].astype(float)))
mart=materialize("mart_daily", lambda: staged.groupby("day",as_index=False).agg(orders=("order_id","count"),revenue=("amount","sum")))
mart["revenue"]=mart["revenue"].round(2)
mart.to_csv(OUT/"summary.csv",index=False)
(OUT/"asset_meta.json").write_text(json.dumps(assets,indent=2),encoding="utf-8")
print(mart)

