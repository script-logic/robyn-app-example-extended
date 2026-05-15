# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from pydantic import BaseModel, Field


class SqliteSettings(BaseModel):
    db_schema: str = "sqlite+aiosqlite"
    db_dir: str = Field(default="./local_database", min_length=1)
    db_name: str = Field(default="database.db", min_length=1)
    pool_size: int = 3
    max_overflow: int = 3
    echo: bool = False
    expire_on_commit: bool = False

    @property
    def db_path(self) -> str:
        return f"{self.db_schema}:///{self.db_dir}/{self.db_name}"
