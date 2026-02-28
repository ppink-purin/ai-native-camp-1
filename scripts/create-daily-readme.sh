#!/bin/bash
# Day X 실습 README.md 자동 생성 스크립트
# 사용법: ./scripts/create-daily-readme.sh [Day 번호]

# Day 번호 (기본값: 1)
DAY_NUMBER=${1:-1}

# 사용자 정보
USER_NAME="까망퓨린"

# 현재 날짜
TODAY=$(date +%Y-%m-%d)

# README.md 생성
cat > README.md <<EOF
# Day ${DAY_NUMBER} 실습

**이름:** ${USER_NAME}
**날짜:** ${TODAY}

## 목표

[작성 필요]

## 진행 상황

- [ ] 과제 1
- [ ] 과제 2
- [ ] 과제 3

## 학습 내용

[작성 필요]

## 참고 자료

- \`CLAUDE.md\` - 프로젝트 컨텍스트
- \`.agents/skills/day${DAY_NUMBER}-*/SKILL.md\` - 해당 Day 스킬 가이드

EOF

echo "✅ README.md 생성 완료 (Day ${DAY_NUMBER})"
echo "📝 파일 위치: $(pwd)/README.md"
