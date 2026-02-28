# Gmail 전송 설정 가이드

LinkedIn 추천 결과를 Gmail로 자동 전송하려면 아래 단계를 따라주세요.

## 1단계: Python 패키지 설치

터미널에서 실행:

```bash
cd /Users/paddington/Project/practice/01_AI_Native_Camp/.claude/skills/my-context-sync/scripts
pip install -r requirements.txt
```

## 2단계: Google Cloud Console 설정

### 2-1. 프로젝트 생성

1. https://console.cloud.google.com/ 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택

### 2-2. Gmail API 활성화

1. 좌측 메뉴: **API 및 서비스** > **사용 설정된 API 및 서비스**
2. 상단 **+ API 및 서비스 사용 설정** 클릭
3. "Gmail API" 검색 후 선택
4. **사용 설정** 클릭

### 2-3. OAuth 2.0 인증 정보 생성

1. 좌측 메뉴: **API 및 서비스** > **사용자 인증 정보**
2. 상단 **+ 사용자 인증 정보 만들기** > **OAuth 클라이언트 ID** 선택
3. 애플리케이션 유형: **데스크톱 앱** 선택
4. 이름: "LinkedIn Sync" (원하는 이름)
5. **만들기** 클릭
6. **JSON 다운로드** 클릭
7. 다운로드한 파일 이름을 `credentials.json`으로 변경
8. 이 파일을 scripts 폴더에 저장:
   ```
   /Users/paddington/Project/practice/01_AI_Native_Camp/.claude/skills/my-context-sync/scripts/credentials.json
   ```

> ⚠️ **보안 주의:** credentials.json 파일은 개인 인증 정보입니다. Git에 커밋하지 마세요!

## 3단계: 첫 실행 (OAuth 인증)

터미널에서 실행:

```bash
cd /Users/paddington/Project/practice/01_AI_Native_Camp/.claude/skills/my-context-sync/scripts
python gmail_sender.py sync/test.md your-email@gmail.com
```

1. 브라우저가 자동으로 열립니다
2. Google 계정으로 로그인
3. "이 앱은 Google에서 인증하지 않았습니다" 경고가 나오면:
   - **고급** 클릭
   - **LinkedIn Sync(으)로 이동** 클릭
4. 권한 허용 화면에서 **허용** 클릭
5. 인증 완료! `token.pickle` 파일이 자동 생성됩니다

> 다음부터는 token.pickle 파일이 있어서 브라우저 인증 없이 바로 전송됩니다.

## 4단계: 스킬에 통합

스킬 실행 시 자동으로 Gmail 전송이 되도록 SKILL.md 파일을 수정하세요:

```markdown
## 실행 흐름

...

### 6단계: Gmail 전송

LinkedIn 추천 결과를 이메일로 전송합니다.

\```bash
python scripts/gmail_sender.py sync/YYYY-MM-DD-linkedin-recommendations.md your-email@gmail.com
\```
```

## 사용 예시

```bash
# 추천 결과를 이메일로 전송
python gmail_sender.py sync/2026-02-28-linkedin-recommendations.md paddington@example.com

# 출력:
# ✅ 이메일 전송 성공! Message ID: 18d3f2a1b2c3d4e5
```

## 문제 해결

### credentials.json 파일이 없다는 오류
- Google Cloud Console에서 OAuth 2.0 클라이언트 ID를 생성하고 JSON을 다운로드하세요
- 파일 이름이 정확히 `credentials.json`인지 확인하세요

### 인증 관련 오류
- `token.pickle` 파일을 삭제하고 다시 실행하여 재인증하세요
- Gmail API가 활성화되어 있는지 확인하세요

### 이메일 전송 실패
- 인터넷 연결 확인
- Gmail API 할당량 확인 (하루 최대 전송 개수 제한 있음)
