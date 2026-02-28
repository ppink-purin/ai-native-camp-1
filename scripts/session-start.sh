#!/bin/bash
# 세션 시작 체크리스트
# 사용법: ./scripts/session-start.sh

echo "🚀 Claude Code 세션 시작 체크"
echo "======================================"
echo ""

# 1. MCP 서버 상태 확인
echo "📡 [1/4] MCP 서버 상태 확인..."
if command -v claude &> /dev/null; then
  claude mcp list 2>/dev/null || echo "⚠️  claude CLI 사용 불가 - .mcp.json 파일로 수동 확인 필요"
else
  echo "ℹ️  MCP 서버 설정 (.mcp.json):"
  if [ -f .mcp.json ]; then
    jq -r '.mcpServers | keys[]' .mcp.json 2>/dev/null | while read server; do
      echo "   ✓ $server"
    done
  else
    echo "   ❌ .mcp.json 파일 없음"
  fi
fi
echo ""

# 2. 관심사 확인
echo "💡 [2/4] 현재 관심사..."
if [ -f interests.json ]; then
  echo "   Primary:"
  jq -r '.primary[]' interests.json 2>/dev/null | while read interest; do
    echo "     • $interest"
  done

  LAST_UPDATED=$(jq -r '.lastUpdated' interests.json 2>/dev/null)
  echo "   (최종 업데이트: $LAST_UPDATED)"

  # 3일 이상 업데이트 안 된 경우 알림
  if [ ! -z "$LAST_UPDATED" ]; then
    DAYS_AGO=$(( ($(date +%s) - $(date -j -f "%Y-%m-%d" "$LAST_UPDATED" +%s 2>/dev/null || echo 0)) / 86400 ))
    if [ $DAYS_AGO -gt 3 ]; then
      echo "   ⚠️  관심사가 ${DAYS_AGO}일 전 업데이트됨 - 변경 필요시 interests.json 수정"
    fi
  fi
else
  echo "   ⚠️  interests.json 파일 없음"
  echo "   💡 추천: interests.json 파일을 생성하여 관심사를 관리하세요"
fi
echo ""

# 3. 미완료 작업 확인
echo "📋 [3/4] 미완료 작업 (CLAUDE.md)..."
if [ -f CLAUDE.md ]; then
  INCOMPLETE=$(grep -E "⏳|🔄" CLAUDE.md | head -5)
  if [ -z "$INCOMPLETE" ]; then
    echo "   ✅ 미완료 작업 없음"
  else
    echo "$INCOMPLETE" | while read line; do
      echo "   $line"
    done
  fi

  echo ""
  echo "   📌 다음 단계 (CLAUDE.md):"
  sed -n '/## 다음 단계/,/^##/p' CLAUDE.md | grep -E "^-" | head -3 | while read line; do
    echo "   $line"
  done
else
  echo "   ⚠️  CLAUDE.md 파일 없음"
fi
echo ""

# 4. Git 상태 확인
echo "🔧 [4/4] Git 상태..."
if git rev-parse --git-dir > /dev/null 2>&1; then
  # Uncommitted changes
  CHANGED=$(git status --porcelain | wc -l | tr -d ' ')
  if [ "$CHANGED" -gt 0 ]; then
    echo "   ⚠️  변경된 파일: $CHANGED개"
    git status --short | head -5
    if [ "$CHANGED" -gt 5 ]; then
      echo "   ... (외 $(($CHANGED - 5))개)"
    fi
  else
    echo "   ✅ 변경사항 없음 (clean)"
  fi

  # Recent commits
  echo ""
  echo "   📝 최근 커밋:"
  git log -3 --oneline --decorate | while read line; do
    echo "      $line"
  done
else
  echo "   ⚠️  Git 저장소 아님"
fi

echo ""
echo "======================================"
echo "✨ 체크 완료! Claude Code를 시작하세요."
echo ""

# 관심사 변경 여부 확인 (선택사항)
read -p "관심사를 변경하시겠습니까? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  echo "💡 interests.json 파일을 열어서 수정하세요:"
  echo "   vim interests.json"
  echo "   또는"
  echo "   open -e interests.json"
fi
