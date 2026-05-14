# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .models import (
    ApplicationSettings,
    CORSSettings,
    FilesystemSettings,
    LoggerSettings,
    SqliteSettings,
)


class AppConfig(BaseSettings):
    db: SqliteSettings = Field(default_factory=SqliteSettings)
    cors: CORSSettings = Field(default_factory=CORSSettings)
    log: LoggerSettings = Field(default_factory=LoggerSettings)
    filesys: FilesystemSettings = Field(default_factory=FilesystemSettings)
    app: ApplicationSettings = Field(default_factory=ApplicationSettings)

    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE_NAME", ".env.test"),
        secrets_dir=os.getenv("SECRETS_DIR", "/run/secrets"),
        env_nested_delimiter="__",
        case_sensitive=False,
        frozen=True,
    )
