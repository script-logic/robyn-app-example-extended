# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from dataclasses import dataclass

from robyn_example.config import AppConfig
from robyn_example.logger import LoggerConfig


@dataclass(frozen=True, slots=True, kw_only=True)
class LoggerConfigAdapter(LoggerConfig):
    @classmethod
    def create(cls, cfg: AppConfig) -> LoggerConfig:
        return cls(
            app_name=cfg.app.title,
            log_level=cfg.log.log_level,
            date_format=cfg.log.date_format,
            console_colors=cfg.log.console_colors,
            console_pad_event_to=cfg.log.console_pad_event_to,
            enable_file_logging=cfg.log.enable_file_logging,
            logs_dir=cfg.filesys.logs_dir,
            logs_file_name=cfg.filesys.logs_file_name,
            max_file_size_mb=cfg.filesys.max_log_file_size_mb,
            backup_count=cfg.filesys.log_backup_count,
            loggers_to_hijack=cfg.log.loggers_to_hijack,
        )
