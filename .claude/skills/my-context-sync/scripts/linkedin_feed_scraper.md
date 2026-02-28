# LinkedIn 피드 스크래핑 가이드

이 파일은 Puppeteer MCP를 사용하여 LinkedIn 피드를 수집하는 방법을 설명합니다.

## 개요

**목표:**
- LinkedIn 피드(타임라인)에서 최근 게시물 수집
- AI가 각 게시물을 분석하여 유용한 글 추천
- 추천 이유와 함께 정리된 리스트 제공

## 워크플로우

```
1. Puppeteer MCP로 LinkedIn 접속
   ↓
2. 로그인 (자동 또는 수동)
   ↓
3. 피드 페이지 이동 (https://www.linkedin.com/feed/)
   ↓
4. 스크롤하며 게시물 수집 (최근 20-50개)
   ↓
5. 각 게시물에서 추출:
   - 작성자 이름/직책
   - 게시물 본문
   - 링크/이미지
   - 반응 수 (좋아요, 댓글)
   ↓
6. Claude AI가 각 게시물 분석:
   - 내 관심사와 관련성 (1-10점)
   - 유용성 평가
   - 한 줄 요약
   - 추천 이유
   ↓
7. 점수 높은 순으로 정렬
   ↓
8. TOP 10 추천 리스트 출력
```

## Puppeteer MCP 도구 사용법

MCP 서버가 제공하는 주요 도구:

### 1. puppeteer_navigate

```
페이지 이동
  URL: https://www.linkedin.com/feed/
```

### 2. puppeteer_screenshot

```
현재 화면 스크린샷 (로그인 확인용)
```

### 3. puppeteer_click

```
요소 클릭 (로그인 버튼, 더보기 등)
  selector: CSS 선택자
```

### 4. puppeteer_fill

```
입력 필드 채우기 (로그인 정보)
  selector: CSS 선택자
  value: 입력 값
```

### 5. puppeteer_evaluate

```
JavaScript 실행하여 데이터 추출
  script: 실행할 JavaScript 코드
```

## LinkedIn 피드 수집 예시

### Phase 1: 로그인

**옵션 A: 수동 로그인 (추천)**
```
1. Puppeteer로 LinkedIn 접속
2. 스크린샷으로 로그인 페이지 확인
3. 사용자가 수동으로 로그인
4. 로그인 완료 후 계속
```

**옵션 B: 자동 로그인 (환경변수 필요)**
```
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
```
⚠️ 보안상 수동 로그인을 추천합니다.

### Phase 2: 피드 수집

```javascript
// JavaScript 코드 (puppeteer_evaluate로 실행)
const posts = [];
const postElements = document.querySelectorAll('.feed-shared-update-v2');

for (let i = 0; i < Math.min(postElements.length, 20); i++) {
  const post = postElements[i];

  // 작성자 정보
  const author = post.querySelector('.update-components-actor__name')?.innerText || '';
  const title = post.querySelector('.update-components-actor__description')?.innerText || '';

  // 게시물 본문
  const content = post.querySelector('.feed-shared-update-v2__description')?.innerText || '';

  // 반응 수
  const reactions = post.querySelector('.social-details-social-counts__reactions-count')?.innerText || '0';
  const comments = post.querySelector('.social-details-social-counts__comments')?.innerText || '0';

  // 링크
  const link = post.querySelector('.app-aware-link')?.href || '';

  posts.push({
    author,
    title,
    content,
    reactions,
    comments,
    link,
    timestamp: new Date().toISOString()
  });
}

return posts;
```

### Phase 3: AI 분석

각 게시물에 대해 Claude가 분석:

```
분석 항목:
1. 관련성 점수 (1-10)
   - 내 관심사 키워드 매칭
   - 주제 적합성

2. 유용성 평가
   - 실용적인 정보인가?
   - 새로운 인사이트가 있는가?
   - 실행 가능한 조언이 있는가?

3. 한 줄 요약
   - 핵심 메시지를 20자 이내로

4. 추천 이유
   - 왜 이 글이 유용한지 설명
```

## 출력 형식

```markdown
# LinkedIn 피드 추천 - 2026-02-27

> AI가 분석한 오늘의 유용한 글 TOP 10

## 🥇 추천 #1: [제목]

**작성자:** 홍길동 (ABC 회사 CTO)
**점수:** 9.5/10
**요약:** AI 인프라 구축 시 주의할 3가지 함정

**추천 이유:**
실무에서 바로 적용 가능한 구체적인 조언. GPU 비용 최적화 사례 포함.

**링크:** [게시물 보기](https://linkedin.com/...)

**본문 미리보기:**
> "많은 팀이 처음부터 큰 GPU 인스턴스를 사용하지만, 실제로는..."

---

## 🥈 추천 #2: [제목]
...
```

## 실행 방법

스킬 실행 시:
1. Puppeteer MCP 도구를 사용하여 LinkedIn 접속
2. 피드 데이터 수집
3. Claude AI가 실시간으로 분석
4. 추천 리스트 생성

**명령어:**
```
"싱크", "sync", "정보 수집"
```

## 주의사항

1. **로그인 유지**: 세션이 만료되면 재로그인 필요
2. **속도 제한**: LinkedIn이 봇으로 인식하지 않도록 적절한 딜레이 필요
3. **개인정보**: 수집된 데이터는 로컬에만 저장됨
4. **이용약관**: LinkedIn 이용약관을 준수하세요

## 커스터마이징

### 관심사 키워드 설정

```yaml
interests:
  - "AI/ML"
  - "스타트업"
  - "개발 문화"
  - "리더십"
```

스킬 실행 시 이 키워드와 관련된 게시물에 높은 점수 부여.

### 수집 개수 조정

기본 20개 → 원하는 개수로 변경 가능 (max 100개 권장)
