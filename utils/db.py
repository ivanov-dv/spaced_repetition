from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool


class AlchemySqlDb:
    def __init__(
            self,
            sql_url,
            base: type[DeclarativeBase],
            test: bool = False
    ):
        self.metadata = base.metadata
        if test:
            self.engine = create_async_engine(
                sql_url,
                poolclass=NullPool,
                echo=False
            )
        else:
            self.engine = create_async_engine(sql_url, echo=False)
        self.SessionLocal = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def prepare(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.metadata.create_all)

    async def clean(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.metadata.drop_all)
            await conn.run_sync(self.metadata.create_all)
