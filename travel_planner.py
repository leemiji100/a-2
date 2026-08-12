import os
import json
import argparse
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
import requests

# 환경변수 로드
load_dotenv()

# API 키 설정
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# 결과 저장 폴더
RESULTS_DIR = "results"
if not os.path.exists(RESULTS_DIR):
    os.makedirs(RESULTS_DIR)


def validate_date(date_str):
    """날짜 검증 함수"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if date_obj < datetime.now():
            return False, "과거 날짜는 선택할 수 없습니다."
        return True, date_obj
    except ValueError:
        return False, "날짜 형식이 잘못되었습니다. (YYYY-MM-DD)"


def get_travel_recommendations(travel_date, errors_list):
    """Gemini API를 통해 여행지 추천받기"""
    prompt = f"""
    당신은 한국 국내 여행 전문가입니다.
    
    여행 날짜: {travel_date}
    
    다음 조건에 맞는 국내 여행지 3곳을 추천해주세요:
    1. 각 여행지의 이름
    2. 추천 이유 (100자 이내)
    3. 주요 관광지 2-3곳
    4. 예상 비용 (1인 기준, 숙박 제외)
    
    JSON 형식으로 응답해주세요:
    {{
        "recommendations": [
            {{
                "city": "도시명",
                "reason": "추천 이유",
                "attractions": ["관광지1", "관광지2", "관광지3"],
                "estimated_cost": "예상 비용"
            }}
        ]
    }}
    
    반드시 유효한 JSON만 응답하세요.
    """

    # API 호출 자체가 계속 실패했을 때도 프로그램이 죽지 않도록 쓸 fallback
    fallback_recommendations = {
        "recommendations": [
            {
                "city": "서울",
                "reason": "수도로서 다양한 문화와 관광지 보유",
                "attractions": ["경복궁", "남산타워", "명동"],
                "estimated_cost": "50만원"
            },
            {
                "city": "부산",
                "reason": "해변 도시로 아름다운 해안 경관",
                "attractions": ["해운대 해수욕장", "광안리", "감천문화마을"],
                "estimated_cost": "60만원"
            },
            {
                "city": "제주도",
                "reason": "자연 경관이 뛰어난 관광지",
                "attractions": ["한라산", "성산일출봉", "협재 해수욕장"],
                "estimated_cost": "80만원"
            }
        ]
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)
            
            # JSON 파싱
            response_text = response.text.strip()
            
            # JSON 코드 블록 제거
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            recommendations = json.loads(response_text)
            return recommendations, errors_list
            
        except json.JSONDecodeError as e:
            error_msg = f"[시도 {attempt + 1}/{max_retries}] JSON 파싱 오류: {str(e)}"
            errors_list.append(error_msg)
            print(f"⚠️  {error_msg}")

            if attempt == max_retries - 1:
                return fallback_recommendations, errors_list

        except Exception as e:
            error_msg = f"[시도 {attempt + 1}/{max_retries}] Gemini API 오류: {str(e)}"
            errors_list.append(error_msg)
            print(f"⚠️  {error_msg}")

            # 마지막 시도까지 API 호출 자체가 실패한 경우에도
            # None을 반환하지 않고 fallback을 반환해 이후 로직이 안전하게 동작하도록 함
            if attempt == max_retries - 1:
                return fallback_recommendations, errors_list

    # 이론상 여기까지 오지 않지만, 방어적으로 fallback 반환
    return fallback_recommendations, errors_list


def search_kakao_place(query):
    """Kakao Local API를 통해 맛집 검색"""
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {
        "query": query,
        "size": 5,
        "sort": "accuracy"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        restaurants = []
        for place in data.get("documents", []):
            restaurants.append({
                "name": place.get("place_name"),
                "address": place.get("address_name"),
                "phone": place.get("phone", "정보 없음"),
                "url": place.get("place_url", "정보 없음")
            })
        
        return restaurants
    
    except Exception as e:
        print(f"⚠️  Kakao API 오류: {str(e)}")
        return []


def generate_travel_report(recommendations, restaurants):
    """최종 여행 리포트 생성"""
    # recommendations가 None이거나 예상한 형태가 아닐 경우를 방어
    if not recommendations or not isinstance(recommendations, dict):
        recommendations = {"recommendations": []}

    report = "# 🌍 AI 기반 국내 여행 추천 리포트\n\n"
    report += f"**생성 날짜:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    report += "## 📍 추천 여행지\n\n"

    rec_list = recommendations.get("recommendations", [])
    if rec_list:
        for i, rec in enumerate(rec_list, 1):
            report += f"### {i}. {rec['city']}\n"
            report += f"**추천 이유:** {rec['reason']}\n\n"
            report += f"**주요 관광지:**\n"
            for attraction in rec.get("attractions", []):
                report += f"- {attraction}\n"
            report += f"\n**예상 비용:** {rec.get('estimated_cost', '정보 없음')}\n\n"
    else:
        report += "여행지 추천 정보를 가져오지 못했습니다.\n\n"

    report += "## 🍽️ 추천 맛집\n\n"
    
    if restaurants:
        for i, restaurant in enumerate(restaurants, 1):
            report += f"### {i}. {restaurant['name']}\n"
            report += f"- **주소:** {restaurant['address']}\n"
            report += f"- **전화:** {restaurant['phone']}\n"
            report += f"- **링크:** {restaurant['url']}\n\n"
    else:
        report += "맛집 정보를 찾을 수 없습니다.\n\n"
    
    report += "---\n"
    report += "*이 리포트는 AI가 생성한 추천입니다. 방문 전 최신 정보를 확인하세요.*\n"
    
    return report


def save_results(recommendations, restaurants, errors_list, travel_date):
    """결과를 파일로 저장"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # JSON 파일 저장
    json_filename = os.path.join(RESULTS_DIR, f"travel_data_{timestamp}.json")
    json_data = {
        "travel_date": travel_date,
        "recommendations": recommendations,
        "restaurants": restaurants,
        "errors": errors_list,
        "generated_at": datetime.now().isoformat()
    }
    
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON 파일 저장: {json_filename}")
    
    # Markdown 파일 저장
    report = generate_travel_report(recommendations, restaurants)
    md_filename = os.path.join(RESULTS_DIR, f"travel_report_{timestamp}.md")
    
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"✅ Markdown 파일 저장: {md_filename}")


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description="AI 기반 국내 여행 추천 프로그램")
    parser.add_argument("--date", type=str, required=True, help="여행 날짜 (YYYY-MM-DD)")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🌍 AI 기반 국내 여행 추천 프로그램")
    print("=" * 60)
    print(f"여행 날짜: {args.date}\n")
    
    # 날짜 검증
    is_valid, result = validate_date(args.date)
    if not is_valid:
        print(f"❌ 오류: {result}")
        return
    
    travel_date = result.strftime("%Y-%m-%d")
    errors_list = []
    
    # [1/4] API 키 확인
    print("[1/4] API 키 확인 중...")
    if not GEMINI_API_KEY or not KAKAO_API_KEY:
        print("❌ API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")
        return
    print("✅ API 키 확인 완료\n")
    
    # [2/4] 날짜 검증
    print("[2/4] 날짜 검증 중...")
    print(f"✅ 날짜 검증 완료\n")
    
    # [3/4] 1차 여행지 추천
    print("[3/4] 1차 여행지 추천 중...")
    recommendations, errors_list = get_travel_recommendations(travel_date, errors_list)
    if recommendations:
        for rec in recommendations.get("recommendations", []):
            print(f"✅ 추천 지역: {rec['city']}")
    print()
    
    # [4/4] 맛집 검색
    print("[4/4] 맛집 검색 중...")
    if recommendations and recommendations.get("recommendations"):
        city = recommendations["recommendations"][0].get("city", "서울")
    else:
        city = "서울"

    query = f"{city} 맛집"
    restaurants = search_kakao_place(query)
    if restaurants:
        print(f"✅ {len(restaurants)}개 맛집 검색 완료")
    print()
    print()
    
    # 결과 저장
    save_results(recommendations, restaurants, errors_list, travel_date)
    
    print("=" * 60)
    print("✨ 프로그램 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()
