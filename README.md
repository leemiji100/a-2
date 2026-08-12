# 🌍 AI 기반 국내 여행 추천 프로그램

REST API를 활용하여 **날짜 기반 여행지 추천**, **맛집 검색**, **최종 여행 리포트 생성**을 자동화하는 Python CLI 프로그램입니다.

---

## 📋 프로젝트 개요

### 기능
1. **1차 여행지 추천** (Gemini API)
   - 입력 날짜를 기반으로 국내 추천 도시 제안
   - 해당 시기의 날씨, 행사/축제 정보 제공

2. **맛집 검색** (Kakao Local API)
   - 추천 도시의 맛집 5곳 자동 검색
   - 주소, 카테고리, 좌표, URL 정보 제공

3. **최종 여행 리포트 생성** (Gemini API)
   - 추천 이유, 날씨, 행사, 맛집, 일정을 포함한 Markdown 리포트 생성
   - results/ 폴더에 JSON + Markdown 파일 자동 저장

### 3단계 API 파이프라인
사용자 입력 (날짜)
↓
[Gemini API] 1차 추천 (JSON)
↓
[Kakao Local API] 맛집 검색
↓
[Gemini API] 최종 리포트 생성 (Markdown)
↓
results/ 폴더에 저장

code
📋 복사

---

## 🛠️ 설치 및 실행

### 1. 프로젝트 클론 또는 다운로드
```bash
# 프로젝트 폴더로 이동
cd travel-planner
2. 필수 패키지 설치
bash
📋 복사
pip install -r requirements.txt
requirements.txt 내용:

code
📋 복사
google-genai==0.3.0
requests==2.31.0
python-dotenv==1.0.0
3. API 키 설정
(1) .env 파일 생성
프로젝트 루트 폴더에 .env 파일을 생성하세요:

bash
📋 복사
touch .env
(2) API 키 입력
.env 파일에 다음을 추가하세요:

env
📋 복사
GEMINI_API_KEY=your_gemini_api_key_here
KAKAO_REST_API_KEY=your_kakao_rest_api_key_here
🔑 API 키 획득 방법
Google Gemini API 키
Google AI Studio 접속
"Create API Key" 클릭
생성된 키를 복사하여 .env에 붙여넣기
Kakao Local API 키
Kakao Developers 접속
로그인 후 "내 애플리케이션" → "앱 만들기"
앱 생성 후 "REST API 키" 복사
.env에 붙여넣기
📖 사용 방법
기본 실행
bash
📋 복사
python travel_planner.py --date "YYYY-MM-DD"
예시
bash
📋 복사
python travel_planner.py --date "2025-03-15"
출력 예시
code
📋 복사
============================================================
🌍 AI 기반 국내 여행 추천 프로그램
============================================================
여행 날짜: 2025-03-15

[1/4] API 키 확인 중...
✅ API 키 확인 완료

[2/4] 날짜 검증 중...
✅ 날짜 검증 완료

[3/4] 1차 여행지 추천 중...
✅ 추천 지역: 제주

[4/4] 맛집 검색 중...
[Kakao API] 상태 코드: 200
[Kakao API] '제주 맛집' 검색 결과: 5건
✅ 맛집 5곳 검색 완료

[5/5] 최종 리포트 생성 중...
✅ 최종 리포트 생성 완료

[6/6] 결과 저장 중...
[저장] JSON 파일: results/travel_data_20250315_143022.json
[저장] Markdown 파일: results/travel_report_20250315_143022.md
✅ 결과 저장 완료

============================================================
✨ 프로그램 완료!
============================================================
📄 JSON 파일: results/travel_data_20250315_143022.json
📋 Markdown 파일: results/travel_report_20250315_143022.md
============================================================
📁 결과물 확인
생성되는 파일
1. JSON 파일 (travel_data_*.json)
json
📋 복사
{
  "timestamp": "20250315_143022",
  "recommendation": {
    "recommended_city": "제주",
    "weather": "봄날씨로 쾌적함",
    "events": ["제주 벚꽃 축제", "제주 해국제"],
    "reason": "3월은 제주의 봄이 시작되는 시기..."
  },
  "restaurants": [
    {
      "name": "흑돼지 식당",
      "address": "제주시 애월읍...",
      "category": "음식점 > 한식 > 고기구이",
      "url": "https://place.kakao.com/...",
      "x": 126.2345,
      "y": 33.4567
    }
  ],
  "errors": []
}
2. Markdown 파일 (travel_report_*.md)
markdown
📋 복사
# 🌍 제주 여행 계획

## 📍 추천 이유
3월은 제주의 봄이 시작되는 시기로...

## 🌤️ 날씨 정보
봄날씨로 쾌적함

## 🎉 행사/축제
- 제주 벚꽃 축제
- 제주 해국제

## 🍽️ 추천 맛집
- **흑돼지 식당** (음식점 > 한식 > 고기구이)
  주소: 제주시 애월읍...

## 📅 추천 일정
- 오전: 도시 관광
- 오후: 맛집 방문
- 저녁: 휴식
🔒 보안 주의사항
⚠️ API 키 유출 방지
1. .env 파일은 절대 Git에 커밋하지 마세요
.gitignore 파일에 추가:

code
📋 복사
.env
*.env
2. 코드에 API 키를 직접 작성하지 마세요
❌ 잘못된 예:

python
📋 복사
GEMINI_API_KEY = "AIzaSyD..."  # 절대 금지!
✅ 올바른 예:

python
📋 복사
from dotenv import load_dotenv
import os

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
3. 결과 파일에 민감한 정보 포함 금지
JSON/Markdown 파일에는 API 키가 저장되지 않습니다.
다른 사람과 결과 파일을 공유할 때 안전합니다.
4. 실수로 유출된 경우
Gemini API: Google Cloud Console에서 키 재생성
Kakao API: Kakao Developers에서 키 재생성
🐛 오류 처리
발생 가능한 오류와 해결 방법
오류	원인	해결 방법
GEMINI_API_KEY가 설정되지 않았습니다	API 키 미설정	.env 파일에 GEMINI_API_KEY 추가
KAKAO_REST_API_KEY가 설정되지 않았습니다	API 키 미설정	.env 파일에 KAKAO_REST_API_KEY 추가
날짜 형식이 올바르지 않습니다	잘못된 날짜 형식	--date "YYYY-MM-DD" 형식 확인
Kakao API 인증 실패 (401/403)	잘못된 API 키	Kakao API 키 재확인
Kakao API 요청 시간 초과	네트워크 문제	인터넷 연결 확인 후 재시도
JSON 파싱 실패	Gemini 응답 형식 오류	프로그램이 자동으로 1회 재시도
오류 기록
모든 오류는 결과 JSON 파일의 errors 배열에 기록됩니다.

📚 학습 목표
이 프로젝트를 완료하면 다음을 이해할 수 있습니다:

1. REST API 이해
HTTP 메서드: GET (조회), POST (생성)의 차이
요청/응답 구조: 헤더, 바디, 상태 코드
인증 방식: API 키를 헤더에 실어 보내는 방식
2. LLM 활용
프롬프트 엔지니어링: JSON 형식 강제, 재시도 로직
구조화된 출력: LLM 결과를 JSON으로 파싱하여 다음 단계 입력으로 활용
에러 핸들링: 파싱 실패 시 재요청
3. API 연동 파이프라인
code
📋 복사
LLM (추천) → 지도 API (검색) → LLM (리포트) → 파일 저장
4. 보안
환경변수 관리: API 키를 코드에 직접 작성하지 않기
.env 파일: 민감한 정보 분리
.gitignore: 실수로 인한 유출 방지
📂 프로젝트 구조
code
📋 복사
travel-planner/
├── travel_planner.py      # 메인 프로그램
├── .env                   # API 키 (Git 무시)
├── .gitignore             # Git 무시 파일 목록
├── requirements.txt       # 필수 패키지
├── README.md              # 이 파일
└── results/               # 결과 저장 폴더 (자동 생성)
    ├── travel_data_*.json
    └── travel_report_*.md
🚀 다음 단계
기능 확장 아이디어
날씨 API 연동: 실제 날씨 데이터 (OpenWeatherMap)
숙박 검색: 호텔/게스트하우스 추천
교통 정보: 대중교통 경로 제안
웹 인터페이스: Flask/FastAPI로 웹 버전 개발
데이터베이스: 여행 기록 저장 및 통계
📞 문제 해결
자주 묻는 질문 (FAQ)
Q: 맛집이 0건으로 나왔습니다.

A: 프로그램이 정상 작동합니다. 검색 결과가 없으면 "데이터 없음"으로 표기되며, 리포트는 계속 생성됩니다.
Q: 같은 날짜로 여러 번 실행하면?

A: 타임스탬프가 다르므로 새로운 파일이 생성됩니다. results/ 폴더에 모두 저장됩니다.
Q: 과거/미래 날짜로 실행해도 되나요?

A: 네, 모든 날짜가 가능합니다. 프로그램은 날짜 형식만 검증합니다.
📄 라이선스
이 프로젝트는 교육 목적으로 자유롭게 사용할 수 있습니다.

✨ 완료!
축하합니다! 🎉 REST API 기반 AI 여행 추천 프로그램이 완성되었습니다.

마지막 확인:

travel_planner.py 작성 완료
.env 파일에 API 키 입력
python travel_planner.py --date "YYYY-MM-DD" 실행 성공
results/ 폴더에 JSON + Markdown 파일 생성 확인
README.md 저장 완료
Happy coding! 🚀

code
📋 복사

---

## ✅ 이제 하세요!

1. **README.md 파일 생성** (프로젝트 루트)
2. 위 내용 복사 & 붙여넣기
3. 저장!

**완료되었나요?** 그럼 최종 테스트를 해봅시다! 🎯
