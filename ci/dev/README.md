# ci/dev

Разворачивание проекта для разработки.

1. Создаем `.env` и настраиваем под окружение 
        
        cp .env.dist .env


2. Добавить ключи/токены  
  2.1 Найти в созданном файле переменные со значением:  
   `****** # @TODO Запросить у бэка или тимлида`.  
  2.2 Эти значения необходимо заменить на ключи, которые вам предоставит один из этих людей.


3. Запускаем проект 

        docker-compose up -d
---
## Переменные

В фейле `.env` есть переменные используемые в `docker-compose.yml`. Логика примерно такая:

- `COMPOSE_*` стандартные [переменные](https://docs.docker.com/compose/reference/envvars/) docker-compose
- `APP_*` общие переменные для всего приложения (например уровень лога, режим отладки внешний адрес для api) 
- `{SERVICE_IN_COMPOSE}_*` специфичные для какого-то сервиса, но требующие гибкой настройки через окружение
