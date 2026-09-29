# Retail Replenishment Asset Graph

[Faiz Elahi](https://www.linkedin.com/in/faizilahi) — [pendataco.com](https://pendataco.com) — [github.com/faizilahi](https://github.com/faizilahi)

Synthetic data only. No vendor-customer employment claim.

A Dagster-style asset graph builds store-SKU replenishment proposals. The
`2024-W37` partition failed its freshness check when on-hand inventory landed
6 hours late, while demand still computed — proposals would have understated
need by **1,284** units.

## Assets

`raw_pos` → `demand_28d` → `on_hand` → `replenishment_proposal` with explicit
deps in `src/assets.py`.

## The partition

Partition key `2024-W37` (Mon 2024-09-09). Generator plants POS and on-hand for
40 stores × 25 SKUs.

## The check that failed

Asset check `on_hand_fresh_within_2h` failed: inventory file timestamp was
`08:12Z` vs partition close `02:00Z` + 2h SLA. Gate blocked materialization;
after a late refresh, proposals total **56,193** units (vs unsafe late-file **57,193**).

```powershell
pip install -r requirements.txt
python scripts/generate_synthetic_data.py
python src/run_assets.py
```
