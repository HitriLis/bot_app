#!/usr/bin/env bash

# Скрипт делает простой смоук тест системы
# Вначаале проверяем что все нужные для проекта контейнеры запущены
for service in $(docker-compose ps --services)
do
  echo "Check $service status..."
  if [ -z `docker-compose ps -q $service` ] || [ -z `docker ps -q --no-trunc | grep $(docker-compose ps -q $service)` ]; then
    echo "Fail! Not running service: $service"
    docker-compose logs --tail 100 $service
    echo "Exit!"
    exit 255
  else
    echo "OK! Service $service up..."
  fi
done

