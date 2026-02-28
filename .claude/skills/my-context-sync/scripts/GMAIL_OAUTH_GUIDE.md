# Gmail OAuth 설정 완벽 가이드

Gmail API를 사용하여 이메일을 전송하려면 Google OAuth 인증이 필요합니다.
이 가이드는 **처음부터 끝까지** 모든 단계를 상세히 설명합니다.

⏱️ **예상 소요 시간**: 10-15분

---

## ✅ 체크리스트

완료한 항목에 체크하세요:

- [ ] Step 1: Google Cloud 프로젝트 생성
- [ ] Step 2: Gmail API 활성화
- [ ] Step 3: OAuth 동의 화면 구성
- [ ] Step 4: OAuth 2.0 클라이언트 ID 생성
- [ ] Step 5: credentials.json 다운로드 및 저장
- [ ] Step 6: 첫 실행 및 인증 테스트

---

## Step 1: Google Cloud 프로젝트 생성

### 1-1. Google Cloud Console 접속

1. 웹 브라우저를 열고 다음 URL로 이동:
   ```
   https://console.cloud.google.com/
   ```

2. **Google 계정으로 로그인**
   - Gmail을 보낼 때 사용할 Google 계정으로 로그인하세요
   - 회사 계정 또는 개인 계정 모두 가능합니다

### 1-2. 새 프로젝트 생성

1. 상단 메뉴바에서 **프로젝트 선택** 드롭다운 클릭
   - "Select a project" 또는 현재 프로젝트 이름이 표시됩니다
   - 파란색 텍스트로 되어 있습니다

2. 팝업창에서 우측 상단의 **NEW PROJECT** 버튼 클릭

3. 프로젝트 정보 입력:
   ```
   Project name: LinkedIn Sync
   Location: No organization (또는 원하는 조직)
   ```

4. **CREATE** 버튼 클릭

5. ⏳ 프로젝트 생성 대기 (10-30초)
   - 우측 상단 종 모양 알림 아이콘에서 진행 상황 확인 가능

6. 생성 완료 후 **SELECT PROJECT** 클릭하여 프로젝트 활성화

> ✅ **확인**: 상단 메뉴바에 "LinkedIn Sync" 프로젝트가 선택되어 있어야 합니다

---

## Step 2: Gmail API 활성화

### 2-1. API 라이브러리로 이동

1. 좌측 햄버거 메뉴 ☰ 클릭

2. **APIs & Services** > **Library** 선택
   - 또는 직접 URL 입력:
     ```
     https://console.cloud.google.com/apis/library
     ```

### 2-2. Gmail API 검색 및 활성화

1. 검색창에 `gmail` 입력

2. **Gmail API** 선택
   - 아이콘: 빨간색/흰색 편지봉투 모양
   - 제공: Google LLC

3. **ENABLE** 버튼 클릭

4. ⏳ API 활성화 대기 (5-10초)

> ✅ **확인**: "API enabled" 메시지가 표시되고, 페이지가 Gmail API 대시보드로 이동합니다

---

## Step 3: OAuth 동의 화면 구성

Gmail API를 사용하려면 OAuth 동의 화면을 먼저 설정해야 합니다.

### 3-1. OAuth 동의 화면으로 이동

1. 좌측 메뉴에서 **APIs & Services** > **OAuth consent screen** 선택
   - 또는 직접 URL:
     ```
     https://console.cloud.google.com/apis/credentials/consent
     ```

### 3-2. 사용자 유형 선택

1. **User Type** 선택:
   ```
   ⦿ External (외부)
   ```
   - 개인 또는 소규모 팀 사용의 경우 External 선택
   - Google Workspace 조직 내부에서만 사용하려면 Internal 선택

2. **CREATE** 버튼 클릭

### 3-3. OAuth 동의 화면 정보 입력

**1단계: App information**

필수 항목만 입력:
```
App name: LinkedIn Sync
User support email: [본인의 이메일 주소 선택]
Developer contact email: [본인의 이메일 주소 입력]
```

선택 항목 (건너뛰어도 됨):
- App logo: 생략
- App domain: 생략

**SAVE AND CONTINUE** 클릭

**2단계: Scopes**

1. **ADD OR REMOVE SCOPES** 버튼 클릭

2. 검색창에 `gmail.send` 입력

3. 다음 scope 선택:
   ```
   ☑ https://www.googleapis.com/auth/gmail.send
   ```
   - 설명: "Send email on your behalf"

4. **UPDATE** 버튼 클릭

5. **SAVE AND CONTINUE** 클릭

**3단계: Test users**

1. **+ ADD USERS** 버튼 클릭

2. 이메일 주소 입력:
   ```
   [본인의 Gmail 주소]
   ```
   - 이메일을 보낼 때 사용할 Gmail 주소를 입력하세요

3. **ADD** 버튼 클릭

4. **SAVE AND CONTINUE** 클릭

**4단계: Summary**

- 설정 내용을 확인하고 **BACK TO DASHBOARD** 클릭

> ✅ **확인**: OAuth consent screen 페이지에서 "Publishing status: Testing" 상태여야 합니다

---

## Step 4: OAuth 2.0 클라이언트 ID 생성

### 4-1. Credentials 페이지로 이동

1. 좌측 메뉴에서 **APIs & Services** > **Credentials** 선택
   - 또는 직접 URL:
     ```
     https://console.cloud.google.com/apis/credentials
     ```

### 4-2. OAuth 클라이언트 ID 생성

1. 상단의 **+ CREATE CREDENTIALS** 버튼 클릭

2. 드롭다운에서 **OAuth client ID** 선택

3. 애플리케이션 유형 선택:
   ```
   Application type: Desktop app
   ```

4. 이름 입력:
   ```
   Name: LinkedIn Sync Desktop
   ```

5. **CREATE** 버튼 클릭

### 4-3. 클라이언트 ID 생성 완료

팝업창이 나타납니다:
```
OAuth client created
Your Client ID: [긴 문자열]
Your Client Secret: [긴 문자열]
```

> ⚠️ **중요**: 이 창을 아직 닫지 마세요!

---

## Step 5: credentials.json 다운로드 및 저장

### 5-1. JSON 파일 다운로드

1. 팝업창에서 **DOWNLOAD JSON** 버튼 클릭

2. 파일이 다운로드 폴더에 저장됩니다
   - 파일명: `client_secret_XXXXX.apps.googleusercontent.com.json`

3. 팝업창 **OK** 버튼 클릭하여 닫기

### 5-2. 파일 이름 변경 및 이동

**Option A: 터미널 사용 (추천)**

다운로드한 JSON 파일을 찾아서 이름을 변경하고 올바른 위치로 이동:

```bash
# 다운로드 폴더에서 파일 찾기 (파일명은 실제 다운로드된 이름으로 변경)
cd ~/Downloads
ls -l client_secret*.json

# 파일 이름 변경 및 올바른 위치로 복사
cp client_secret_XXXXX.apps.googleusercontent.com.json \
   /Users/paddington/Project/practice/01_AI_Native_Camp/.claude/skills/my-context-sync/scripts/credentials.json

# 복사 확인
ls -l /Users/paddington/Project/practice/01_AI_Native_Camp/.claude/skills/my-context-sync/scripts/credentials.json
```

**Option B: Finder 사용**

1. Finder에서 **Downloads** 폴더 열기

2. `client_secret_XXXXX.apps.googleusercontent.com.json` 파일 찾기

3. 파일을 다음 경로로 복사:
   ```
   /Users/paddington/Project/practice/01_AI_Native_Camp/.claude/skills/my-context-sync/scripts/
   ```

4. 파일 이름을 `credentials.json`으로 변경

### 5-3. 파일 내용 확인

JSON 파일이 올바른지 확인:

```bash
cat /Users/paddington/Project/practice/01_AI_Native_Camp/.claude/skills/my-context-sync/scripts/credentials.json
```

다음과 같은 구조여야 합니다:
```json
{
  "installed": {
    "client_id": "XXXXX.apps.googleusercontent.com",
    "project_id": "linkedin-sync-XXXXX",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "XXXXX",
    "redirect_uris": ["http://localhost"]
  }
}
```

> ✅ **확인**: credentials.json 파일이 scripts 폴더에 저장되어 있어야 합니다

---

## Step 6: 첫 실행 및 인증 테스트

### 6-1. 테스트 마크다운 파일 생성

간단한 테스트 파일 생성:

```bash
cd /Users/paddington/Project/practice/01_AI_Native_Camp/.claude/skills/my-context-sync/scripts

# 테스트 디렉토리 생성
mkdir -p sync

# 테스트 마크다운 파일 생성
cat > sync/test.md << 'EOF'
# LinkedIn 추천 테스트

이것은 Gmail 전송 테스트 메시지입니다.

## 추천 #1

**제목**: 테스트 게시물
**작성자**: 테스트 사용자
**추천 이유**: Gmail 전송 기능 테스트용

EOF
```

### 6-2. Gmail 전송 스크립트 실행

1. 터미널에서 실행:
   ```bash
   cd /Users/paddington/Project/practice/01_AI_Native_Camp/.claude/skills/my-context-sync/scripts

   python3 gmail_sender.py sync/test.md [본인의Gmail주소@gmail.com]
   ```

   > 🔄 `[본인의Gmail주소@gmail.com]`를 실제 Gmail 주소로 변경하세요

2. **자동으로 브라우저가 열립니다**

### 6-3. OAuth 인증 진행

브라우저에서:

1. **Google 계정 선택**
   - Test users에 추가한 Gmail 계정 선택

2. **보안 경고가 나타날 수 있습니다**:
   ```
   Google hasn't verified this app
   ```

   이것은 정상입니다! 다음 단계를 따르세요:

   a. **Advanced** (고급) 클릭

   b. **Go to LinkedIn Sync (unsafe)** 클릭
      - 본인이 만든 앱이므로 안전합니다

3. **권한 허용 화면**:
   ```
   LinkedIn Sync wants to access your Google Account

   This will allow LinkedIn Sync to:
   ☑ Send email on your behalf
   ```

   **Allow** (허용) 버튼 클릭

4. **인증 완료!**
   ```
   The authentication flow has completed.
   You may close this window.
   ```

   브라우저 탭을 닫아도 됩니다

### 6-4. 전송 결과 확인

터미널로 돌아가서 결과 확인:

```
✅ 이메일 전송 성공! Message ID: 18d3f2a1b2c3d4e5
```

Gmail 받은편지함을 확인하여 테스트 이메일이 도착했는지 확인하세요!

### 6-5. 인증 토큰 저장 확인

`token.pickle` 파일이 자동 생성되었는지 확인:

```bash
ls -l token.pickle
```

> ✅ **확인**: token.pickle 파일이 있으면 다음부터는 브라우저 인증 없이 바로 이메일을 보낼 수 있습니다!

---

## 🎉 설정 완료!

축하합니다! Gmail OAuth 인증 설정이 완료되었습니다.

이제 LinkedIn 추천 스킬에서 자동으로 이메일을 받을 수 있습니다.

### 다음 단계

스킬을 실행하여 실제 LinkedIn 피드를 수집하고 추천을 받아보세요:

```bash
/my-context-sync
```

---

## 🔧 문제 해결

### credentials.json 파일이 없다는 오류

```
FileNotFoundError: credentials.json 파일이 필요합니다.
```

**해결**:
- Step 5를 다시 확인하세요
- 파일이 정확히 `credentials.json`이라는 이름인지 확인
- 파일이 scripts 폴더에 있는지 확인

### "This app isn't verified" 경고

**해결**:
- 이것은 정상입니다! 본인이 만든 앱이므로 안전합니다
- "Advanced" > "Go to LinkedIn Sync (unsafe)" 클릭하여 진행

### "Access blocked: This app's request is invalid"

**해결**:
- OAuth 동의 화면 설정을 다시 확인하세요
- Scopes에 `gmail.send`가 추가되어 있는지 확인
- Test users에 본인의 Gmail이 추가되어 있는지 확인

### 이메일이 전송되지 않음

**해결**:
1. Gmail API가 활성화되어 있는지 확인
2. 인터넷 연결 확인
3. token.pickle 파일을 삭제하고 다시 인증 시도:
   ```bash
   rm token.pickle
   python3 gmail_sender.py sync/test.md your-email@gmail.com
   ```

### Gmail API 할당량 초과

**오류**:
```
Quota exceeded for quota metric 'Queries' and limit 'Queries per day'
```

**해결**:
- Gmail API는 하루 최대 전송 개수 제한이 있습니다
- 개인 계정: 하루 약 500-2000개
- 다음 날까지 대기하거나, Google Cloud Console에서 할당량 증가 요청

---

## 📚 참고 자료

- [Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)
- [OAuth 2.0 for Desktop Apps](https://developers.google.com/identity/protocols/oauth2/native-app)
- [Gmail API Send Mail](https://developers.google.com/gmail/api/guides/sending)
