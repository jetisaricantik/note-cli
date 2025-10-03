#!/usr/bin/env bash
set -euo pipefail

# 1) Подгружаем окружение
set -a
[ -f "$HOME/.env" ] && . "$HOME/.env"
set +a

# 2) Диагностика окружения
mkdir -p /root/note-cli
{
  echo "[$(date -Is)] DIAG: whoami=$(id -un) HOME=$HOME"
  echo "[$(date -Is)] DIAG: TOKEN_LEN=${#TELEGRAM_TOKEN} CHAT_ID=${TELEGRAM_CHAT_ID:-<empty>}"
  echo "[$(date -Is)] DIAG: PATH=$PATH"
} >> /root/note-cli/cron.log

# 3) Запуск планировщика
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
cd /root/note-cli
/usr/bin/python3 -m auto_updater.scheduler >> /root/note-cli/cron.log 2>&1
