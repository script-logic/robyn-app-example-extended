# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass(frozen=True, slots=True, kw_only=True)
class LoggerConfig:
    app_name: str
    log_level: int
    date_format: str
    console_colors: bool
    console_pad_event_to: int
    enable_file_logging: bool
    logs_dir: Path
    logs_file_name: Path
    max_file_size_mb: int
    backup_count: int
    loggers_to_hijack: dict[str, Literal[0, 10, 20, 30, 40, 50]]
