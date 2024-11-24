import math
import json

# JSON 파일 로드 함수
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

# TV score 계산 함수
def calculate_tv_scores(data, alpha=0.5, delta=7):
    results = []
    
    for item in data['results']:
        title = item['title']
        ratios = item['data']
        tv_scores = []
        
        # S_t 계산
        for i in range(1, len(ratios)):
            S_t = ratios[i]['ratio']
            S_t_minus_1 = ratios[i - 1]['ratio']
            
            # 이전 S_t 계산 (delta만큼 전의 값)
            if i >= delta:
                S_t_delta = ratios[i - delta]['ratio']
            else:
                S_t_delta = None
            
            # TV 계산
            if S_t_delta is not None:
                growth_rate = (S_t - S_t_minus_1) / (S_t_minus_1 + 1)
                exp_decay = math.exp(-alpha * S_t_delta)
                tv_score = growth_rate * exp_decay * 100
            else:
                tv_score = 0  # delta보다 작은 경우
            
            tv_scores.append({
                "period": ratios[i]['period'],
                "tv_score": tv_score
            })
        
        results.append({
            "title": title,
            "tv_scores": tv_scores
        })
    
    return results

# TV score 저장 함수
def save_results_to_json(results, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(results, json_file, ensure_ascii=False, indent=4)

# 파일 경로 설정
input_file = '/trend_alimi/project/crawler/trend_score.json'  # 입력 JSON 파일 경로
output_file = '/trend_alimi/project/crawler/tv_score.json'     # 출력 JSON 파일 경로

# JSON 파일 로드
data = load_json(input_file)

# TV score 계산
tv_scores = calculate_tv_scores(data)

# TV score 저장
save_results_to_json(tv_scores, output_file)

print(f"TV scores have been calculated and saved to {output_file}")
