<p align="center">
  <h1 align="center">🕶️ 유행 알림이: 유행 아이템 조기 예측 서비스 📈 </h1>
  <p align="center">
    <h3 align="center">2024-2 WE-Meet 프로젝트 (Text Mining 활용 데이터 분석 및 신사업 아이디어 도출)</h3>
  </p>
</p>
<br>

## 📌 소개
<p align="center">
  <img src="https://github.com/user-attachments/assets/f5514b90-ca37-47b5-9e3e-864d050ca561" width="400"/>
</p>

본 프로젝트는 **Text Mining 활용 데이터 분석 및 신사업 아이디어 도출**의 일환으로, 실시간 검색량을 기반으로 키워드의 유행 정도를 파악하는 서비스입니다.
하단은 2024-11-24을 기준으로 생성된 결과 화면입니다.
<br>
<p align="center">
  <img src="https://github.com/user-attachments/assets/85fb7085-a323-4432-ba22-32794573c325" width="400"/>
</p>
<br>

## 💻 서비스 로직
<p align="center">
  <img src="https://github.com/user-attachments/assets/53267818-4b88-4e64-b30a-23b110d215f5" width="700"/>
</p>

사용자의 POST 요청이 Flask 서버로 전달되면 핵심 로직인 **Python 스크립트**가 실행됩니다. <br>
1. **keyword.py**: selenium 라이브러리를 통해 [Google Trends](https://trends.google.com/trends/)에서 최근 2일 동안의 실시간 인기 키워드를 추출합니다.
2. **keyword_selection.py**: [OpenAI API](https://openai.com/index/openai-api/)를 통해 GPT-4o-mini 모델을 불러오고, 1.에서 추출한 키워드를 선별합니다.
3. **trend_score.py**: [NAVER 데이터랩 API](https://developers.naver.com/products/service-api/datalab/datalab.md)를 통해 2.에서 선별한 키워드의 상대적 검색량을 주 단위로 조회합니다. 본 프로젝트의 목표는 유행 아이템을 탐지하는 것이므로 유행에 민감한 10대, 20대를 타겟으로 조회하였습니다.
4. **tv_score.py**: 3.에서 조회한 주 단위의 상대적 검색량을 **유행 정도에 대한 지표**인 **TV score**로 변환합니다.
5. **result.py**: 4.의 TV score 중 peak가 발생하는 시기와 그 최댓값을 키워드별로 정리합니다.
<br>

## 🛠️ 실행 방법
1. 필요한 **Python 라이브러리**를 설치합니다(`selenium`, `openai`, `urllib` 등).
2. Chrome 버전에 맞는 **ChromeDriver**를 설치하고, `keyword.py`의 `chrome_driver_path` 경로를 알맞게 수정합니다.
3. 루트 경로에 `.env` 파일을 생성하고, 필요한 정보(하단 참고)를 입력합니다.
```bash
CLIENT_ID=<NAVER 데이터랩 키>
CLIENT_SECRET=<NAVER 데이터랩 암호 키>
API_KEY=<OpenAI API 키>
```
4. `app.py`를 실행하고, 터미널에 출력되는 주소로 접속해 서비스를 실행합니다.
5. 필요한 경우, `body.json`의 내용을 수정하여 사용합니다.
