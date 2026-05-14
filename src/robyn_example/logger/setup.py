# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

import logging
from logging import Handler

import structlog
from structlog.stdlib import get_logger
from that_depends import Provide, inject

from robyn_example.di import Ioc

from .handlers import HandlerBuilder
from .interfaces import LoggerConfig
from .processors import ProcessorBuilder


@inject
def setup_logging(cfg: LoggerConfig = Provide[Ioc.log_cfg]) -> None:
    handler_builder = HandlerBuilder(cfg)
    processor_builder = ProcessorBuilder(cfg)

    shared_processors = processor_builder.build_shared_chain()
    handlers: list[Handler] = handler_builder.build_handler_chain(
        shared_processors
    )

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    root_logger = logging.getLogger()
    root_logger.handlers = handlers
    root_logger.setLevel(cfg.log_level)

    for (
        third_party_logger_name,
        logger_lvl,
    ) in cfg.loggers_to_hijack.items():
        logger = logging.getLogger(third_party_logger_name)
        logger.handlers.clear()
        logger.propagate = True
        logger.setLevel(logger_lvl)


log = get_logger()
