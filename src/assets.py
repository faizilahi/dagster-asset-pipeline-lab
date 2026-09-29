from __future__ import annotations
import pandas as pd

ASSET_GRAPH = {
    "raw_pos": [],
    "demand_28d": ["raw_pos"],
    "on_hand": [],
    "replenishment_proposal": ["demand_28d", "on_hand"],
}

def demand_28d(pos: pd.DataFrame, as_of: str) -> pd.DataFrame:
    end = pd.Timestamp(as_of)
    start = end - pd.Timedelta(days=27)
    w = pos[(pos["sale_date"] >= start.strftime("%Y-%m-%d")) & (pos["sale_date"] <= end.strftime("%Y-%m-%d"))]
    g = w.groupby(["store_id", "sku_id"], as_index=False).agg(units_28d=("units", "sum"))
    g["daily_demand"] = (g["units_28d"] / 28).round(2)
    return g

def replenishment(demand: pd.DataFrame, on_hand: pd.DataFrame, cover_days: int = 14) -> pd.DataFrame:
    m = demand.merge(on_hand, on=["store_id", "sku_id"], how="left")
    m["on_hand"] = m["on_hand"].fillna(0)
    m["target"] = (m["daily_demand"] * cover_days).round()
    m["propose_units"] = (m["target"] - m["on_hand"]).clip(lower=0).astype(int)
    return m
