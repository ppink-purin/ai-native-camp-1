---
name: my-fetch-youtube
description: YouTube URL을 받으면 자막을 추출하고, Web Search로 자동자막 오류를 보정한 뒤, 요약-인사이트-전체 번역을 제공하는 스킬. "유튜브 번역", "영상 정리", "YouTube 요약" 요청에 사용.
---

# My Fetch YouTube Skill

YouTube 영상의 자막을 추출하고 번역하는 스킬입니다.

## 자막 추출

YouTube 영상에서 자막을 추출하고 텍스트로 정제합니다.

### 1. yt-dlp로 자막 다운로드

다음 명령어로 YouTube 영상의 자막을 추출합니다:

```bash
yt-dlp --write-auto-sub --sub-lang "ko,en" --skip-download --convert-subs vtt -o "%(title)s" "{URL}"
```

**명령어 설명:**
- `--write-auto-sub`: 자동 생성 자막 포함
- `--sub-lang "ko,en"`: 한국어 우선, 영어 차선으로 자막 다운로드
- `--skip-download`: 영상은 다운로드하지 않음 (자막만 추출)
- `--convert-subs vtt`: VTT 형식으로 변환
- `-o "%(title)s"`: 영상 제목으로 파일명 지정

### 1-1. WebFetch로 자막 가져오기 (yt-dlp 대안)

yt-dlp가 PO token 제한으로 자막을 다운로드하지 못할 경우, WebFetch를 사용하여 YouTube의 비공식 Transcript API를 직접 호출할 수 있습니다.

**YouTube Transcript API URL 구조:**

```
https://www.youtube.com/api/timedtext?v={VIDEO_ID}&lang={LANG_CODE}&fmt=json3
```

**URL 파라미터:**
- `v`: YouTube 영상 ID (URL에서 추출)
  - 예: `https://www.youtube.com/watch?v=abc123` → VIDEO_ID는 `abc123`
- `lang`: 자막 언어 코드 (`ko`, `en`, `ja` 등)
- `fmt`: 응답 형식 (`json3` 권장 - 가장 상세한 정보)

**WebFetch 호출 예시:**

```
WebFetch(
    url: "https://www.youtube.com/api/timedtext?v={VIDEO_ID}&lang=ko&fmt=json3",
    prompt: "Extract all subtitle text from the events array. For each event, get the 'utf8' field from 'segs' array and combine them into a continuous transcript. Ignore timestamps and return only the text content."
)
```

**언어 우선순위:**

1. **한국어** (`lang=ko`) 먼저 시도
2. **영어** (`lang=en`) 차선으로 시도
3. 자막이 없으면 다른 영상 선택 안내

**JSON 응답 구조:**

YouTube Transcript API는 다음과 같은 JSON을 반환합니다:

```json
{
  "events": [
    {
      "tStartMs": 0,
      "dDurationMs": 2000,
      "segs": [
        {"utf8": "안녕하세요"}
      ]
    },
    {
      "tStartMs": 2000,
      "dDurationMs": 3000,
      "segs": [
        {"utf8": "오늘은 Claude에 대해"}
      ]
    }
  ]
}
```

- `events`: 자막 이벤트 배열
- `tStartMs`: 시작 시간 (밀리초)
- `dDurationMs`: 지속 시간 (밀리초)
- `segs`: 텍스트 세그먼트 배열
- `utf8`: 실제 자막 텍스트

**텍스트 추출 프롬프트:**

WebFetch 호출 시 다음 프롬프트를 사용합니다:

```
"Extract all subtitle text from the events array.
For each event, get the 'utf8' field from the 'segs' array and combine all segments into a single continuous transcript.
Ignore all timestamps and metadata.
Return only the pure text content, with each segment on a new line."
```

**yt-dlp vs WebFetch 선택 기준:**

| 상황 | 사용 방법 | 이유 |
|------|----------|------|
| 일반적인 경우 | yt-dlp 우선 시도 | 가장 안정적이고 자막 목록 확인 가능 |
| PO token 오류 발생 | WebFetch로 전환 | YouTube API 직접 호출로 제한 우회 |
| 자막 언어 확인 필요 | yt-dlp --list-subs | 사용 가능한 모든 자막 언어 목록 확인 |
| 빠른 단일 자막 추출 | WebFetch 직접 호출 | 파일 다운로드 없이 즉시 텍스트 반환 |

**WebFetch 실행 순서:**

1. **VIDEO_ID 추출**
   - URL에서 `v=` 파라미터 추출
   - 예: `https://www.youtube.com/watch?v=Uh98_aGhAuY` → `Uh98_aGhAuY`

2. **한국어 자막 시도**
   ```
   WebFetch(
       url: "https://www.youtube.com/api/timedtext?v=Uh98_aGhAuY&lang=ko&fmt=json3",
       prompt: "Extract all subtitle text..."
   )
   ```

3. **한국어 자막이 없으면 영어 시도**
   ```
   WebFetch(
       url: "https://www.youtube.com/api/timedtext?v=Uh98_aGhAuY&lang=en&fmt=json3",
       prompt: "Extract all subtitle text..."
   )
   ```

4. **둘 다 없으면 사용자에게 안내**
   ```
   ⚠️ 이 영상에는 한국어/영어 자막이 없습니다. 다른 영상을 선택해주세요.
   ```

**주의사항:**

- WebFetch는 한 번에 하나의 언어만 요청 가능 (순차적으로 시도 필요)
- 자막이 없으면 빈 `events` 배열 반환
- VTT 파일 방식과 달리 이미 정제된 텍스트로 반환됨 (타임스탬프 제거 불필요)
- Web Search 보정은 동일하게 적용

### 2. VTT 자막을 순수 텍스트로 정제

다운로드한 VTT 파일에는 타임스탬프, 번호, 웹 형식 표시가 포함되어 있습니다. 다음 sed 파이프라인으로 순수 텍스트만 추출합니다:

```bash
cat "자막파일.vtt" | sed -E 's/^[0-9]+$//' | sed -E 's/[0-9]{2}:[0-9]{2}:[0-9]{2}.*//g' | sed -E 's/<[^>]+>//g' | tr -s '\n' | grep -v '^$'
```

**파이프라인 설명:**
1. `sed -E 's/^[0-9]+$//'` - 자막 번호 제거
2. `sed -E 's/[0-9]{2}:[0-9]{2}:[0-9]{2}.*//g'` - 타임스탬프 제거
3. `sed -E 's/<[^>]+>//g'` - HTML/웹 형식 표시 제거
4. `tr -s '\n'` - 연속된 빈 줄을 하나로 압축
5. `grep -v '^$'` - 빈 줄 완전히 제거

### 3. 자막 언어 우선순위

자막이 여러 언어로 제공될 경우, 다음 우선순위로 선택합니다:

1. **한국어 수동 자막** (manual) - 가장 정확
2. **영어 수동 자막** (manual) - 두 번째로 정확
3. **한국어 자동 자막** (auto-generated) - Web Search 보정 필요
4. **영어 자동 자막** (auto-generated) - Web Search 보정 필요

수동 자막이 있으면 자동 자막보다 우선적으로 사용합니다.

### 4. 자막이 없는 경우

자막이 전혀 제공되지 않는 영상의 경우:

```
⚠️ 이 영상에는 자막이 없습니다. 다른 영상을 선택해주세요.
```

자막 없는 영상은 처리할 수 없으므로 명확히 안내합니다.

## 메타데이터 추출

영상의 메타데이터를 추출하여 컨텍스트를 파악하고 Web Search 보정에 활용합니다.

### 명령어

```bash
yt-dlp --dump-json --no-download "{URL}"
```

**명령어 설명:**
- `--dump-json`: 영상 정보를 JSON 형식으로 출력
- `--no-download`: 영상 다운로드하지 않음 (메타데이터만 추출)

### 추출할 주요 필드

yt-dlp가 반환하는 JSON에서 다음 정보를 추출합니다:

#### 1. title (영상 제목)
- 영상의 공식 제목
- Web Search 보정 시 핵심 키워드 출처
- 예: `"Claude 4.5 소개: 차세대 AI 모델"`

#### 2. description (영상 설명)
- 영상 설명란 전체 텍스트
- 고유명사, 링크, 관련 용어 포함
- Web Search 키워드 추출의 주요 소스

#### 3. channel (채널명)
- 업로더/채널 이름
- `uploader` 또는 `channel` 필드 사용
- 예: `"Anthropic"`

#### 4. duration (영상 길이)
- 초 단위 영상 길이
- 10분(600초) 이상이면 Task Agent 사용 권장
- 예: `1234` (20분 34초)

#### 5. chapters (챕터)
- 영상에 챕터가 설정되어 있는 경우
- 각 챕터의 시작 시간과 제목
- 번역 시 챕터별로 구분하여 제공

**챕터 예시:**
```json
{
  "chapters": [
    {"start_time": 0, "title": "소개"},
    {"start_time": 120, "title": "주요 기능"},
    {"start_time": 300, "title": "데모"}
  ]
}
```

### 메타데이터 활용

추출한 메타데이터는 다음 단계에서 활용됩니다:

1. **Web Search 보정**: title과 description에서 키워드 추출
2. **컨텍스트 제공**: 사용자에게 영상 정보 표시
3. **번역 구조화**: 챕터가 있으면 챕터별로 번역 구분
4. **처리 방식 결정**: duration에 따라 Task Agent 사용 여부 결정

## Web Search 보정 (핵심!)

자동 자막의 고유명사/전문 용어 오류를 웹 검색으로 보정합니다. 이것이 fetch-youtube를 fetch-tweet보다 한 단계 더 발전시키는 핵심 기능입니다.

### 왜 필요한가?

YouTube의 자동 자막은 AI 음성 인식으로 생성되어 다음과 같은 오류가 발생합니다:

- **고유명사 오인식**: "Claude" → "Cloud", "Anthropic" → "앤트로피"
- **전문 용어 오류**: "Prompt Engineering" → "프롬프트 엔지니어링" (부정확)
- **약어 오류**: "AI" → "에이", "LLM" → "엘엘엠"

### 보정 프로세스

#### 1단계: 키워드 추출 (5-10개)

영상 제목과 description에서 다음 유형의 키워드를 추출합니다:

**고유명사:**
- 사람 이름: "Sam Altman", "Dario Amodei"
- 회사명: "Anthropic", "OpenAI", "Google DeepMind"
- 제품명: "Claude", "GPT-4", "Gemini"

**전문 용어:**
- 기술 용어: "Transformer", "Fine-tuning", "RAG"
- 업계 용어: "Constitutional AI", "Chain of Thought"

**약어:**
- "AI", "LLM", "NLP", "AGI", "API"

**추출 예시:**

영상 제목: "Claude 4.5 소개: Anthropic의 차세대 AI 모델"

추출된 키워드:
1. Claude
2. Anthropic
3. AI 모델
4. Constitutional AI
5. LLM

#### 2단계: WebSearch 병렬 실행

추출한 각 키워드에 대해 WebSearch를 병렬로 실행합니다:

**검색 쿼리 패턴:**

```
"{키워드} 정확한 표기"
"{사람 이름} {회사명}"
"{전문 용어} explained"
"{약어} full form"
```

**검색 예시:**

```
WebSearch("Claude AI 정확한 표기")
WebSearch("Anthropic company")
WebSearch("Constitutional AI explained")
WebSearch("LLM full form")
```

#### 3단계: 자동 자막 보정

검색 결과를 바탕으로 자막의 오류를 수정합니다:

**보정 규칙:**

1. **고유명사**: 검색 결과의 공식 표기 사용
2. **전문 용어**: 원문 병기 (예: "헌법적 AI(Constitutional AI)")
3. **약어**: 전체 형태 확인 후 맥락에 맞게 유지
4. **보정 내역 기록**: 원문 → 수정 형태로 기록

**보정 예시:**

| 원문 (자동 자막) | 수정 (보정 후) | 근거 |
|----------------|---------------|------|
| "클라우드 포인트 파이브" | "Claude 4.5" | WebSearch: "Claude AI" |
| "앤트로피사" | "Anthropic" | WebSearch: "Anthropic company" |
| "컨스티튜셔널 에이아이" | "Constitutional AI" | WebSearch: 공식 용어 |
| "라지 랭귀지 모델" | "대규모 언어 모델(LLM)" | WebSearch: 정식 번역 + 약어 병기 |

### 보정 전/후 비교

#### 보정 전 (자동 자막 원문)

```
오늘은 클라우드라는 새로운 에이아이 모델에 대해 소개하겠습니다.
이 모델은 앤트로피사에서 개발했으며, 컨스티튜셔널 에이아이 기법을
사용합니다. 기존의 라지 랭귀지 모델과 비교했을 때...
```

#### 보정 후

```
오늘은 Claude라는 새로운 AI 모델에 대해 소개하겠습니다.
이 모델은 Anthropic에서 개발했으며, Constitutional AI 기법을
사용합니다. 기존의 대규모 언어 모델(LLM)과 비교했을 때...
```

**보정 내역:**
- "클라우드" → "Claude" (고유명사)
- "에이아이" → "AI" (약어)
- "앤트로피사" → "Anthropic" (회사명)
- "컨스티튜셔널 에이아이" → "Constitutional AI" (전문 용어)
- "라지 랭귀지 모델" → "대규모 언어 모델(LLM)" (전문 용어 + 약어 병기)

### 보정 결과 표시

사용자에게 보정 내역을 투명하게 제공합니다:

```markdown
## 자막 보정 내역

자동 자막에서 다음 용어들을 보정했습니다:

1. "클라우드" → "Claude" (AI 모델명)
2. "앤트로피사" → "Anthropic" (회사명)
3. "컨스티튜셔널 에이아이" → "Constitutional AI" (기술 용어)
4. "라지 랭귀지 모델" → "대규모 언어 모델(LLM)" (전문 용어)

총 4개 용어 보정 완료
```

### 주의사항

- **과도한 보정 방지**: 명확한 오류만 수정 (추측성 수정 금지)
- **맥락 고려**: 동일 단어라도 맥락에 따라 다르게 보정
- **원문 보존**: 보정 전 원문도 기록하여 필요시 참고 가능

## 번역 파이프라인

자막을 추출하고 보정한 후, 3단계로 나누어 번역을 제공합니다. fetch-tweet과 동일한 구조이지만 YouTube 영상에 최적화되어 있습니다.

### 1단계 - 요약 (3-5문장)

영상의 핵심 내용을 빠르게 파악할 수 있도록 요약합니다.

**포함 내용:**
- 영상의 핵심 주제와 메시지
- 채널명과 영상 제목
- 영상 길이와 주요 정보

**예시:**
```
Anthropic 공식 채널에서 게시한 "Claude 4.5 소개" 영상 (15분)입니다.
새로운 AI 모델 Claude 4.5의 주요 기능과 개선사항을 소개합니다.
Constitutional AI 기법을 통해 안전성을 크게 향상시켰으며,
멀티모달 기능과 코딩 능력이 강화되었습니다.
```

### 2단계 - 인사이트 (3개)

영상의 의미를 더 깊이 분석합니다.

**1. 핵심 메시지**
- 이 영상이 정말 전달하고자 하는 것
- 발표자/제작자의 의도
- 주요 주장과 근거

**2. 시사점**
- 업계 또는 기술 트렌드에서의 의미
- 이 영상이 나타내는 변화나 흐름
- 다른 제품/서비스와의 비교

**3. 적용점**
- 나(시청자)에게 어떤 의미인지
- 실제로 어떻게 활용하거나 적용할 수 있는지
- 추가로 학습하면 좋을 내용

### 3단계 - 전체 번역된 아티클

영상 전체를 읽기 쉬운 아티클 형태로 번역합니다.

**아티클 구조:**

```markdown
# [영상 제목 번역]

**채널:** [채널명]
**길이:** [분:초]
**게시일:** [날짜]

## 소개

[영상 오프닝 내용]

## [챕터 1 제목]

[챕터 1 내용 번역]

## [챕터 2 제목]

[챕터 2 내용 번역]

## 결론

[영상 마무리 내용]
```

**번역 원칙:**

1. **보정된 용어 사용**
   - Web Search로 보정한 고유명사/전문 용어 적용
   - 예: "Claude", "Anthropic", "Constitutional AI"

2. **전문 용어 원문 병기**
   - 한국어 번역 후 괄호로 원문 표기
   - 예: "헌법적 AI(Constitutional AI)", "대규모 언어 모델(LLM)"

3. **챕터별 구분** (챕터가 있는 경우)
   - 메타데이터의 chapters 정보 활용
   - 각 챕터를 섹션으로 구분하여 가독성 향상

4. **자연스러운 한국어**
   - 문장 구조를 한국어 어순에 맞게 조정
   - 구어체 특성을 고려한 번역 (YouTube는 말하는 내용)
   - 불필요한 반복이나 간투사 정리

5. **타임스탬프 제거**
   - VTT 형식의 타임스탬프는 이미 정제 단계에서 제거됨
   - 깔끔한 아티클 형태로 제공

### 긴 영상 처리 (10분 이상)

영상 길이가 10분(600초) 이상인 경우, **Task Agent**를 사용하여 처리합니다.

**Task Agent 사용 이유:**

- **컨텍스트 관리**: 긴 자막은 메인 세션 컨텍스트를 과도하게 소모
- **효율성**: 번역 작업을 별도 에이전트에게 위임하여 메인 세션 보호
- **품질**: 충분한 컨텍스트로 전체 내용을 일관되게 번역

**Task Agent 호출 방법:**

```
Task(
    subagent_type="general-purpose",
    description="YouTube 영상 번역",
    prompt="""
    다음 YouTube 자막을 번역해주세요:

    [보정된 자막 전체]

    요약 → 인사이트 → 전체 아티클 순서로 제공해주세요.
    """
)
```

**짧은 영상 (10분 미만):**
- 메인 세션에서 직접 처리
- 즉시 번역 결과 제공

**긴 영상 (10분 이상):**
- Task Agent로 위임
- 번역 완료 후 결과 통합
