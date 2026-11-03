#!/usr/bin/env bash
# Срез прода для GTM. Запускать со своего Mac из корня репозитория маркетоса:
#   bash Docs/tools/prod/gtm_snapshot.sh
# Результат: gtm_snapshot_<дата>.txt в текущей папке. Его и прислать агенту.
# Только чтение (BEGIN READ ONLY ... ROLLBACK), персональных данных в выводе нет.
set -euo pipefail

HOST="${HOST:-root@201.24.56.21}"   # сверить с finik-backend docs/INFRA_TRUTH.md: dig +short api.kubysh.com
OUT="gtm_snapshot_$(date +%Y-%m-%d).txt"
SQL="$(dirname "$0")/gtm_snapshot.sql"

ssh "$HOST" '
  C=$(docker ps --format "{{.Names}}" | grep -m1 postgres)
  echo "контейнер: $C"
  docker exec -i "$C" sh -c "psql -X -U \"\$POSTGRES_USER\" -d \"\$POSTGRES_DB\""
' < "$SQL" > "$OUT" 2>&1

echo "Готово: $OUT ($(wc -l < "$OUT") строк)"
grep -n -i "error\|ошибка" "$OUT" | head -5 || true
