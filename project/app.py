from flask import Flask, jsonify, render_template
import subprocess
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CRAWLER_FOLDER = os.path.join(BASE_DIR, "crawler")
RESULT_JSON_PATH = os.path.join(CRAWLER_FOLDER, "result.json")

# 실행할 스크립트 목록
SCRIPTS = [
    "keyword.py",
    "keyword_selection.py",
    "trend_score.py",
    "tv_score.py",
    "result.py"
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run-script", methods=["POST"])
def run_script():
    # Python 스크립트 실행
    for script in SCRIPTS:
        script_path = os.path.join(CRAWLER_FOLDER, script)
        try:
            subprocess.run(["python", script_path], check=True)
        except subprocess.CalledProcessError as e:
            return jsonify({"error": f"Error running {script}: {str(e)}"}), 500

    # JSON 파일 읽기
    if not os.path.exists(RESULT_JSON_PATH):
        return jsonify({"error": "Result JSON not found"}), 500

    with open(RESULT_JSON_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    # 현재 날짜와 2주 전 날짜 계산
    today = datetime.now()
    two_weeks_ago = today - timedelta(weeks=2)

    # 필터링: period가 null이 아닌 항목만 처리
    filtered_data = []
    for item in data:
        period = item.get("period")
        if period:  # period가 null이 아닌 경우
            try:
                period_date = datetime.strptime(period, "%Y-%m-%d")  # period를 datetime으로 변환
                if two_weeks_ago <= period_date <= today:  # datetime 객체 간 비교
                    filtered_data.append({
                        "title": item["title"],
                        "max_tv_score": item["max_tv_score"],
                        "period": period  # 추가: period 값을 포함
                    })
            except ValueError:
                # 잘못된 날짜 형식 무시
                continue



    if not filtered_data:
        print(f"DEBUG: No items within the last 2 weeks. Two weeks ago: {two_weeks_ago}, Today: {today}")
    else:
        print(f"DEBUG: Filtered data: {filtered_data}")

    return jsonify(filtered_data)


if __name__ == "__main__":
    app.run(debug=True)
