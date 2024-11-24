import os
import sys
import json
import urllib.request

def load_account_info(file_path):
    account_info = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            account_info[key] = value
    return account_info

def load_request_body(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

account_file = "/trend_alimi/.env"
body_file = "/trend_alimi/backend/body.json"
output_file = "/trend_alimi/backend/result.json"

# 계정 정보와 요청 데이터 불러오기
account_info = load_account_info(account_file)
client_id = account_info['CLIENT_ID']
client_secret = account_info['CLIENT_SECRET']
body = load_request_body(body_file)

# 요청 설정
url = "https://openapi.naver.com/v1/datalab/search";
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
request.add_header("Content-Type","application/json")

# JSON 데이터를 문자열로 변환
data = json.dumps(body).encode("utf-8")

# API 호출
response = urllib.request.urlopen(request, data=data)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    result = response_body.decode('utf-8')

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(json.loads(result), file, ensure_ascii=False, indent=4)
    print(f"Result saved to {output_file}")
else:
    print("Error Code:" + rescode)