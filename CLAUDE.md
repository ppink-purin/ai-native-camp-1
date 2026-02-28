# AI Native Camp - 프로젝트 컨텍스트

## 프로젝트 개요
- **목적**: AI Native Camp 학습 프로젝트 (Day 1-6 커리큘럼)
- **사용자**: 까망퓨린
- **시작일**: 2026-02-27
- **현재 진행**: Day 5 완료 (2026-02-28)
- **학습 내용**: Claude Code, 커스텀 스킬, MCP, Multi-agent 패턴

## 현재 진도

- ✅ Day 1: Onboarding (Claude Code 기초)
- ✅ Day 2: Context Sync 스킬 만들기 (my-context-sync)
- ✅ Day 4: Session Wrap & Analyze (my-session-wrap)
- ✅ Day 5: Fetch & Digest (콘텐츠 수집 및 학습)
- ⏳ Day 6: PRD Submit (최종 프로젝트 제출)

## 커스텀 스킬

### 1. my-context-sync
**위치**: `.claude/skills/my-context-sync/`
**목적**: LinkedIn 피드 분석 및 AI 추천
**트리거**: "싱크", "sync", "정보 수집"

**기능**:
- Puppeteer로 LinkedIn 피드 스크래핑
- AI가 관심사 기반으로 게시물 평가 (점수 1-10)
- TOP 10 추천 마크다운 생성 (`sync/YYYY-MM-DD-linkedin-recommendations.md`)
- Gmail 전송 옵션

**MCP 의존성**:
- Puppeteer (웹 스크래핑)
- Gmail (이메일 전송)

**관심사 키워드**:
- AI/ML
- 개발/기술
- 스타트업/비즈니스
- 기술 트렌드

### 2. my-session-wrap
**위치**: `.claude/skills/my-session-wrap/`
**목적**: 세션 종료 시 작업 정리 및 분석
**트리거**: "/wrap", "세션 정리", "마무리"

**아키텍처**:
- **Phase 1**: 4개 병렬 에이전트
  - doc-updater: 문서 업데이트 분석
  - automation-scout: 자동화 패턴 탐지
  - learning-extractor: 학습 내용 추출 (TIL)
  - followup-suggester: 후속 작업 제안
- **Phase 2**: 검증 에이전트
  - duplicate-checker: 중복 검증 및 제거
- **Phase 3**: 사용자 선택 기반 실행
  - 커밋 생성
  - 문서 업데이트
  - 자동화 생성

### 3. my-fetch-tweet
**위치**: `.claude/skills/my-fetch-tweet/`
**목적**: X/Twitter 트윗 수집 및 한국어 번역
**트리거**: "트윗 번역", "트윗 가져와", "X 게시글"

**기능**:
- FxEmbed API로 트윗 데이터 추출 (`api.fxtwitter.com`)
- 트윗 본문, 작성자, 통계 (좋아요, 리트윗, 조회수) 가져오기
- 3단계 번역 파이프라인:
  1. 요약 (3-5문장)
  2. 인사이트 (핵심 메시지, 시사점, 적용점)
  3. 전체 번역

**MCP 의존성**: WebFetch (API 호출)

### 4. my-fetch-youtube
**위치**: `.claude/skills/my-fetch-youtube/`
**목적**: YouTube 자막 추출 및 한국어 번역
**트리거**: "유튜브 번역", "영상 정리", "YouTube 요약"

**기능**:
- yt-dlp로 자막 다운로드 (ko/en 우선순위)
- WebFetch 대안: YouTube Transcript API 직접 호출
- **Web Search 보정**: 자동 자막의 고유명사/전문 용어 오류 수정
- 3단계 번역 파이프라인 (fetch-tweet과 동일)

**핵심 차별점**:
- Web Search로 자막 오류 보정 (예: "클라우드" → "Claude")
- 메타데이터 추출 (제목, 채널, 챕터)
- Task Agent 활용 (10분+ 영상)

**MCP 의존성**: WebFetch, Web Search

**제약사항**: YouTube PO token 제한으로 일부 영상 자막 추출 불가

### 5. my-content-digest
**위치**: `.claude/skills/my-content-digest/`
**목적**: Quiz-First 방식으로 콘텐츠 학습
**트리거**: "콘텐츠 소화", "퀴즈", "학습", "digest"

**핵심 원칙: Quiz-First 학습법**
- 요약을 먼저 보여주지 않음
- Pre-Quiz 3문제 → 선택적 콘텐츠 → 본 퀴즈 9문제
- Pretesting Effect로 기억력 9-12% 향상

**기능**:
1. **Pre-Quiz**: 콘텐츠 보기 전 3문제 출제
2. **선택적 요약**: 틀린 문제만 또는 전체 요약
3. **본 퀴즈**: 9문제 (기본 3 + 중급 3 + 심화 3)
4. **후속 선택**: 재퀴즈, 관련 콘텐츠 추천

**스킬 체이닝**:
```
my-fetch-tweet → my-content-digest
my-fetch-youtube → my-content-digest
```

## MCP 서버 설정

**설정 파일**: `.mcp.json`, `.claude/settings.local.json`

**활성화된 서버**:
```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "mcp-fetch-server"]
    }
  }
}
```

- **Puppeteer**: 웹 스크래핑 (LinkedIn 피드 수집)
- **Fetch**: HTTP 요청 (API 호출)
- **Gmail**: 이메일 전송 (Claude AI Gmail MCP)

## 주요 학습 내용

### Multi-Agent 패턴
- **병렬 실행**: 독립적 작업을 동시에 처리 (Phase 1의 4개 에이전트)
- **순차 실행**: 의존성 있는 작업을 순서대로 처리 (Phase 2 검증)
- **2-Phase Pipeline**: 분석 → 검증 구조로 품질 향상

### 스킬 개발 Best Practices
- Frontmatter에 명확한 트리거 설정
- 관심사 기반 동적 설정 (사용자 입력)
- 구체적인 출력 포맷 정의 (마크다운 템플릿)
- MCP 서버 연동 문서화

### 워크플로우 자동화
- LinkedIn 피드 → AI 분석 → 추천 리스트 → Gmail 전송
- 세션 정리 → 다각도 분석 → 중복 제거 → 선택 실행

## 프로젝트 구조

```
01_AI_Native_Camp/
├── .agents/skills/          # Camp 제공 스킬 (day1-6)
├── .claude/
│   ├── settings.json        # Superpowers 플러그인 설정
│   ├── settings.local.json  # MCP 서버 활성화
│   └── skills/
│       ├── my-context-sync/    # 커스텀: LinkedIn 분석
│       ├── my-session-wrap/    # 커스텀: 세션 정리
│       ├── my-fetch-tweet/     # 커스텀: 트윗 수집 및 번역
│       ├── my-fetch-youtube/   # 커스텀: YouTube 자막 추출
│       └── my-content-digest/  # 커스텀: Quiz-First 학습
├── sync/                    # AI 분석 결과 저장
│   └── 2026-02-27-linkedin-recommendations.md
├── scripts/                 # 자동화 스크립트
├── .mcp.json               # MCP 서버 설정
├── .env.example            # 환경 변수 예시
├── CLAUDE.md               # 이 파일
└── README.md               # 프로젝트 소개
```

## 일반 워크플로우

### LinkedIn 피드 분석
```
1. 사용자: "싱크" 또는 "sync"
2. AI: 관심사 확인 (AI/ML, 개발, 스타트업 등)
3. Puppeteer로 LinkedIn 피드 스크래핑
4. 각 게시물 AI 평가 (관련성, 유용성 점수)
5. TOP 10 정렬 및 마크다운 생성
6. sync/YYYY-MM-DD-linkedin-recommendations.md 저장
7. (선택) Gmail 전송
```

### 세션 정리
```
1. 사용자: "/wrap" 또는 "세션 정리"
2. Git 상태 확인 및 세션 요약 작성
3. Phase 1: 4개 에이전트 병렬 실행
4. Phase 2: duplicate-checker로 중복 검증
5. 결과 통합 및 사용자 선택
6. 선택된 작업 실행 (커밋/문서/자동화)
```

### 트윗 번역 및 학습
```
1. 사용자: "이 트윗 번역해줘 [URL]"
2. my-fetch-tweet 스킬 실행
   - FxEmbed API로 트윗 데이터 가져오기
   - 3단계 번역 (요약 → 인사이트 → 전체)
3. (선택) "퀴즈 내줘" → my-content-digest 실행
```

### YouTube 영상 학습
```
1. 사용자: "이 유튜브 영상 정리해줘 [URL]"
2. my-fetch-youtube 스킬 실행
   - yt-dlp로 자막 다운로드 (또는 Transcript API)
   - Web Search로 자동 자막 오류 보정
   - 3단계 번역 (요약 → 인사이트 → 전체)
3. (선택) "학습하기" → my-content-digest 실행
```

## 환경 변수
- `LINKEDIN_ACCESS_TOKEN`: LinkedIn API 토큰 (선택사항)
- Gmail OAuth: `scripts/credentials.json` 사용

## 학습 노트

### 2026-02-28 (Day 4)
**배운 점**:
- Multi-agent 패턴의 강력함
- 병렬 실행으로 분석 속도 향상
- 검증 단계로 중복 제거 및 품질 향상

### 2026-02-28 (Day 5)
**배운 점**:
- **Quiz-First 학습법**: 요약 대신 퀴즈부터 → 기억력 9-12% 향상 (Pretesting Effect)
- **스킬 체이닝**: fetch → digest 파이프라인으로 워크플로우 구축
- **API 활용**: FxEmbed API (트윗), YouTube Transcript API (자막)
- **Web Search 보정**: 자동 자막 오류 수정 (예: "클라우드" → "Claude")

**개선점**:
- YouTube PO token 제약 발견 → WebFetch 대안 추가
- 스킬 설계 원칙 확립 (단일 책임, 독립성)

**새로운 발견**:
- Information Gap Theory: 틀린 문제가 호기심 → 기억 강화
- 플랫폼별 제약 사항 (YouTube 보안 정책)
- 3단계 번역 파이프라인의 효과 (요약 → 인사이트 → 전체)

## 다음 단계
- ✅ Day 5: Fetch & Digest 완료
  - ✅ my-fetch-tweet (트윗 번역)
  - ✅ my-fetch-youtube (YouTube 자막 번역)
  - ✅ my-content-digest (Quiz-First 학습)
- Day 6: PRD Submit (최종 프로젝트 제출)
  - gh CLI 설치 및 인증 필요
  - PRD 작성 및 GitHub PR 제출
