# Alembic

Для миграции базы данных используется [alembic](https://alembic.sqlalchemy.org).

Для создания миграции используется такой workflow

1. Редактируем модели в `app/backend/src/models`
2. Запускаем генерацию файлов миграции 

        cd app/backend/src
        alembic revision --autogenerate -m 'Migrations comment'

3. После этого можно успешно применить миграцию
    
        alembic upgrade head
