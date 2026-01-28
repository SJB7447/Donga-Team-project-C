# AI Content Factory - 실행 가이드

1단계 필수 기능 구현이 완료되었습니다.

## 1. 환경 설정

1. 터미널에서 프로젝트 폴더로 이동:
   ```bash
   cd "d:\programming project\Donga team project\ai_content_factory"
   ```

2. 필수 라이브러리 설치:
   ```bash
   pip install -r requirements.txt
   ```

3. 환경 변수 설정:
   - `.env.example` 파일의 이름을 `.env`로 변경합니다.
   - `.env` 파일을 열고 `OPENAI_API_KEY` 부분에 실제 OpenAI API 키를 입력합니다.

## 2. 실행 방법

1. 서버 실행:
   ```bash
   python app.py
   ```

2. 접속:
   - 웹브라우저를 열고 `http://127.0.0.1:5000` 접속

## 3. 기능 테스트

1. **주제 입력**: 입력창에 기사 주제(예: "2024년 전기차 시장 전망")를 입력합니다.
2. **생성**: "콘텐츠 생성하기" 버튼을 클릭합니다.
3. **결과 확인**: 잠시 후 생성된 기사가 하단에 표시됩니다.

## 기여
- **Backend**: Antigravity
- **Frontend**: Antigravity
