import os
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    database_url: str = 'postgresql://user:secret@localhost:5432/x5_chat'
    app_debug: bool = False
    base_root: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    media_root: str = os.path.join(base_root, 'media')
    configs_root: str = os.path.join(base_root, 'configs')
    media_url: str = '/media/'
    static_url: str = '/static/'
    static_root: str = os.path.join(base_root, 'static')
    media_debug: bool = False
    database_pool_size: int = 1
    time_zone: str = 'Europe/Moscow'


    def validate(cls, val):
        return str(val).split(',')
    # pylint: enable=E0213

    class Config:
        env_file = '.env'


settings = Settings()

