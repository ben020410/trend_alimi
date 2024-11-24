import json
from math import ceil

# JSON 파일 경로
file_path = "/trend_alimi/project/crawler/tv_score.json"

# 파일 읽기
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# 결과를 저장할 리스트
result = []

# 각 타이틀에 대해 최댓값과 해당 period 찾기
for item in data:
    title = item["title"]
    tv_scores = item["tv_scores"]
    
    if tv_scores:  # tv_scores가 비어있지 않은 경우
        max_score_entry = max(tv_scores, key=lambda x: x["tv_score"])
        max_score = round(max_score_entry["tv_score"])
        max_period = max_score_entry["period"]
    else:  # tv_scores가 비어있는 경우
        max_score = None
        max_period = None
    
    result.append({"title": title, "max_tv_score": max_score, "period": max_period})

# 결과를 JSON으로 출력
output_file = "/trend_alimi/project/crawler/result.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False, indent=4)

print(f"결과가 '{output_file}'에 저장되었습니다.")