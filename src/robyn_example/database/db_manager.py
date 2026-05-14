# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from robyn_example.config import AppConfig
from robyn_example.logger import log

from .models import Base


class SessionError(Exception): ...


class DatabaseManager:
    def __init__(self, cfg: AppConfig) -> None:
        self.engine = create_async_engine(
            url=cfg.db.db_path,
            pool_size=cfg.db.pool_size,
            max_overflow=cfg.db.max_overflow,
            echo=cfg.db.echo,
        )
        self.SessionFactory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=cfg.db.expire_on_commit,
        )

    @property
    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession]:
        session = self.SessionFactory()
        try:
            yield session
        except Exception:
            await session.rollback()
            await log.aexception("Database session error")
            raise
        finally:
            await session.close()

    async def health_check(self) -> bool:
        try:
            async with self.engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            await log.ainfo("Database health check success")
        except SessionError:
            await log.aexception("Database health check failed")
            return False
        else:
            return True

    async def init_db(self) -> None:
        async with self.engine.begin() as conn:
            result = await conn.execute(text("PRAGMA journal_mode=WAL"))
            await conn.execute(text("PRAGMA synchronous=NORMAL"))
            await conn.execute(text("PRAGMA cache_size=-64000"))
            await conn.execute(text("PRAGMA busy_timeout=5000"))
            await conn.execute(text("PRAGMA foreign_keys=ON"))
            mode = result.scalar()
            await log.ainfo("SQLite journal mode: %s", mode)
            await conn.run_sync(Base.metadata.create_all)
        await log.ainfo("Database tables created")

    async def dispose(self) -> None:
        await self.engine.dispose()
        await log.ainfo("Database connections disposed")
