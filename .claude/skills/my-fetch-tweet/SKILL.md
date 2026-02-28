---
name: my-fetch-tweet
description: X/Twitter URL을 받으면 트윗 원문을 가져와서 요약-인사이트-전체 번역을 제공하는 스킬. "트윗 번역", "트윗 가져와", "X 게시글" 요청에 사용.
---

# My Fetch Tweet Skill

X/Twitter 트윗을 가져와서 한국어로 번역하는 스킬입니다.

## API 연동 방법

### FxEmbed API 사용

FxEmbed API (`api.fxtwitter.com`)를 사용하여 트윗 데이터를 가져옵니다.

#### URL 변환 과정

1. **URL에서 정보 추출**
   - `screen_name`: 트윗 작성자의 사용자명
   - `status_id`: 트윗의 고유 ID

2. **도메인 변환**
   ```
   원본: https://x.com/{screen_name}/status/{status_id}
   변환: https://api.fxtwitter.com/{screen_name}/status/{status_id}
   ```

3. **데이터 가져오기**
   - WebFetch 도구를 사용하여 JSON 데이터 요청
   - API가 트윗의 모든 정보를 JSON 형식으로 반환

4. **주요 데이터 필드**
   - `tweet.text`: 트윗 본문
   - `tweet.author.name`: 작성자 이름
   - `tweet.author.screen_name`: 작성자 사용자명
   - `tweet.likes`: 좋아요 수
   - `tweet.retweets`: 리트윗 수
   - `tweet.replies`: 답글 수
   - `tweet.views`: 조회수 (있는 경우)

#### 지원 URL 형식

다음 도메인의 트윗 URL을 모두 지원합니다:
- `x.com`
- `twitter.com`
- `fxtwitter.com`
- `fixupx.com`

## 번역 파이프라인

트윗을 가져온 후, 3단계로 나누어 번역을 제공합니다. 전체 번역을 바로 보여주지 않고 단계별로 제공하는 이유는 핵심부터 파악하고 맥락을 이해한 후 전체를 읽으면 이해도가 훨씬 높아지기 때문입니다.

### 1단계 - 요약 (3-5문장)

트윗의 핵심을 빠르게 파악할 수 있도록 요약합니다.

**포함 내용:**
- 트윗의 핵심 주장을 한국어로 요약
- 작성자 정보 (이름, 사용자명)
- 인게이지먼트 수치 (좋아요, 리트윗, 조회수 등)

**예시:**
```
@username (작성자명)이 AI 에이전트의 미래에 대해 트윗했습니다.
핵심 주장은 [요약 내용].
좋아요 1.2K, 리트윗 234, 조회수 45K를 기록했습니다.
```

### 2단계 - 인사이트 (3개)

트윗의 의미를 더 깊이 분석합니다.

**1. 핵심 메시지**
- 이 트윗이 정말 말하고 싶은 것
- 표면적 내용 뒤에 숨은 진짜 메시지

**2. 시사점**
- 업계 또는 트렌드에서의 의미
- 이 트윗이 나타내는 변화나 흐름

**3. 적용점**
- 나(독자)에게 어떤 의미인지
- 실제로 어떻게 활용하거나 참고할 수 있는지

### 3단계 - 전체 번역

원문 전체를 자연스러운 한국어로 번역합니다.

**번역 원칙:**
- 원문 전체를 자연스러운 한국어로 번역
- 인용 트윗이나 스레드가 있으면 함께 번역
- 전문 용어는 한국어 번역 후 원문 병기
  - 예: "에이전트(Agent)", "프롬프트 엔지니어링(Prompt Engineering)"
- 링크나 해시태그는 원문 그대로 유지
- 문장 구조는 한국어 어순에 맞게 자연스럽게 조정

## WebFetch Fallback

스크립트 실행이 어렵거나 불가능한 환경에서는 WebFetch 도구를 직접 사용하여 API를 호출할 수 있습니다.

### 사용 방법

**1. URL 구성**

트윗 URL에서 `screen_name`과 `status_id`를 추출하여 API URL을 만듭니다:

```
https://api.fxtwitter.com/{screen_name}/status/{status_id}
```

**예시:**
```
원본: https://x.com/elonmusk/status/1234567890
API:  https://api.fxtwitter.com/elonmusk/status/1234567890
```

**2. WebFetch 호출**

WebFetch 도구를 사용하여 데이터를 가져옵니다:

```
WebFetch(
  url: "https://api.fxtwitter.com/{screen_name}/status/{status_id}",
  prompt: "Extract the full tweet text, author name, and engagement metrics"
)
```

**3. 응답 처리**

API가 반환한 JSON 데이터에서 필요한 정보를 추출하여 번역 파이프라인(요약 → 인사이트 → 전체 번역)을 진행합니다.

### Fallback 사용 시나리오

- 스크립트 실행 권한이 없는 환경
- 간단한 트윗 하나만 빠르게 확인할 때
- API 직접 호출이 더 적합한 상황
