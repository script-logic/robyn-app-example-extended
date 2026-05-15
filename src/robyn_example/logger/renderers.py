# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT


import orjson
import structlog
from structlog.types import Processor

from .interfaces import LoggerConfig


def build_json_renderer() -> Processor:
    def orjson_serializer[**P](
        obj: object, *_args: P.args, **_kwargs: P.kwargs
    ) -> str:
        return orjson.dumps(
            obj,
            default=str,
            option=orjson.OPT_APPEND_NEWLINE,
        ).decode("utf-8")

    return structlog.processors.JSONRenderer(orjson_serializer)


def build_console_renderer(config: LoggerConfig) -> Processor:
    return structlog.dev.ConsoleRenderer(
        colors=config.console_colors,
        pad_event_to=config.console_pad_event_to,
    )
