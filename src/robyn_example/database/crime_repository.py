# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import CrimesTable


async def create_crime_repo(
    db_crime: CrimesTable,
    session: AsyncSession,
) -> CrimesTable:
    session.add(db_crime)
    await session.commit()
    await session.refresh(db_crime)
    return db_crime


async def get_crimes_repo(
    skip: int,
    limit: int,
    session: AsyncSession,
) -> list[CrimesTable]:
    result = await session.execute(
        select(CrimesTable).offset(skip).limit(limit)
    )
    return list(result.scalars().all())


async def get_crime_repo(
    crime_id: int,
    session: AsyncSession,
) -> CrimesTable | None:
    result = await session.execute(
        select(CrimesTable).where(CrimesTable.id == crime_id)
    )
    return result.scalars().first()


async def update_crime_repo(
    db_crime: CrimesTable,
    session: AsyncSession,
) -> CrimesTable:
    await session.commit()
    await session.refresh(db_crime)
    return db_crime


async def delete_crime_repo(
    db_crime: CrimesTable,
    session: AsyncSession,
) -> CrimesTable:
    await session.delete(db_crime)
    await session.commit()
    return db_crime
