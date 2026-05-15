# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from that_depends import BaseContainer
from that_depends.experimental import LazyProvider

REAL_IOC_PATH = "robyn_example.di._real_ioc.RealContainer"


class LazyProviderDescriptor:
    def __set_name__(self, owner: type, name: str) -> None:
        self.provider_name = name
        self.path = f"{REAL_IOC_PATH}.{self.provider_name}"

    def __get__(self, obj: object, objtype: type) -> LazyProvider:
        if not hasattr(self, "_cached_provider"):
            self._cached_provider = LazyProvider(self.path)
        return self._cached_provider


class ProxyContainer(BaseContainer):
    request_id_ctx = LazyProviderDescriptor()
    cfg = LazyProviderDescriptor()
    log_cfg = LazyProviderDescriptor()
    robyn_app = LazyProviderDescriptor()
    db = LazyProviderDescriptor()
