print("실험 스크립트 시작")

from pathlib import Path
import pandas as pd
import numpy as np

BASE = Path(__file__).resolve().parents[1]  # backend 기준 상위
DATA = BASE / "data"

df = pd.read_csv(DATA / "demo_observations.csv", parse_dates=["timestamp"])

# 날짜 기준 train / test 분할 (처음 5일 vs 나머지)
df["date"] = df["timestamp"].dt.date
unique_dates = sorted(df["date"].unique())
split_point = unique_dates[4]  # 0~4번째까지 train, 이후 test

train = df[df["date"] <= split_point].copy()
test = df[df["date"] > split_point].copy()

# ---------- 모델 A: 요일×시간 평균 ----------
for d in (train, test):
    d["dow"] = d["timestamp"].dt.dayofweek
    d["hour"] = d["timestamp"].dt.hour

avg_table = (
    train
    .groupby(["location_id", "dow", "hour"])["count"]
    .mean()
    .rename("pred_A")
)

test = test.join(
    avg_table,
    on=["location_id", "dow", "hour"]
)

# 결측(pred_A 없는 경우)은 간단히 전체 평균으로 대체
test["pred_A"].fillna(train["count"].mean(), inplace=True)

# ---------- 모델 B: 이동평균(직전 3타임) ----------
test = test.sort_values(["location_id", "timestamp"])
# train+test를 이어서 rolling 계산 후 test 구간만 평가
all_df = pd.concat([train, test]).sort_values(["location_id", "timestamp"])

all_df["pred_B"] = (
    all_df
    .groupby("location_id")["count"]
    .rolling(window=3)
    .mean()
    .shift(1)   # 이전 값들로만 예측
    .reset_index(level=0, drop=True)
)

# 다시 test 구간만 추출
test = all_df[all_df["date"].isin(test["date"].unique())].copy()
test["pred_B"].fillna(train["count"].mean(), inplace=True)

# ---------- 지표 계산 ----------
def mae(y, yhat):
    return np.mean(np.abs(y - yhat))

def rmse(y, yhat):
    return np.sqrt(np.mean((y - yhat) ** 2))

y_true = test["count"].values
mae_A = mae(y_true, test["pred_A"].values)
rmse_A = rmse(y_true, test["pred_A"].values)

mae_B = mae(y_true, test["pred_B"].values)
rmse_B = rmse(y_true, test["pred_B"].values)

result = pd.DataFrame(
    {
        "Model": ["요일×시간 평균", "3포인트 이동평균"],
        "MAE": [mae_A, mae_B],
        "RMSE": [rmse_A, rmse_B],
    }
)

print(result)
result.to_csv(BASE / "experiment_baselines_result.csv", index=False)
print("Saved:", DATA / "experiment_baselines_result.csv")
