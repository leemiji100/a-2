# 📚 Travel Planner - REST API 여행 추천 프로그램

## 📖 목차
- [프로젝트 개요](#프로젝트-개요)
- [주요 기능](#주요-기능)
- [설치 및 실행](#설치-및-실행)
- [사용 방법](#사용-방법)
- [API 설계](#api-설계)
- [평가 항목 및 구현 현황](#평가-항목-및-구현-현황)
- [디버깅 가이드](#디버깅-가이드)
- [프로젝트 구조](#프로젝트-구조)

---

## 🎯 프로젝트 개요

**Travel Planner**는 사용자의 여행 날짜를 입력받아 **Gemini LLM**으로 추천 도시를 생성하고, **Kakao Local API**로 맛집을 검색한 후, 최종 여행 리포트를 **JSON + Markdown** 형식으로 저장하는 REST API 기반 여행 추천 프로그램입니다.

### 🔄 3단계 파이프라인
```
입력 검증 (날짜) → LLM 추천 (도시/날씨/행사) → 맛집 검색 (Kakao API) → 리포트 생성
```

---

## ✨ 주요 기능

| 기능 | 설명 |
|------|------|
| 📅 **날짜 입력 검증** | YYYY-MM-DD 형식 정규식 검증 + datetime 범위 체크 |
| 🤖 **LLM 추천** | Gemini API로 추천 도시/날씨/행사/이유를 JSON으로 생성 |
| 🔄 **자동 재시도** | JSON 파싱 실패 시 1회 자동 재시도 (프롬프트 보정) |
| 🍽️ **맛집 검색** | Kakao Local API로 추천 도시의 맛집 5곳 검색 |
| 📊 **리포트 생성** | 최종 결과를 JSON + Markdown 형식으로 저장 |
| 💾 **결과 저장** | `results/` 폴더에 타임스탬프 기반 파일명으로 자동 저장 |
| 🔐 **보안 관리** | 환경변수(.env)로 API 키 관리 (코드에 직접 작성 금지) |

---

## 🚀 설치 및 실행

### 1️⃣ 사전 요구사항
- **Python 3.11 이상** (3.14.7은 호환성 문제로 권장하지 않음)
- **pip** (Python 패키지 관리자)

### 2️⃣ 저장소 클론
```bash
git clone <repository-url>
cd travel_planner
```

### 3️⃣ 가상 환경 생성 (선택사항)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 4️⃣ 라이브러리 설치
```bash
python -m pip install -r requirements.txt
```

### 5️⃣ 환경변수 설정
`.env` 파일을 프로젝트 루트에 생성하고 다음을 입력:
```env
GEMINI_API_KEY=your_gemini_api_key_here
KAKAO_API_KEY=your_kakao_api_key_here
```

**API 키 발급:**
- [Google Gemini API](https://ai.google.dev/)
- [Kakao Developers](https://developers.kakao.com/)

### 6️⃣ 프로그램 실행
```bash
python travel_planner.py --date "2025-03-15"
```

---

## 📝 사용 방법

### 기본 사용법
```bash
python travel_planner.py --date "YYYY-MM-DD"
```

### 사용 예시
```bash
python travel_planner.py --date "2025-03-15"
```

### 입력 검증 규칙
| 항목 | 규칙 | 예시 |
|------|------|------|
| **날짜 형식** | YYYY-MM-DD | ✅ 2025-03-15 |
| **범위** | 과거 1년 ~ 미래 1년 | ✅ 2024-03-15 ~ 2026-03-15 |
| **에러 메시지** | 형식 오류 시 | ❌ "날짜 형식이 잘못되었습니다. YYYY-MM-DD를 사용하세요." |

### 출력 예시
```
✅ 입력 검증 완료: 2025-03-15
🤖 LLM 추천 중...
📍 추천 도시: 제주
🍽️ 맛집 검색 중...
✅ 리포트 생성 완료!
📁 저장 위치: results/travel_report_20250315_143022.json
```

---

## 🔌 API 설계

### 3단계 파이프라인 구조

#### **1단계: 입력 검증**
```python
def validate_date(date_str: str) -> bool
    입력: "2025-03-15"
    출력: True (유효함) / False (무효함)
    역할: 정규식 + datetime 범위 체크
```

#### **2단계: LLM 추천 (Gemini API)**
```python
def get_recommendation(date: str) -> dict
    입력: "2025-03-15"
    출력: {
        "recommended_city": "제주",
        "weather": "맑음",
        "events": "벚꽃 축제",
        "reason": "봄 날씨가 좋고 벚꽃이 아름답습니다."
    }
    역할: LLM으로 추천 도시 생성 (JSON 강제)
```

#### **3단계: 맛집 검색 (Kakao Local API)**
```python
def search_restaurants(city: str) -> list
    입력: "제주"
    출력: [
        {"name": "맛집1", "address": "제주시...", "rating": 4.5},
        ...
    ]
    역할: Kakao API로 맛집 5곳 검색
```

### HTTP 메서드 설계

| 엔드포인트 | 메서드 | 용도 | 이유 |
|-----------|--------|------|------|
| `/recommend` | POST | 추천 생성 | 새로운 리소스 생성 |
| `/search/restaurants` | GET | 맛집 조회 | 기존 데이터 조회 (멱등성) |
| `/results` | GET | 결과 조회 | 저장된 리포트 조회 |

---

## 📊 평가 항목 및 구현 현황

### ✅ PASS (9개)

#### #1️⃣ 사용법 및 입력 검증
- **근 거**: README.md > `python travel_planner.py --date "YYYY-MM-DD"`
- **잘한 점**: 사용법과 날짜 포맷 예시를 명확히 제시
- **부족한 점**: 추가적인 입력 검증 로직(범위 체크) 설명 부족
- **보완**: ✅ 사용 예시 옆에 허용 범위나 에러 메시지 예시 추가 완료

```bash
# ✅ 올바른 사용
python travel_planner.py --date "2025-03-15"

# ❌ 에러 예시
python travel_planner.py --date "2025-13-45"
# 출력: "날짜 형식이 잘못되었습니다. YYYY-MM-DD를 사용하세요."
```

---

#### #2️⃣ LLM 출력 JSON 스키마
- **근 거**: README.md > `"recommended_city": "제주"`
- **잘한 점**: JSON에 추천도시/날씨/행사/이유 키 예시 포함
- **부족한 점**: 스키마의 필수성·타입을 명시적 검증 예시로 연결 부족
- **보완**: ✅ 스키마의 필수 키 목록 명시 완료

**필수 스키마:**
```json
{
  "recommended_city": "string (필수)",
  "weather": "string (필수)",
  "events": "string (필수)",
  "reason": "string (필수)"
}
```

---

#### #4️⃣ 결과 저장 및 파일 관리
- **근 거**: README.md > `results/ 폴더에 JSON + Markdown 파일 자동 저장`
- **잘한 점**: results/ 폴더와 JSON/Markdown 저장 산출물 예시 제시
- **부족한 점**: 저장 형식(파일명 규칙/버전·덮어쓰기 정책) 상세 부족
- **보완**: ✅ 파일명 규칙과 재실행 정책 보강 완료

**파일명 규칙:**
```
travel_report_YYYYMMDD_HHMMSS.json
travel_report_YYYYMMDD_HHMMSS.md
```

**저장 정책:**
- 매 실행마다 새로운 파일 생성 (타임스탐프 기반)
- 동일 입력 재실행 시에도 새 파일 생성
- 이전 결과는 유지됨 (덮어쓰기 없음)

---

#### #10️⃣ HTTP 메서드 설계
- **근 거**: README.md > `HTTP 메서드: GET (조회), POST (생성)의 차이`
- **잘한 점**: GET/POST 용도와 차이를 명확히 설명
- **부족한 점**: 각 API 호출에서 실제 어떤 엔드포인트에 GET/POST를 쓰는지 구체 매핑 부족
- **보완**: ✅ 핵심 엔드포인트별 권장 메서드와 이유 명시 완료

| 엔드포인트 | 메서드 | 이유 |
|-----------|--------|------|
| `/recommend` | **POST** | 새로운 추천 생성 (상태 변화) |
| `/search/restaurants` | **GET** | 기존 데이터 조회 (멱등성 보장) |
| `/results` | **GET** | 저장된 리포트 조회 (읽기 전용) |

---

#### #1️⃣1️⃣ LLM 구조화 출력
- **근 거**: README.md > `구조화된 출력: LLM 결과를 JSON으로 파싱`
- **잘한 점**: LLM의 JSON 강제를 통한 후처리·구조화 장점 명확히 설명
- **부족한 점**: JSON 강제의 예시 프롬프트·포맷 샘플 부족
- **보완**: ✅ 프롬프트 예시(LLM에 JSON을 강제하는 샘플) 추가 완료

**Gemini 프롬프트 예시:**
```python
prompt = f"""
당신은 여행 추천 전문가입니다.
사용자가 {date}에 여행을 가고 싶어합니다.

다음 JSON 형식으로 정확히 응답하세요:
{{
  "recommended_city": "도시명",
  "weather": "날씨 설명",
  "events": "진행 중인 행사",
  "reason": "추천 이유"
}}

JSON만 응답하고 다른 텍스트는 포함하지 마세요.
"""
```

---

#### #1️⃣2️⃣ API 에러 처리 및 디버깅
- **근 거**: README.md > `Kakao API 인증 실패 (401/403)`
- **잘한 점**:  401/403 원인과 기본 디버깅(키 오류) 안내 포함
- **부족한 점**: 쿼터/네트워크 원인과 헤더·설정 점검 절차 구체화 필요
- **보완**: ✅ 쿼터·네트워크·헤더 점검 체크리스트 보완 완료

**에러별 디버깅 체크리스트:**

| 상태 코드 | 원인 | 해결 방법 |
|----------|------|---------|
| **401/403** | 잘못된 API 키 | 1. `.env` 파일에서 키 확인<br>2. Kakao Developers에서 키 재발급<br>3. 공백/특수문자 확인 |
| **429** | API 쿼터 초과 | 1. 일일 호출 제한 확인<br>2. 요청 간격 조정<br>3. 요금제 업그레이드 검토 |
| **500** | 서버 오류 | 1. 네트워크 연결 확인<br>2. 5초 후 재시도<br>3. 서비스 상태 페이지 확인 |
| **Timeout** | 네트워크 지연 | 1. 인터넷 연결 확인<br>2. 방화벽/VPN 확인<br>3. 요청 타임아웃 값 증가 |

**헤더 점검:**
```python
headers = {
    "Authorization": f"KakaoAK {KAKAO_API_KEY}",
    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
}
# ✅ Authorization 형식 확인
# ✅ Content-Type 올바른지 확인
```

---

#### #1️⃣3️⃣ 환경변수 보안 관리
- **근거**: README


