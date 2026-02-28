# TIL: Day 1 Onboarding - Claude Code 핵심 기능 학습

**날짜**: 2026-03-01
**주제**: AI Native Camp Day 1 - Claude Code 7가지 핵심 기능 체험 및 학습

---

## 학습 개요

Day 1 Onboarding은 "Working Backward" 방식으로 진행되었다. 즉, 7일 후 모습을 먼저 체험하고, 그 원리를 이해하는 순서로 학습했다.

### 핵심 학습 방법론
- **Working Backward**: 결과물을 먼저 보고, 원리를 나중에 이해
- **2-Phase 학습**: 각 블록을 반드시 2턴으로 나눔
  - Phase A: 설명 + 실행 안내 → STOP
  - Phase B: 퀴즈 + 피드백 → 다음 블록 이동
- **체험 중심**: 외우지 않고 느끼기, 모르면 Claude에게 물어보기

---

## 7가지 핵심 기능

### 1. CLAUDE.md - 팀 위키
**근본 원리**: 시스템 프롬프트
**역할**: Claude가 매 세션 시작할 때 자동으로 읽는 영구 기억
**비유**: 팀 위키 - Claude의 규칙서

```
세션 시작
  │
  ▼
CLAUDE.md ──→ 시스템 프롬프트 ──→ Claude가 규칙을 아는 상태로 대화 시작
```

**핵심 명령어**:
- `/init`: 현재 폴더 분석하여 CLAUDE.md 자동 생성
- `/memory`: 개인 선호사항을 영구 기억으로 저장

**실전 활용**:
- "항상 존댓말로", "표로 정리해줘" 같은 개인 규칙 저장
- 프로젝트 구조, 기술 스택, 빌드 방법 등 자동 파악

---

### 2. Skill - 업무 레시피
**근본 원리**: 점진적 로딩(Progressive Disclosure)
**역할**: 반복하는 업무를 한 번 저장하면 다음부터 한 줄로 실행
**비유**: 업무 레시피 - 자동화된 워크플로우

**CLAUDE.md와의 차이**:
- CLAUDE.md: 항상 전부 로딩 (매 세션)
- Skill: 필요할 때만 점진적으로 로딩 (컨텍스트 윈도우 절약)

**폴더 구조**:
```
my-skill/
├── SKILL.md          # 필수: 스킬의 본체 (메타데이터 + 지시사항)
├── scripts/          # 선택: 실행할 코드
├── references/       # 선택: 참고 문서, 교안
└── assets/           # 선택: 템플릿, 리소스
```

**핵심**: `SKILL.md`만 있으면 스킬이 된다. 나머지는 필요할 때 추가.

**실전 활용 예시**:
- `/weekly-sync`: Slack 메시지 수집 → git log 확인 → 문서 생성
- `/day1-onboarding`: 이 온보딩 자체도 Skill로 구현됨

---

### 3. MCP - 외부 도구 플러그
**근본 원리**: 툴 콜링(Tool Calling)
**역할**: Claude와 외부 도구(Slack, Calendar, Notion)를 연결하는 오픈 표준 프로토콜
**비유**: 외부 도구 플러그 - 서비스 연결 어댑터

```
Claude ──── "Slack에서 메시지 읽어줘"
  │
  ▼ 툴 콜링
Claude Code ◀══ MCP 프로토콜 ══▶ Slack Server
  내 컴퓨터                       외부 서비스
```

**핵심**: AI가 텍스트만 생성하는 게 아니라, "이 함수를 이 파라미터로 호출해"라고 구조화된 요청을 보냄.

**실전 활용**:
- Slack 메시지 읽기/쓰기
- Gmail 이메일 검색/작성
- Puppeteer로 웹 자동화
- Fetch로 웹 콘텐츠 가져오기

---

### 4. Subagent - 부하 직원
**근본 원리**: 프로세스 격리 + Blank Slate
**역할**: 독립된 공간에서 특정 작업을 전담 처리
**비유**: 부하 직원 - 1:1 위임 후 보고받기

```
┌─ 메인 Claude ──────────────────────────┐
│  대화 컨텍스트: [A, B, C, D, E...]     │
│                                        │
│  "PDF 분석해줘" ──┐                     │
│                   ▼                    │
│  ┌─ Subagent ──────────────┐           │
│  │ 컨텍스트: [blank slate]  │           │
│  │ 작업: PDF 분석            │           │
│  │ 결과: 요약 3줄 ──────────┼──▶ 전달   │
│  └─────────────────────────┘           │
└────────────────────────────────────────┘
```

**핵심**: 메인 대화의 컨텍스트를 물려받지 않고, 빈 상태에서 시작해서 작업만 수행.

**실전 활용 예시**:
```
이 폴더의 파일 구조를 탐색해서 정리해줘. Explore 에이전트를 사용해
```

---

### 5. Agent Teams - 프로젝트 팀
**근본 원리**: 멀티 에이전트 협업
**역할**: 각 에이전트가 독립된 컨텍스트 윈도우를 갖고, 서로 메시지를 주고받으며 협업
**비유**: 프로젝트 팀 - 팀원끼리 직접 소통 + 공유 칸반보드

**Subagent와의 차이**:
- Subagent: 부하 직원 (1:1 위임, 리더에게만 보고)
- Agent Teams: 프로젝트 팀 (팀원끼리 직접 소통 + 공유 태스크 리스트)

```
┌─ 리더 ─────────────────────────────────────┐
│                                            │
│  ┌─ Agent A ─┐  ┌─ Agent B ─┐  ┌─ Agent C ─┐
│  │ 시장조사   │  │ 보고서    │  │ 발표자료   │
│  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
│        │              │              │
│        └──────── 메시지 ─────────────┘
│                    +
│            공유 태스크 리스트
└────────────────────────────────────────────┘
```

**활성화 방법** (`~/.claude/settings.json`):
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

**실전 활용**:
- 복잡한 프로젝트를 여러 전문가 에이전트가 동시 작업
- 시장조사, 보고서 작성, 발표자료 생성을 병렬 처리

---

### 6. Hook - 자동 체크리스트
**근본 원리**: 결정론적 프로그래밍
**역할**: 특정 이벤트가 발생하면 자동으로 실행
**비유**: 자동 체크리스트 - 이벤트 기반 자동화

**AI vs Hook**:
```
AI (확률적)                    Hook (결정론적)
  "파일 저장 후                   파일 저장 이벤트
   포맷팅 해줘"                      │
      │                            ▼
      ▼                     ┌──────────────┐
  대부분 함                  │ prettier     │
  가끔 까먹음                │ --write .    │ ← 100% 실행
                            └──────────────┘
```

**핵심**: AI는 확률적이라 "대부분" 맞지만 100%는 아님. Hook은 코드가 실행되므로 100% 확실.

**실전 활용 예시**:
```
Stop Hook을 추가해줘. 응답이 끝나면 현재 시간을 터미널에 출력하도록
```
→ 응답이 끝날 때마다 `[완료] 14:32:05` 같은 시간이 터미널에 표시됨.

---

### 7. Plugin - 종합 패키지
**근본 원리**: 패키징과 배포
**역할**: 위의 모든 기능을 하나의 설치 단위로 묶어서 팀 전체가 동일한 환경을 갖추게 함
**비유**: 종합 패키지 - 한 줄로 팀 배포

```
개별 설치 (Plugin 없이)          Plugin (한 번에)
┌─────────┐                    ┌─────────────────┐
│ Skill A │ ← 수동 복사         │ marketing-plugin│
│ Skill B │ ← 수동 복사         │ ┌─ Skill A,B   │
│ MCP 설정 │ ← 수동 설정   vs   │ ├─ MCP 설정    │
│ Hook 설정│ ← 수동 설정         │ ├─ Hook 설정   │
│ Agent   │ ← 수동 설정         │ └─ Agent       │
└─────────┘                    └────────┬────────┘
  팀원 각자 반복                         │
                              claude plugin add
                                한 줄이면 끝
```

**실전 활용 예시**:
```
# 마켓플레이스 등록
/plugin marketplace add obra/superpowers-marketplace
/plugin marketplace add team-attention/plugins-for-claude-natives

# 플러그인 설치
/plugin install superpowers@superpowers-marketplace
/plugin install clarify
```

**설치한 플러그인**:
- `superpowers`: 개발 워크플로우 강화
- `clarify`: 모호한 요청을 명확하게 만들어줌 (Day 3에서 심화)

---

## 7가지 기능의 관계도

```
┌─ CLAUDE.md ─── Claude가 매번 읽는 규칙
│
├─ Skill ─────── 반복 업무를 레시피로 저장
│   └─ MCP ───── Slack, Calendar 등 외부 도구 연결
│
├─ Subagent ──── 하나의 작업을 백그라운드에서 처리
│   └─ Agent Teams ── 여러 Subagent가 동시에 작업
│
├─ Hook ──────── 특정 이벤트 발생 시 자동 실행
│
└─ Plugin ────── 위의 모든 것을 묶어서 팀에 공유
```

---

## 실전 체험한 3가지 데모

### 데모 1: Skill 실행 - `/weekly-sync`
- 한 마디로 복잡한 업무 자동화
- Slack 메시지 수집 → git log 확인 → 문서 생성까지 한 번에

### 데모 2: 모호한 요청 → AskUserQuestion으로 명확화
**Before**:
```
우리 팀 업무를 개선해줘
```
→ Claude가 혼자 추측해서 결과 내놓음

**After**:
```
우리 팀 업무를 개선해줘. 모호한 부분은 AskUserQuestion으로 질문해서 명확하게 만들어
```
→ Claude가 "어떤 팀인가요?", "몇 명인가요?", "가장 큰 병목은?" 등 선택지를 제시하며 질문

**핵심**: AskUserQuestion을 활용하면 Claude가 추측 대신 질문. 결과의 정확도가 완전히 달라짐.

### 데모 3: Claude에게 물어보기
```
Claude Code에서 MCP가 뭐야?
```
→ 기능을 다 외울 필요 없다. 모르면 Claude에게 물어보면 된다.

---

## 핵심 인사이트

### 1. 외우지 말고 체험하라
- 7가지 기능을 한 번에 외울 필요 없음
- 필요할 때마다 Claude에게 물어보면 됨
- Working Backward 방식으로 먼저 결과물을 보고, 원리는 나중에 이해

### 2. 컨텍스트 윈도우는 유한하다
- CLAUDE.md: 항상 로딩 (영구 기억)
- Skill: 점진적 로딩 (필요할 때만)
- Subagent: 프로세스 격리 (메인 컨텍스트 소비 안 함)
- Agent Teams: 각자 독립 컨텍스트 (병렬 작업)

### 3. AI의 한계를 코드로 보완
- AI는 확률적 → "대부분" 맞지만 100%는 아님
- Hook은 결정론적 → 코드 실행이므로 100% 확실
- 중요한 작업은 Hook으로 자동화

### 4. 모호함을 명확함으로
- 일반 요청: Claude가 혼자 추측
- AskUserQuestion 활용: Claude가 질문으로 명확화
- 결과의 정확도가 완전히 달라짐

---

## 실수 & 배운 점

### 실수 1: 한 번에 다 외우려고 함
**배운 점**: 외우지 말고 필요할 때 Claude에게 물어보기. 모르는 게 정상.

### 실수 2: CLAUDE.md와 Skill의 차이를 이해 못함
**배운 점**:
- CLAUDE.md = 영구 기억 (매번 로딩)
- Skill = 점진적 로딩 (필요할 때만)
- 컨텍스트 윈도우 절약이 핵심

### 실수 3: Subagent와 Agent Teams를 혼동
**배운 점**:
- Subagent = 부하 직원 (1:1 위임, 리더에게만 보고)
- Agent Teams = 프로젝트 팀 (팀원끼리 직접 소통 + 공유 태스크 리스트)

### 실수 4: Hook을 단순 자동화로만 생각함
**배운 점**: Hook은 AI의 확률성을 코드의 결정론으로 보완하는 도구. 100% 확실한 실행이 필요한 작업에 사용.

---

## 새로운 발견

### 1. Progressive Disclosure 설계 철학
- 모든 정보를 한 번에 주지 않음
- 필요한 순간에 필요한 지식만 로딩
- Skill, MCP, Subagent 모두 이 원칙을 따름

### 2. STOP PROTOCOL의 중요성
- Day 1 Onboarding의 핵심 규칙
- 각 블록을 반드시 2턴으로 나눔 (Phase A → Phase B)
- 한 턴에 너무 많은 정보를 주지 않음 = Progressive Disclosure의 실천

### 3. 점진적 학습 곡선
```
Block 0: Setup        → CLAUDE.md 이해
Block 1: Experience   → 결과물 먼저 체험
Block 2: Why          → CLI를 쓰는 이유
Block 3: What         → 7가지 기능 각각 체험
Block 4: Basics       → CLI + git + GitHub 기초
```
→ 난이도가 점진적으로 증가하도록 설계됨

### 4. 참고 문서의 구조화
- 각 reference 파일: `EXPLAIN` → `EXECUTE` → `QUIZ`
- 설명 → 실습 → 퀴즈 → 다음 블록
- 반복 학습 패턴

---

## 실전 적용 가능한 인사이트

### 1. 나만의 CLAUDE.md 만들기
- `/init`로 자동 생성 후 수정
- 개인 선호사항: "항상 존댓말로", "표로 정리해줘"
- 프로젝트 규칙: 코딩 컨벤션, 브랜치 전략 등

### 2. 반복 업무를 Skill로 만들기
- 매주/매일 하는 작업 찾기
- SKILL.md 하나로 시작
- 필요하면 scripts/, references/ 추가

### 3. MCP로 외부 도구 연결
- Slack, Gmail, Calendar 등 내가 쓰는 도구 파악
- MCP 서버 설치 및 연결
- Skill과 조합하여 자동화 워크플로우 구축

### 4. Hook으로 100% 확실한 자동화
- Stop Hook: 응답 완료 시 시간 출력, 요약 저장 등
- 파일 저장 Hook: 자동 포맷팅, 린트 등
- git Hook: 커밋 전 자동 검증 등

### 5. Plugin으로 팀 배포
- 내가 만든 Skill + MCP + Hook을 Plugin으로 패키징
- 팀원들에게 한 줄로 배포
- 동일한 개발 환경 구축

---

## 다음 스텝

### Day 2: Context Sync Skill 만들기
- MCP를 활용한 실전 Skill 제작
- LinkedIn, Gmail 등 외부 도구 연결
- 병렬 데이터 수집 및 출력 포맷 설계

### Day 3: Clarify Plugin 심화
- AskUserQuestion 패턴 마스터
- 모호한 요청을 명확하게 만드는 방법
- PRD(Product Requirements Document) 자동 생성

### Day 4: Session Wrap & Analyze
- 세션 자동 요약 Skill 제작
- History Insight로 세션 분석
- Session Analyzer로 패턴 발견

### Day 5: Fetch & Digest
- 트위터, YouTube 콘텐츠 가져오기
- 콘텐츠 다이제스트 생성
- Context Sync와 통합

---

## 공식 문서 링크

### 전체 기능 개요
- https://code.claude.com/docs/ko/features-overview

### 7가지 핵심 기능
1. CLAUDE.md: https://code.claude.com/docs/ko/memory
2. Skill: https://code.claude.com/docs/ko/skills
3. MCP: https://code.claude.com/docs/ko/mcp
4. Subagent: https://code.claude.com/docs/ko/sub-agents
5. Agent Teams: https://code.claude.com/docs/ko/agent-teams
6. Hook: https://code.claude.com/docs/ko/hooks-guide
7. Plugin: https://code.claude.com/docs/ko/plugins

### 기타 참고
- Quickstart: https://code.claude.com/docs/ko/quickstart
- Plugin 마켓플레이스: https://code.claude.com/docs/ko/discover-plugins
- AgentSkills.io: https://agentskills.io/what-are-skills

---

## 마무리

Day 1 Onboarding은 Claude Code의 7가지 핵심 기능을 체험하는 여정이었다. 중요한 건 외우는 게 아니라 필요할 때 꺼내 쓸 수 있는 능력을 키우는 것. 모르면 Claude에게 물어보면 된다. 이게 AI Native의 핵심이다.

> "전부 외울 필요 없다. 모르면 Claude에게 물어보면 된다."

---

**파일 위치**: `/Users/paddington/Project/practice/01_AI_Native_Camp/TIL_Day1_Onboarding.md`
