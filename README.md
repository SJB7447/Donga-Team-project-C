# AI Content Factory (팀 프로젝트)

AI 기반 콘텐츠 생성, 자동 저장(Supabase), 그리고 스토리보드 기획까지 지원하는 올인원 플랫폼입니다.

## 🚀 팀원 협업 가이드 (Getting Started)

프로젝트를 다운로드(Clone) 받은 후, 다음 순서대로 세팅해주세요.

### 1. 개발 환경 설정
터미널에서 다음 명령어를 실행하여 필수 라이브러리를 설치합니다.
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정 (중요!)
보안상 `api key`는 깃허브에 올라가지 않습니다.
` .env` 파일을 직접 생성하고, 팀장에게 공유받은 키를 입력해주세요.

1. 프로젝트 최상위 폴더에 `.env` 파일 생성
2. 아래 내용을 복사 후 붙여넣기 (값은 실제 키로 변경)
```ini
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3. 프로젝트 실행
서버를 실행하고 브라우저에서 접속합니다.
```bash
python app.py
```
- 접속 주소: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 📂 프로젝트 구조
- `app.py`: 플라스크 백엔드 서버 (API + 라우팅)
- `templates/index.html`: 프론트엔드 (UI/UX)
- `verify_supabase.py`: DB 연결 테스트 스크립트
- `requirements.txt`: 의존성 패키지 목록

## ✨ 주요 기능
1. **AI 기사 작성**: 주제와 톤 설정에 따른 자동 기사 생성
2. **HTML 내보내기**: 복사 붙여넣기가 가능한 HTML 코드 제공
3. **참고 URL 크롤링**: 외부 링크를 읽고 반영하여 글 작성
4. **스토리보드 기획**: 영상 제작용 씬/대본 자동 구성
5. **히스토리(DB)**: Supabase를 통한 자동 저장 및 기록 열람

## 기여
- **Backend & Frontend**: Antigravity & Team Donga
