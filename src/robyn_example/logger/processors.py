# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

import structlog
from structlog.stdlib import BoundLogger
from structlog.types import EventDict, Processor

from .interfaces import LoggerConfig


class ProcessorBuilder:
    def __init__(
        self,
        logging_config: LoggerConfig,
        additional_processors: list[Processor] | None = None,
    ) -> None:
        self.logging_config = logging_config
        self.additional_processors = additional_processors or []

    def build_base_chain(self) -> list[Processor]:
        return [
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(
                fmt=self.logging_config.date_format
            ),
            structlog.processors.CallsiteParameterAdder([
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.QUAL_NAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.THREAD_NAME,
                structlog.processors.CallsiteParameter.PROCESS_NAME,
            ]),
            structlog.processors.StackInfoRenderer(),
        ]

    def build_shared_chain(self) -> list[Processor]:
        chain = self.build_base_chain()
        chain.append(clean_log_message)
        chain.extend(self.additional_processors)
        return chain


def clean_log_message(
    _logger: BoundLogger, _method_name: str, event_dict: EventDict
) -> EventDict:
    if event := event_dict.get("event"):
        event_dict["event"] = (
            str(event)
            .strip()
            .replace("\x1b[92m", "")
            .replace("\x1b[93m", "")
            .replace("\x1b[94m", "")
            .replace("\x1b[0m", "")
        )
    return event_dict
