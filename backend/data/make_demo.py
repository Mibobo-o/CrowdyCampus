from pathlib import Path
import pandas as pd
import numpy as np

DATA = Path(__file__).parent
locs = pd.read_csv(DATA/"locations_master.csv")


# 1주일, 30분 간격
idx = pd.date_range("2025-09-08 08:00", periods=7*24*2, freq="30min")
rows = []
rng = np.random.default_rng(42)

required_cols = {"location_id", "category", "capacity"}
if not required_cols.issubset(locs.columns):
    raise ValueError(f"Missing required columns in locations_master.csv: {required_cols - set(locs.columns)}")

hours = idx.hour
for _, r in locs.iterrows():
    base = np.zeros(len(idx), dtype=int)
    # 간단한 패턴: 점심(11~13) 식당↑, 저녁(18~21) 도서관↑
    

    if r["category"] == "cafeteria":
        base += ( (hours>=11) & (hours<=13) ) * rng.integers(120, 260, len(idx))
    elif r["category"] == "reading_room":
        base += ( (hours>=18) & (hours<=21) ) * rng.integers(40, 120, len(idx))
    elif r["category"] == "lecture":
        base += ( (hours>=9) & (hours<=17) ) * rng.integers(10, 60, len(idx))
    else:
        base += rng.integers(0, 20, len(idx))

    # 노이즈 + 수용인원 클리핑
    base = base + rng.integers(0, 15, len(idx))
    base = np.clip(base, 0, int(r["capacity"]))

    for t, c in zip(idx, base):
        rows.append(dict(timestamp=t.isoformat(), location_id=r["location_id"], count=int(c), source="sim"))

df = pd.DataFrame(rows)
df.to_csv(DATA/"demo_observations.csv", index=False)
print("Wrote:", DATA/"demo_observations.csv")
print(df.groupby("location_id")["count"].describe())
