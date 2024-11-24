from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# ChromeDriver 경로 설정
chrome_driver_path = "C:/webdriver/chromedriver-win64/chromedriver.exe"

# Selenium 옵션 설정
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Selenium WebDriver 초기화
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Google Trends 페이지 접속
url = "https://trends.google.com/trending?geo=KR&hours=168"
driver.get(url)

# 페이지 로드 대기
time.sleep(5)  # 데이터 로드 완료를 기다림

# 데이터 추출
trends = []
try:
    # 키워드 요소 탐색
    trend_elements = driver.find_elements(By.CLASS_NAME, 'mZ3RIc')  # 키워드 클래스 이름
    for trend in trend_elements:
        try:
            title = trend.text.strip()  # 키워드 추출
            trends.append({'Keyword': title})
        except Exception as e:
            print(f"Error extracting trend: {e}")
except Exception as e:
    print("Failed to fetch trends:", e)

# DataFrame으로 변환
trends_df = pd.DataFrame(trends)

# 출력
print(trends_df)

# DataFrame을 CSV 파일로 저장
output_path = "/trend_alimi/backend/keyword.csv"  # 저장할 파일 경로와 이름
trends_df.to_csv(output_path, index=False, encoding='utf-8-sig')  # 인덱스 제외, UTF-8로 저장
print(f"Data saved to {output_path}")

# 드라이버 종료
driver.quit()
