# AI Native Camp - 까망퓨린

**시작일:** 2026-02-27
**현재 진행:** Day 5 완료 (2026-02-28)

## 프로젝트 소개

AI Native Camp의 실습 프로젝트입니다. Claude Code를 활용하여 LinkedIn 피드 분석, 세션 정리 자동화 등의 커스텀 스킬을 개발하고 있습니다.

## 주요 기능

### 1. LinkedIn 피드 AI 추천 (my-context-sync)
- Puppeteer로 LinkedIn 피드 자동 수집
- AI가 관심사 기반으로 게시물 평가 및 추천
- TOP 10 마크다운 리포트 생성
- Gmail 자동 전송 (선택)

**실행:**
```
"싱크" 또는 "sync" 입력
```

### 2. 세션 정리 자동화 (my-session-wrap)
- Git 변경사항 자동 분석
- 4개 병렬 에이전트로 다각도 분석
- 문서 업데이트, 자동화 제안, 학습 정리
- 사용자 선택 기반 실행

**실행:**
```
"/wrap" 또는 "세션 정리" 입력
```

### 3. 트윗 번역 및 분석 (my-fetch-tweet)
- FxEmbed API로 X/Twitter 트윗 자동 수집
- 3단계 번역 파이프라인 (요약 → 인사이트 → 전체 번역)
- 작성자 정보 및 인게이지먼트 수치 포함
- 전문 용어 원문 병기

**실행:**
```
"이 트윗 번역해줘 [URL]"
```

### 4. YouTube 영상 번역 (my-fetch-youtube)
- yt-dlp 또는 YouTube Transcript API로 자막 추출
- Web Search 보정으로 고유명사/전문 용어 오류 수정
- 메타데이터 기반 컨텍스트 파악
- 챕터별 구분 번역 (챕터 있는 경우)

**실행:**
```
"이 영상 번역해줘 [YouTube URL]"
```

### 5. Quiz-First 학습 (my-content-digest)
- Pre-Quiz로 호기심 자극 (3문제)
- 선택적 콘텐츠 제공 (틀린 부분/인사이트/전체)
- 3단계 본 퀴즈 (기본/중급/심화 각 3문제)
- 기억력 9-12% 향상 효과

**실행:**
```
"[콘텐츠] 내용으로 퀴즈 내줘"
```

## MCP 서버 설정

- **Puppeteer**: 웹 스크래핑
- **Fetch**: HTTP 요청
- **Gmail**: 이메일 전송 (OAuth 설정 필요)

설정 파일: `.mcp.json`, `.claude/settings.local.json`

## 디렉토리 구조

```
01_AI_Native_Camp/
├── .agents/skills/          # 제공된 학습 스킬 (Day 1-6)
├── .claude/skills/
│   ├── my-context-sync/     # LinkedIn 분석 스킬
│   ├── my-session-wrap/     # 세션 정리 스킬
│   ├── my-fetch-tweet/      # X/Twitter 트윗 번역 스킬
│   ├── my-fetch-youtube/    # YouTube 영상 번역 스킬
│   └── my-content-digest/   # Quiz-First 학습 스킬
├── sync/                    # AI 분석 결과 저장
├── scripts/                 # 자동화 스크립트
├── .mcp.json               # MCP 서버 설정
├── CLAUDE.md               # 프로젝트 컨텍스트
└── README.md               # 이 파일
```

## 학습 진도

- [x] Day 1: Onboarding - Claude Code 기초
- [x] Day 2: Context Sync 스킬 개발
- [x] Day 4: Session Wrap & Analyze
- [x] Day 5: Fetch & Digest
- [ ] Day 6: PRD Submit

## 생성된 리포트

- `sync/2026-02-27-linkedin-recommendations.md` - LinkedIn TOP 10 추천

## ⚡ Quick Win - 워크플로우 개선 도구

세션 히스토리 분석을 바탕으로 즉시 사용 가능한 개선 도구를 제공합니다.

### 세션 시작 체크 (10초)
```bash
./scripts/session-start.sh
```
- MCP 서버 상태, 관심사, 미완료 작업, Git 상태 자동 확인

### 세션 종료 루틴 (2분)
```bash
./scripts/session-end.sh
```
- 변경사항 확인, 관심사 업데이트, 에러 기록

### 주간 리뷰 (30분, 매주 일요일)
```bash
cat scripts/weekly-review.md
```
- 전체 세션 분석, 학습 정리, 다음 주 목표 설정

**📘 상세 가이드:** `QUICK_WIN_GUIDE.md` 참고

**효과:** 세션당 65분 절약 (65% ↓)

---

## 참고 자료

- `QUICK_WIN_GUIDE.md` - **워크플로우 개선 가이드 (필독!)**
- `CLAUDE.md` - 프로젝트 컨텍스트 및 워크플로우
- `.claude/skills/my-context-sync/SKILL.md` - LinkedIn 스킬 상세
- `.claude/skills/my-session-wrap/SKILL.md` - Session Wrap 스킬 상세
- `.claude/skills/my-fetch-tweet/SKILL.md` - 트윗 번역 스킬 상세
- `.claude/skills/my-fetch-youtube/SKILL.md` - YouTube 번역 스킬 상세
- `.claude/skills/my-content-digest/SKILL.md` - Quiz-First 학습 스킬 상세
