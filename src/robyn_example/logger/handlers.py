# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

import sys
from logging import Handler, StreamHandler
from logging.handlers import RotatingFileHandler

import orjson
import structlog
from structlog.types import Processor

from .interfaces import LoggerConfig


class HandlerBuilder:
    def __init__(
        self,
        logging_config: LoggerConfig,
    ) -> None:
        self.cfg = logging_config

    def build_console_renderer(
        self, shared_processors: list[Processor]
    ) -> Handler:
        renderer = structlog.dev.ConsoleRenderer(
            colors=self.cfg.console_colors,
            pad_event_to=self.cfg.console_pad_event_to,
        )
        console_formatter = structlog.stdlib.ProcessorFormatter(
            processor=renderer,
            foreign_pre_chain=shared_processors,
        )
        console_handler = StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        return console_handler

    def build_file_renderer(
        self, shared_processors: list[Processor]
    ) -> Handler:
        renderer = structlog.processors.JSONRenderer(
            lambda obj, **_kwargs: orjson.dumps(
                obj,
                default=str,
                option=orjson.OPT_APPEND_NEWLINE,
            ).decode("utf-8")
        )
        json_formatter = structlog.stdlib.ProcessorFormatter(
            processor=renderer,
            foreign_pre_chain=shared_processors,
        )
        log_file = self.cfg.logs_dir / self.cfg.logs_file_name
        log_file.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            filename=str(log_file),
            maxBytes=self.cfg.max_file_size_mb * 1024 * 1024,
            backupCount=self.cfg.backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(json_formatter)

        return file_handler

    def build_handlers_chain(
        self, shared_processors: list[Processor]
    ) -> list[Handler]:
        result: list[Handler] = []
        result.append(self.build_console_renderer(shared_processors))
        if self.cfg.enable_file_logging:
            result.append(self.build_file_renderer(shared_processors))
        return result
