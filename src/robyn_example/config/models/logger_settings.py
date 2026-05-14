# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

import logging
from typing import Literal

from pydantic import BaseModel, model_validator

LogLevel = Literal[0, 10, 20, 30, 40, 50]


class LoggerSettings(BaseModel):
    date_format: str = "%Y-%m-%d %H:%M:%S"
    console_colors: bool = True
    enable_file_logging: bool = True
    console_pad_event_to: int = 20
    log_level: LogLevel = logging.DEBUG
    loggers_to_hijack: dict[str, LogLevel] = {
        "sqlalchemy": logging.INFO,
        "robyn": logging.INFO,
        "pydantic": logging.DEBUG,
        "that_depends": logging.DEBUG,
        "aiosqlite": logging.INFO,
        "pydantic_settings": logging.DEBUG,
        "actix_server": logging.DEBUG,
        "asyncio": logging.INFO,
    }
    uniform_hijacked_loggers_level: bool = False
    hijacked_loggers_level: LogLevel | None = None

    @model_validator(mode="after")
    def apply_hijacked_level(self) -> LoggerSettings:
        if (
            self.uniform_hijacked_loggers_level
            and self.hijacked_loggers_level is not None
        ):
            self.loggers_to_hijack = dict.fromkeys(
                self.loggers_to_hijack,
                self.hijacked_loggers_level,
            )
        return self
