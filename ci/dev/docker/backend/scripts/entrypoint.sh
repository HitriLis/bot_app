#!/usr/bin/env sh

set -e

# Ожидаем запуска postgres и tarantool
DB_HOST=`echo ${DSN__DATABASE} | sed -r 's/.*@([^:]+):.*/\1/'`
DB_PORT=`echo ${DSN__DATABASE} | sed -e 's,^.*:,:,g' -e 's,.*:\([0-9]*\).*,\1,g' -e 's,[^0-9],,g'`

# Миграция и синхронизация
alembic upgrade head

cp -r /var/app/src/static /var/app/

# Запуск команды
#uvicorn main:app --reload --host 0.0.0.0 --port 8000
#hypercorn main:app --reload --bind 0.0.0.0:8000 --keep-alive 15
hypercorn main:app --bind 0.0.0.0:8000 --workers 5 --backlog 500 --keep-alive 15
