from sqlalchemy.ext.asyncio import create_async_engine

from src.config import settings
from src.models import *
import pytest
from src.database import Base, engine, engine_null_pool
from httpx import AsyncClient

# meta = MetaData()
# Table("t1", meta, Column("name", String(50), primary_key=True))

@pytest.fixture(scope='session', autouse=True)
async def async_main() -> None:
    assert settings.MODE == 'TEST'

    async with engine_null_pool.begin() as conn:
      await conn.run_sync(Base.metadata.drop_all)
      await conn.run_sync(Base.metadata.create_all)