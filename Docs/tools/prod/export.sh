#!/usr/bin/env bash
# Полная выгрузка прода для GTM и сверки дашборда. Сам подключается к бэкенду по SSH.
#
#   bash Docs/tools/prod/export.sh
#
# Что делает:
#   1. находит сервер через DNS api.kubysh.com (правило finik-backend docs/INFRA_TRUTH.md), проверяет SSH;
#   2. находит контейнер Postgres и проверяет, что витрина свежая (иначе это замороженная база);
#   3. выгружает таблицы в CSV (Docs/tools/prod/export/*.sql), сверку дашборда и GTM-срез в текст;
#   4. кладет все в ~/kubysh_prod_export/<дата_время>/ и архив .zip рядом. Архив прислать агенту.
#
# Только чтение: каждое подключение открывается с default_transaction_read_only=on.
# Почт, телефонов, имен, номеров заказов нет; id людей заменены на md5-префикс.
# Архив НЕ класть в репозиторий маркетоса: он публичный.
set -uo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
STAMP="$(date +%Y-%m-%d_%H%M)"
OUT="${OUT:-$HOME/kubysh_prod_export}/$STAMP"
mkdir -p "$OUT"
LOG="$OUT/_log.txt"

say() { echo "$*" | tee -a "$LOG"; }

# 1. Сервер
IP="${HOST_IP:-$(dig +short api.kubysh.com 2>/dev/null | grep -E '^[0-9.]+$' | tail -1)}"
# VPN и прокси с «фейковыми IP» подменяют DNS (240.x, 198.18.x, 10.x и т.п.) — такой адрес не сервер.
case "$IP" in
  ''|10.*|127.*|169.254.*|172.1[6-9].*|172.2[0-9].*|172.3[01].*|192.168.*|198.1[89].*|100.6[4-9].*|100.[7-9][0-9].*|100.1[01][0-9].*|100.12[0-7].*|2[4-5][0-9].*)
    [ -n "$IP" ] && echo "DNS вернул $IP — похоже на подмену VPN, беру адрес прода из INFRA_TRUTH"
    IP="201.24.56.21" ;;
esac
HOST="${HOST:-root@$IP}"
CM="$HOME/.ssh/cm-kubysh-%r@%h:%p"
SSH=(ssh -o BatchMode=yes -o ConnectTimeout=15 -o ControlMaster=auto -o ControlPath="$CM" -o ControlPersist=120 "$HOST")

say "Сервер: $HOST (api.kubysh.com → $IP)"
if [ "$IP" = "207.154.252.247" ]; then
  say "СТОП: это замороженный сервер (база от 27.08.2026). Нужен прод."; exit 1
fi
if ! "${SSH[@]}" true 2>>"$LOG"; then
  say "СТОП: SSH не пускает. Проверьте ключ: ssh $HOST"; exit 1
fi

# 2. Контейнер и свежесть
PG="$("${SSH[@]}" "docker ps --format '{{.Names}}' | grep -m1 postgres")"
[ -n "$PG" ] || { say "СТОП: контейнер postgres не найден"; exit 1; }
say "Postgres: $PG"

psql_remote() {  # $1 = доп. флаги psql; SQL на stdin
  "${SSH[@]}" "docker exec -i -e PGOPTIONS='-c default_transaction_read_only=on -c statement_timeout=300000' $PG \
    sh -c 'psql -X -q $1 -U \"\$POSTGRES_USER\" -d \"\$POSTGRES_DB\"'"
}

FRESH="$(echo "SELECT max(as_of_date) FROM mart_build_state" | psql_remote "-At")"
TODAY="$(TZ=Europe/Moscow date +%Y-%m-%d)"
say "Витрина на: $FRESH, сегодня: $TODAY"
[ "$FRESH" = "$TODAY" ] || say "ВНИМАНИЕ: витрина не сегодняшняя. Сырые таблицы актуальны, fct_* — на $FRESH."

# 3. Выгрузка
fail=0
for f in "$DIR"/export/*.sql; do
  name="$(basename "$f" .sql)"
  if psql_remote "-v ON_ERROR_STOP=1 --csv" < "$f" > "$OUT/$name.csv" 2>>"$LOG"; then
    say "  ok  $name.csv  $(($(wc -l < "$OUT/$name.csv") - 1)) строк"
  else
    say "  ОШИБКА  $name (подробности в _log.txt)"; fail=$((fail + 1))
  fi
done

for t in verify_dashboard gtm_snapshot; do
  psql_remote "" < "$DIR/$t.sql" > "$OUT/$t.txt" 2> "$OUT/$t.err"
  errs=$(grep -c ERROR "$OUT/$t.err")
  cat "$OUT/$t.err" >> "$LOG"; rm -f "$OUT/$t.err"
  if [ "$errs" = 0 ]; then say "  ok  $t.txt"
  else say "  ОШИБКА  $t.txt: $errs запросов упали (подробности в _log.txt)"; fail=$((fail + 1)); fi
done

"${SSH[@]}" -O exit 2>/dev/null || true

# 4. Архив
(cd "$(dirname "$OUT")" && zip -qr "$STAMP.zip" "$STAMP")
say ""
say "Готово: $OUT.zip  (ошибок: $fail)"
say "Сверка дашборда для глаз: $OUT/verify_dashboard.txt"
