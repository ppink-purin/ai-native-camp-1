# AI Native Camp - 프로젝트 컨텍스트

## 프로젝트 개요
- **목적**: AI Native Camp 학습 프로젝트 (Day 1-6 커리큘럼)
- **사용자**: 까망퓨린
- **시작일**: 2026-02-27
- **현재 진행**: Day 4 실습 (2026-02-28)
- **학습 내용**: Claude Code, 커스텀 스킬, MCP, Multi-agent 패턴

## 현재 진도

- ✅ Day 1: Onboarding (Claude Code 기초)
- ✅ Day 2: Context Sync 스킬 만들기 (my-context-sync)
- 🔄 Day 4: Session Wrap & Analyze (my-session-wrap)
- ⏳ Day 5: Fetch & Digest (콘텐츠 수집 스킬)
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
│       ├── my-context-sync/ # 커스텀: LinkedIn 분석
│       └── my-session-wrap/ # 커스텀: 세션 정리
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

## 환경 변수
- `LINKEDIN_ACCESS_TOKEN`: LinkedIn API 토큰 (선택사항)
- Gmail OAuth: `scripts/credentials.json` 사용

## 학습 노트 (2026-02-28)

### 배운 점
- Claude Code 기본 워크플로우 이해
- README.md의 중요성 인식
- AI 에이전트 활용의 효율성 발견
- 세션 요약의 중요성 인식

### 개선점
- Git 저장소 미초기화 → 이제 초기화 완료
- 최소한의 문서화 → CLAUDE.md, README.md 확장

### 새로운 발견
- Multi-agent 패턴의 강력함
- 병렬 실행으로 분석 속도 향상
- 검증 단계로 중복 제거 및 품질 향상

## 다음 단계
- Day 5: Fetch & Digest (트윗/유튜브 콘텐츠 수집)
  - yt-dlp 설치 필요
  - fetch-tweet, fetch-youtube, content-digest 스킬 만들기
- Day 6: PRD Submit (최종 프로젝트 제출)
