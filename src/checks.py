from datetime import datetime
import pandas as pd

def on_hand_fresh_within_2h(on_hand: pd.DataFrame, partition_close: str, sla_hours: int = 2) -> dict:
    ts = datetime.fromisoformat(str(on_hand["as_of_ts"].iloc[0]).replace("Z", ""))
    close = datetime.fromisoformat(partition_close)
    age_h = (ts - close).total_seconds() / 3600.0
    # freshness: as_of should be <= close + sla (arrived by SLA)
    # late file has as_of after close+sla
    ok = ts <= close + pd.Timedelta(hours=sla_hours)
    return {"check": "on_hand_fresh_within_2h", "passed": bool(ok), "as_of_ts": str(on_hand["as_of_ts"].iloc[0]),
            "hours_after_close": round(age_h, 2)}
