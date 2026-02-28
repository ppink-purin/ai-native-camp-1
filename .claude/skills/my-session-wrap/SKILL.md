---
name: my-session-wrap
description: 세션 종료 시 작업 정리, 문서 업데이트, 학습 기록을 하는 스킬. "/wrap", "세션 정리", "마무리" 요청에 사용.
---

# My Session Wrap Skill

세션 종료 시 작업을 체계적으로 정리하고 분석하는 스킬입니다.

## Execution Flow

```
┌─────────────────────────────────────────────────────┐
│  1. Git 상태 확인                                    │
├─────────────────────────────────────────────────────┤
│  2. Phase 1: 4개 분석 에이전트 (병렬 실행)           │
│     ┌─────────────────┬─────────────────┐           │
│     │  doc-updater    │  automation-    │           │
│     │  (문서 업데이트)  │  scout          │           │
│     │                 │  (자동화 발견)    │           │
│     ├─────────────────┼─────────────────┤           │
│     │  learning-      │  followup-      │           │
│     │  extractor      │  suggester      │           │
│     │  (학습 정리)     │  (후속 작업)     │           │
│     └─────────────────┴─────────────────┘           │
├─────────────────────────────────────────────────────┤
│  3. Phase 2: 검증 에이전트 (순차 실행)               │
│     ┌───────────────────────────────────┐           │
│     │       duplicate-checker           │           │
│     │      (중복 검증 및 제거)           │           │
│     └───────────────────────────────────┘           │
├─────────────────────────────────────────────────────┤
│  4. 결과 통합 및 요약                                │
├─────────────────────────────────────────────────────┤
│  5. 사용자 선택 + 실행                               │
└─────────────────────────────────────────────────────┘
```

---

## Step 1: 변경 내용 확인

세션에서 수정된 파일과 변경 사항을 파악합니다.

### Git 상태 확인

```bash
git status --short
git diff --stat HEAD~3 2>/dev/null || git diff --stat
```

### 세션 요약 작성

다음 정보를 바탕으로 세션 요약을 작성합니다:

```
Session Summary:
- 주요 작업: [이 세션에서 수행한 주요 작업]
- 변경 파일: [생성/수정된 파일 목록]
- 주요 결정: [내린 주요 기술적 결정사항]
```

이 요약은 Phase 1의 모든 에이전트에게 공통으로 제공됩니다.

---

## Step 2: Phase 1 - 4개 분석 에이전트 (병렬 실행)

4개의 전문가 에이전트를 **동시에** 실행하여 세션을 다각도로 분석합니다.

### 병렬 실행 방법

단일 메시지에서 4개의 Task를 호출하여 병렬 실행합니다:

```
Task(
    subagent_type="doc-updater",
    description="문서 업데이트 분석",
    prompt="[Session Summary]

CLAUDE.md, context.md, README 등의 문서를 분석하여 업데이트가 필요한 부분을 찾아주세요.
구체적으로 추가할 내용을 제안해주세요."
)

Task(
    subagent_type="automation-scout",
    description="자동화 패턴 분석",
    prompt="[Session Summary]

이 세션에서 반복된 작업이나 패턴을 찾아주세요.
스킬, 스크립트, 또는 명령어로 자동화할 수 있는 부분을 제안해주세요."
)

Task(
    subagent_type="learning-extractor",
    description="학습 내용 추출",
    prompt="[Session Summary]

이번 세션에서 배운 점, 실수, 새로운 발견을 정리해주세요.
TIL(Today I Learned) 형식으로 요약해주세요."
)

Task(
    subagent_type="followup-suggester",
    description="후속 작업 제안",
    prompt="[Session Summary]

미완료된 작업과 다음 세션의 우선순위를 제안해주세요.
우선순위가 높은 작업부터 나열해주세요."
)
```

### 에이전트 역할

| 에이전트 | 역할 | 출력 형식 |
|---------|------|----------|
| **doc-updater** | CLAUDE.md, context.md 업데이트 분석 | 추가할 구체적 내용 |
| **automation-scout** | 자동화 가능한 패턴 탐지 | 스킬/명령어/스크립트 제안 |
| **learning-extractor** | 학습 내용 추출 | TIL 형식 요약 |
| **followup-suggester** | 후속 작업 제안 | 우선순위별 작업 목록 |

### 핵심 특징

- ✅ **병렬 실행**: 4개 에이전트가 동시에 작동 → 빠른 분석
- ✅ **독립적 분석**: 각 에이전트는 서로 의존하지 않음
- ✅ **공통 입력**: 모든 에이전트가 동일한 Session Summary를 받음

---

## Step 3: Phase 2 - 검증 에이전트 (순차 실행)

Phase 1의 결과를 검증하여 중복을 제거하고 품질을 높입니다.

### 실행 시점

⚠️ **Phase 1이 완료된 후**에 실행됩니다. Phase 1의 모든 결과가 있어야 비교가 가능하기 때문입니다.

### 순차 실행 방법

Phase 1의 4개 결과를 입력으로 받아 검증합니다:

```
Task(
    subagent_type="duplicate-checker",
    description="Phase 1 제안 검증",
    prompt="""
Phase 1 분석 결과를 검증합니다.

## doc-updater 제안:
[doc-updater 결과]

## automation-scout 제안:
[automation-scout 결과]

## learning-extractor 결과:
[learning-extractor 결과]

## followup-suggester 제안:
[followup-suggester 결과]

각 제안을 기존 문서/자동화와 비교하여 다음을 판단하세요:

1. **완전 중복 (Complete duplicate)**: 이미 존재함 → Skip 권장
2. **부분 중복 (Partial duplicate)**: 일부 겹침 → 병합 방법 제안
3. **신규 (No duplicate)**: 새로운 내용 → 추가 승인

각 제안에 대해 판단 결과와 권장사항을 제시하세요.
"""
)
```

### 검증 로직

| 중복 유형 | 판단 기준 | 권장 조치 |
|----------|----------|----------|
| **완전 중복** | 제안 내용이 이미 문서/코드에 존재 | Skip (건너뛰기) |
| **부분 중복** | 일부는 존재하고 일부는 새로운 내용 | 병합 방법 제안 |
| **신규** | 완전히 새로운 내용 | 추가 승인 |

### 왜 순차 실행인가?

Phase 1의 **모든 결과**를 받아야 서로 비교할 수 있습니다:
- doc-updater: "README 업데이트 필요"
- followup-suggester: "다음 세션에 README 수정"
- → duplicate-checker가 이 둘이 **같은 내용**임을 파악하고 중복 제거

### 핵심 특징

- ✅ **순차 실행**: Phase 1 완료 후 실행
- ✅ **의존성**: Phase 1의 4개 결과에 의존
- ✅ **품질 향상**: 중복 제거로 깔끔한 최종 결과

---

## Step 4: 결과 통합 및 요약

Phase 1과 Phase 2의 모든 결과를 통합하여 사용자에게 보여줍니다.

### 결과 요약 형식

```markdown
## 세션 정리 결과

### 📝 문서 업데이트
[doc-updater 요약]
- 검증 결과: [duplicate-checker 피드백]

### 🤖 자동화 제안
[automation-scout 요약]
- 검증 결과: [duplicate-checker 피드백]

### 💡 학습 내용
[learning-extractor 요약]

### 📋 후속 작업
[followup-suggester 요약]
```

---

## Step 5: 사용자 선택

AskUserQuestion을 사용하여 사용자가 실행할 작업을 선택하도록 합니다.

### 선택 옵션

```
AskUserQuestion(
    questions=[{
        "question": "어떤 작업을 수행할까요?",
        "header": "Wrap 옵션",
        "multiSelect": true,
        "options": [
            {
                "label": "커밋 생성 (추천)",
                "description": "변경사항을 커밋합니다"
            },
            {
                "label": "CLAUDE.md 업데이트",
                "description": "새로운 지식/워크플로우를 문서화합니다"
            },
            {
                "label": "자동화 생성",
                "description": "스킬/명령어/에이전트를 생성합니다"
            },
            {
                "label": "건너뛰기",
                "description": "작업 없이 종료합니다"
            }
        ]
    }]
)
```

**핵심**: `multiSelect: true` → 여러 작업을 동시에 선택 가능

### 사용자 경험

- ✅ **선택의 자유**: 필요한 작업만 선택
- ✅ **다중 선택**: 커밋 + 문서 업데이트를 동시에 가능
- ✅ **유연성**: 상황에 맞게 조정 가능

---

## Step 6: 선택된 작업 실행

사용자가 선택한 작업만 실행합니다.

### 실행 로직

```
if "커밋 생성" in 선택:
    - 변경사항을 git add
    - 커밋 메시지 작성 (세션 요약 기반)
    - git commit 실행

if "CLAUDE.md 업데이트" in 선택:
    - doc-updater 제안 내용을 CLAUDE.md에 추가
    - 파일 저장

if "자동화 생성" in 선택:
    - automation-scout 제안을 바탕으로 스킬/스크립트 생성
    - 필요한 파일 생성 및 설정

if "건너뛰기" in 선택:
    - 세션 종료 메시지 출력
```

### 핵심 원칙

- ✅ **선택된 것만 실행**: 불필요한 작업 방지
- ✅ **순차적 실행**: 선택된 작업을 순서대로 처리
- ✅ **완료 확인**: 각 작업 완료 시 피드백 제공

---

## 완성! 🎉

이제 `my-session-wrap` 스킬이 완성되었습니다.

### 스킬 구조 요약

1. **Frontmatter**: 스킬 이름과 설명
2. **Execution Flow**: 전체 흐름 다이어그램
3. **Step 1**: Git 상태 확인 및 세션 요약
4. **Step 2**: Phase 1 - 4개 병렬 에이전트
5. **Step 3**: Phase 2 - 검증 에이전트
6. **Step 4-6**: 결과 통합, 사용자 선택, 실행

### 다음 단계

Block 2에서 이 스킬을 실제로 실행하고 결과를 확인할 것입니다!
