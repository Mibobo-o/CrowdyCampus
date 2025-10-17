from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI(title="CrowdyCampus API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

BASE = Path(__file__).parent
DATA = BASE / "data"

# 초기 로드
locations = pd.read_csv(DATA/"locations_master.csv")
obs = pd.read_csv(DATA/"demo_observations.csv", parse_dates=["timestamp"])

# 예측용 평균 테이블 (요일×시간)
tmp = obs.assign(dow=obs["timestamp"].dt.dayofweek, hour=obs["timestamp"].dt.hour)
AVG = tmp.groupby(["location_id","dow","hour"])["count"].mean().round().astype(int)

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/locations")
def get_locations():
    return locations.to_dict(orient="records")

@app.get("/predict")
def predict(at: str, location_id: str):
    ts = pd.to_datetime(at)
    key = (location_id, int(ts.dayofweek), int(ts.hour))
    yhat = int(AVG.get(key, 0))
    cap = int(locations.set_index("location_id").loc[location_id, "capacity"])
    ratio = min(yhat / cap, 1.0) if cap else 0.0
    return {
        "location_id": location_id,
        "timestamp": ts.isoformat(),
        "predicted_count": yhat,
        "capacity": cap,
        "congestion_ratio": round(ratio, 3)
    }
