import csv
import json
from openai import OpenAI

# OpenAI API 키 로드 함수
def load_api_key(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("API_KEY"):
                return line.strip().split('=')[1].strip('"')
    raise ValueError("API_KEY not found in .env file.")

# 키워드 로드 함수
def load_keywords(csv_path):
    keywords = []
    with open(csv_path, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if row:  # 빈 줄 방지
                keywords.append(row[0])
    return keywords

# body.json 로드 함수
def load_body_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

# body.json 저장 함수
def save_body_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

# 기존 데이터 초기화 함수
def clear_body_json(body_data):
    body_data['keywordGroups'] = []

# 키워드 추가 함수
def add_keywords_to_body_json(body_data, keywords):
    for keyword_pair in keywords:
        korean_keyword, english_keyword = keyword_pair.split(" (")  # "위키드 (Wicked)" 형식 처리
        english_keyword = english_keyword.rstrip(")")
        body_data['keywordGroups'].append({
            "groupName": korean_keyword.strip(),
            "keywords": [korean_keyword.strip(), english_keyword.strip()]
        })

# 파일 경로 설정
keyword_file_path = "/trend_alimi/backend/keyword.csv"
body_json_path = "/trend_alimi/backend/body.json"

# 키워드 목록 로드
keywords = load_keywords(keyword_file_path)

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=load_api_key("/trend_alimi/.env"))

# GPT 모델 호출
response = client.chat.completions.create(
    model="gpt-4o-mini",  # 사용할 모델 이름
    messages=[
        {
            "role": "system",
            "content": (
                "From the following list of keywords, identify 5 keywords that have potential for branding or commercialization. "
                "Focus on keywords that could represent a product, service, entertainment content, event, or any intellectual property that could be uniquely marketed. "
                "If there are similar or closely related keywords, select only one that is most suitable for branding and exclude the others. "
                "Return the selected keywords strictly in the following format: '한글 키워드 (영문 키워드)'. Ensure there is no additional text or explanation."
            ),
        },
        {"role": "user", "content": f"Keywords:\n{', '.join(keywords)}"}
    ]
)

# 응답에서 추출된 키워드 가져오기
response_content = response.choices[0].message.content
selected_keywords = []
for line in response_content.split('\n'):
    if line.strip():  # 빈 줄 방지
        selected_keywords.append(line.strip())

# 기존 body.json 로드
body_data = load_body_json(body_json_path)

# 기존 groupName과 keywords 내용 삭제
clear_body_json(body_data)

# 선택된 키워드 추가
add_keywords_to_body_json(body_data, selected_keywords)

# body.json 저장
save_body_json(body_json_path, body_data)

# 최종 결과 출력
print("Updated body.json saved with new keywords:")
print(json.dumps(body_data, ensure_ascii=False, indent=4))
