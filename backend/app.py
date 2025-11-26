from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # CORS 미들웨어 추가를 위한 임포트
import pandas as pd

app = FastAPI(title="CrowdyCampus API", version="0.1.0")
# 허용할 주소 목록 
origins = [
    "https://mibobo-o.github.io",  # 1순위: 깃허브 페이지 주소
    "http://127.0.0.1:5500",    # 2순위: 로컬 테스트용 주소 (VS Code Live Server 등)
    "http://localhost:8000",   # 3순위: (혹시 모를) 로컬 테스트용
    "http://localhost:8001",
    "http://127.0.0.1:8001",
]
# 3. CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_methods=["*"], 
    allow_headers=["*"],
    allow_credentials=True # (분리형 배포 시 자격증명 허용)
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
