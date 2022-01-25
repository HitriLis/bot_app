import databases
from sqlalchemy.ext.declarative import declarative_base

from settings import settings


database = databases.Database(
    settings.database_url.replace('postgres://', 'postgresql+aiopg://').replace('postgresql://', 'postgresql+aiopg://'),
    min_size=settings.database_pool_size,
    max_size=settings.database_pool_size
)
Base = declarative_base()


