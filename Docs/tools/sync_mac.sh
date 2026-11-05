#!/usr/bin/env bash
# Подтянуть ветку агента на Mac, не трогая основную папку и ваши локальные правки.
#   bash Docs/tools/sync_mac.sh            — из папки репозитория маркетоса
# Ветка кладется в папку рядом: ../kubysh-gtm (git worktree). Повторный запуск обновляет ее до свежей версии.
set -euo pipefail
BRANCH="${1:-claude/jolly-noether-pgpg7d}"
WT="${WT:-../kubysh-gtm}"
git fetch origin "$BRANCH"
if git worktree list | grep -q "$(cd "$(dirname "$WT")" && pwd)/$(basename "$WT")"; then
  git -C "$WT" checkout -q --detach "origin/$BRANCH"
else
  git worktree add -q --detach "$WT" "origin/$BRANCH"
fi
echo "Готово: $(cd "$WT" && pwd) на $(git -C "$WT" log --oneline -1)"
echo "Стратегия: $WT/Docs/strategy/GTM_2026-11.md"
echo "Серия постов: $WT/Docs/publications/85_Growth_story_05.11.md"
