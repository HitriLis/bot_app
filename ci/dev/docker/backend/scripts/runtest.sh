#!/usr/bin/env sh
if command -v dockerize &> /dev/null; then
  dockerize -wait tcp://psql:5432 -timeout 120s
fi

if command -v alembic &> /dev/null; then
  alembic upgrade head
fi

if [ -d /var/app/src/static ]; then
  cp -r /var/app/src/static /var/app/
fi


if python3 -m pytest --doctest-modules --cov=. tests; then
  coverage xml
else
  exit 1
fi
