# CrowdyCampus  
실시간 혼잡도 기반 캠퍼스 내 시설 이용 지원 서비스

🔗 **프로젝트 데모 사이트:** https://mibobo-o.github.io/CrowdyCampus/  
🔗 **API 엔드포인트:** https://crowdycampus.onrender.com/
🔗 **Google Slide 발표자료:** https://docs.google.com/presentation/d/1kT-0Ihq9DpSrSw0aV0GT2U61dc3JaqWFjK08vxS59_8/edit?slide=id.p1#slide=id.p1
---

## 📌 프로젝트 개요
**CrowdyCampus**는 캠퍼스 내 주요 건물과 공간의 **혼잡도 정보를 실시간으로 제공**하여  
학생들의 동선 최적화와 시설 이용 효율성을 높이기 위한 웹 서비스입니다.  
건물 위치, 유형, 예상 인원수, 혼잡 비율 등을 한눈에 확인할 수 있으며  
사용자는 보다 편리하게 학습·운동·휴식 공간을 선택할 수 있습니다.

---

## ✨ 주요 기능

### 1. 실시간 지도 기반 UI  
- 캠퍼스 전체 지도를 기반으로 한 직관적 시각화  
- 각 건물에 대한 마커 표시  
- 혼잡도에 따른 색상 변화(Green–Yellow–Red)

### 2. 혼잡도 예측 모델  
- 데모 데이터 기반 시계열 패턴 분석  
- `/predict` API를 통한 실시간 예측값 반환  
- 예상 인원수 / 최대 수용 인원 비교를 통한 혼잡도 계산

### 3. 사용자 경험 기능  
- 자동 재생(시간 흐름에 따른 예측 값 순차 적용)  
- 디버그 툴바(테스트용 UI)  
- 시설 정보 툴팁 및 UI 확장 가능 구조

---

## 🗂 데이터 구조

### `locations_master.csv`
- 캠퍼스 건물 및 시설 정보  
- (건물명, 카테고리, 위도, 경도, 수용 인원)

### `demo_observations.csv`
- 시간대별 방문량 시뮬레이션 데이터  
- 예측 모델(요일 × 시간 평균)에 사용됨

---

## 🧩 기술 스택

### Frontend  
- HTML / CSS / JavaScript  
- Leaflet.js 지도 시각화  
- GitHub Pages 배포

### Backend  
- FastAPI  
- Pandas  
- Uvicorn  
- Render 배포

---

## 🚀 배포 환경  
- **Frontend:** GitHub Pages  
- **Backend:** Render  
- GitHub → Render 자동 배포 적용

---

## 📈 개발 목표 (진행 중)
- 실제 센서 기반 데이터 연동  
- 혼잡도 예측 모델 고도화  
- 모바일 UI 최적화  
- 통계 대시보드 추가  
- 즐겨찾기 및 개인화 기능 확장

---

## 👥 팀 정보  
- **기획 / 프론트엔드 / 백엔드 / 데이터 분석:** 강민주  
- **소속:** 동의대학교 컴퓨터소프트웨어공학과  
- **진행 시기:** 2025년 2학기

---

