#!/usr/bin/env bash
set -euo pipefail
# 1) Подтягиваем окружение (токены и т.п.)
set -a
[ -f "$HOME/.env" ] && . "$HOME/.env"
set +a
# 2) Нормальные пути для cron
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
cd "$(dirname "$0")"
# 3) Запуск планировщика вашего проекта
/usr/bin/python3 -m auto_updater.scheduler >> "$(pwd)/cron.log" 2>&1
