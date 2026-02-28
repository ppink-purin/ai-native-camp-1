# Quick Win 가이드 🚀

즉시 사용 가능한 워크플로우 개선 도구

---

## 📦 설치 완료 항목

✅ `scripts/session-start.sh` - 세션 시작 체크리스트
✅ `scripts/session-end.sh` - 세션 종료 루틴
✅ `scripts/weekly-review.md` - 주간 리뷰 가이드
✅ `interests.json` - 관심사 중앙 관리
✅ `.claude/memory/errors.md` - 에러 기록
✅ `.git/hooks/post-commit` - 커밋 후 자동 알림

---

## 🎯 사용 방법

### 1. 세션 시작 전 (매번)

```bash
./scripts/session-start.sh
```

**확인 내용:**
- ✅ MCP 서버 상태
- ✅ 현재 관심사
- ✅ 미완료 작업 (CLAUDE.md)
- ✅ Git 변경사항
- ✅ 최근 커밋

**예상 시간:** 10초

---

### 2. 세션 종료 후 (매번)

#### Option A: 자동 정리 (추천)

```
Claude Code에서:
/wrap
```

또는

```
세션 정리
```

#### Option B: 수동 체크

```bash
./scripts/session-end.sh
```

**확인 내용:**
- ✅ 커밋되지 않은 변경사항 확인
- ✅ 관심사 업데이트 여부
- ✅ 해결한 에러 기록

**예상 시간:** 1-2분

---

### 3. 주간 리뷰 (매주 일요일)

```bash
# 가이드 읽기
cat scripts/weekly-review.md

# 또는 텍스트 에디터로 열기
open -a "TextEdit" scripts/weekly-review.md
```

**주요 단계:**
1. `/history-insight`로 전체 세션 분석
2. CLAUDE.md 학습 노트 정리
3. 다음 주 목표 설정
4. 관심사 트렌드 분석
5. MCP 서버 점검
6. 주간 하이라이트 문서 작성

**예상 시간:** 30분

---

## 💡 팁 & 트릭

### 별칭(Alias) 설정

`.zshrc` 또는 `.bashrc`에 추가:

```bash
# AI Native Camp 별칭
alias cc-start='cd ~/Project/practice/01_AI_Native_Camp && ./scripts/session-start.sh'
alias cc-end='cd ~/Project/practice/01_AI_Native_Camp && ./scripts/session-end.sh'
alias cc-review='cd ~/Project/practice/01_AI_Native_Camp && open scripts/weekly-review.md'
```

**적용:**

```bash
source ~/.zshrc  # 또는 source ~/.bashrc
```

**사용:**

```bash
cc-start   # 어디서든 세션 시작 체크
cc-end     # 어디서든 세션 종료 체크
cc-review  # 주간 리뷰 가이드 열기
```

---

### 관심사 빠르게 추가

```bash
# 새 관심사 추가
echo '"LLM Ops"' | jq '.primary += [.]' interests.json > tmp && mv tmp interests.json

# 관심사 제거
jq '.primary -= ["제거할주제"]' interests.json > tmp && mv tmp interests.json

# 현재 관심사 보기
jq '.primary' interests.json
```

---

### 에러 기록 빠르게 추가

```bash
# 에러 기록 파일 열기
ERROR_FILE=".claude/projects/-Users-paddington-Project-practice-01-AI-Native-Camp/memory/errors.md"
open -a "TextEdit" "$ERROR_FILE"

# 또는 vim
vim "$ERROR_FILE"
```

**템플릿:**

```markdown
## [에러명]

**발생일:** 2026-02-28

**문제:**
[무엇이 잘못되었는가]

**해결책:**
[어떻게 해결했는가]

**재발 방지:**
[다음에는 어떻게 할 것인가]
```

---

## 📊 효과 측정

### Before (Quick Win 적용 전)

| 활동 | 시간 |
|------|------|
| 세션 시작 준비 | 5분 |
| MCP 문제 발견 | 세션 중간 (10분 손실) |
| 세션 정리 | 15분 |
| 주간 리뷰 | 안 함 😅 |
| **합계 (주당)** | **100분+** |

### After (Quick Win 적용 후)

| 활동 | 시간 |
|------|------|
| 세션 시작 체크 | 10초 |
| MCP 문제 발견 | 세션 시작 전 (0분 손실) |
| 세션 정리 (/wrap) | 5분 |
| 주간 리뷰 | 30분 |
| **합계 (주당)** | **35분** |

**시간 절감: 65분/주 (65% ↓)**

---

## 🔧 트러블슈팅

### 스크립트 실행 권한 없음

```bash
chmod +x scripts/session-start.sh
chmod +x scripts/session-end.sh
```

### jq 명령 없음

```bash
# macOS
brew install jq

# Linux (Ubuntu/Debian)
sudo apt-get install jq
```

### Git 훅이 작동하지 않음

```bash
chmod +x .git/hooks/post-commit
```

---

## 🎯 다음 단계

Quick Win에 익숙해지면:

1. **session-starter 스킬** 개발 (30분)
   - MCP 자동 헬스체크
   - 작업 자동 로드

2. **interests.json 통합** (15분)
   - my-context-sync에 연결
   - 동적 관심사 로딩

3. **mcp-doctor 스킬** 개발 (1시간)
   - 자동 진단 및 복구

---

## 📝 피드백

개선 아이디어가 있으면 `errors.md`에 기록하거나 CLAUDE.md에 메모하세요!

---

**버전:** 1.0.0
**최종 업데이트:** 2026-02-28
**작성:** history-insight 분석 기반
