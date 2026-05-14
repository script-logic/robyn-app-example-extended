# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT


from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, func
from sqlalchemy.orm import (
    Mapped,
    configure_mappers,
    declarative_base,
    mapped_column,
)

Base = declarative_base()


class CrimesTable(Base):
    __tablename__ = "crimes"

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True, index=True
    )
    type: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)
    suspect_name: Mapped[str] = mapped_column(String)
    date_time: Mapped[datetime] = mapped_column(DateTime)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )


configure_mappers()
