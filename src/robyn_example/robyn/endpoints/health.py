# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from robyn import SubRouter

from robyn_example.di import Ioc

app: SubRouter = Ioc.robyn_app.resolve_sync()


@app.get("/health", const=True)
def health_check() -> dict[str, str]:
    return {"status": "healthy", "version": "1.0.0"}
