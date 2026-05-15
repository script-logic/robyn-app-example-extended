# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from contextvars import ContextVar

from robyn import Robyn
from that_depends import BaseContainer, ContextScopes
from that_depends.providers import Singleton

from robyn_example.adapters import LoggerConfigAdapter
from robyn_example.config import AppConfig
from robyn_example.database import DatabaseManager
from robyn_example.logger import LoggerConfig


class RealContainer(BaseContainer):
    default_scope = ContextScopes.REQUEST
    request_id_ctx = Singleton(ContextVar[str], "request_id")
    cfg: Singleton[AppConfig] = Singleton(AppConfig)
    log_cfg: Singleton[LoggerConfig] = Singleton(
        LoggerConfigAdapter.create, cfg.cast
    )
    robyn_app: Singleton[Robyn] = Singleton(Robyn, __file__)
    db: Singleton[DatabaseManager] = Singleton(
        DatabaseManager,
        cfg.cast,
    )
