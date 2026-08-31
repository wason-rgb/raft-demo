#!/bin/bash
# 一键把本地源码推到 GitHub，触发云端构建 + 蒲公英自动分发
# Usage: bash push.sh "commit message"

set -e
COMMIT_MSG="${1:-feat: update raft demo}"
cd "$(dirname "$0")"

git init 2>/dev/null || true
git add .
git commit -m "$COMMIT_MSG" --allow-empty 2>/dev/null || git commit -m "$COMMIT_MSG" 2>/dev/null || echo "nothing to commit"
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/wason-rgb/raft-demo.git
git push -u origin main --force

echo ""
echo "✅ 推送完成，查看构建进度："
echo "  https://github.com/wason-rgb/raft-demo/actions"
echo ""
echo "📦 构建成功后会自动上传到蒲公英："
echo "  https://www.pgyer.com"
