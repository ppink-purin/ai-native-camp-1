#!/bin/bash
# 세션 종료 루틴
# 사용법: ./scripts/session-end.sh

echo "🏁 Claude Code 세션 종료 체크"
echo "======================================"
echo ""

# 1. Git 상태 확인
echo "📝 [1/3] 변경사항 확인..."
if git rev-parse --git-dir > /dev/null 2>&1; then
  CHANGED=$(git status --porcelain | wc -l | tr -d ' ')

  if [ "$CHANGED" -gt 0 ]; then
    echo "   ⚠️  커밋되지 않은 변경사항: $CHANGED개"
    echo ""
    git status --short
    echo ""

    read -p "지금 /wrap을 실행하시겠습니까? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      echo "💡 Claude Code에서 다음 명령을 실행하세요:"
      echo "   /wrap"
      echo ""
      echo "   또는"
      echo "   세션 정리"
      exit 0
    fi
  else
    echo "   ✅ 모든 변경사항 커밋됨"
  fi
else
  echo "   ⚠️  Git 저장소 아님"
fi
echo ""

# 2. 관심사 업데이트 확인
echo "💡 [2/3] 관심사 업데이트..."
if [ -f interests.json ]; then
  LAST_UPDATED=$(jq -r '.lastUpdated' interests.json 2>/dev/null)
  TODAY=$(date +%Y-%m-%d)

  if [ "$LAST_UPDATED" != "$TODAY" ]; then
    echo "   ℹ️  마지막 업데이트: $LAST_UPDATED"
    echo ""
    read -p "오늘 새로운 관심사가 생겼나요? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      read -p "추가할 관심사를 입력하세요: " NEW_INTEREST

      # interests.json에 추가
      jq --arg interest "$NEW_INTEREST" --arg date "$TODAY" \
        '.primary += [$interest] | .lastUpdated = $date' \
        interests.json > tmp.json && mv tmp.json interests.json

      echo "   ✅ '$NEW_INTEREST' 추가됨"
      echo "   📄 업데이트된 관심사:"
      jq -r '.primary[]' interests.json | while read i; do
        echo "      • $i"
      done
    fi
  else
    echo "   ✅ 오늘 이미 업데이트됨"
  fi
else
  echo "   ⚠️  interests.json 파일 없음"
fi
echo ""

# 3. 에러 기록 확인
echo "🐛 [3/3] 에러 기록..."
ERROR_FILE=".claude/projects/-Users-paddington-Project-practice-01-AI-Native-Camp/memory/errors.md"

if [ ! -f "$ERROR_FILE" ]; then
  echo "   ℹ️  에러 기록 파일이 없습니다."
fi

echo ""
read -p "오늘 해결한 에러가 있나요? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  read -p "에러명을 입력하세요: " ERROR_NAME
  read -p "해결책을 간단히 입력하세요: " ERROR_SOLUTION

  # 에러 기록 파일에 추가
  mkdir -p "$(dirname "$ERROR_FILE")"
  cat >> "$ERROR_FILE" << EOF

---

## $ERROR_NAME

**발생일:** $(date +%Y-%m-%d)

**해결책:**
$ERROR_SOLUTION

EOF

  echo "   ✅ 에러 기록 완료: $ERROR_FILE"
fi

echo ""
echo "======================================"
echo "✨ 세션 종료 체크 완료!"
echo ""
echo "📊 요약:"
echo "   • Git 상태: $([ "$CHANGED" -gt 0 ] && echo "⚠️  커밋 필요" || echo "✅ Clean")"
echo "   • 관심사: $([ -f interests.json ] && jq -r '.primary | length' interests.json 2>/dev/null || echo "0")개"
echo "   • 다음 세션: CLAUDE.md의 '다음 단계' 참고"
echo ""
echo "좋은 하루 되세요! 👋"
