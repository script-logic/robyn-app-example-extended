# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from pydantic import BaseModel


class ApplicationSettings(BaseModel):
    title: str = "Robyn Example"
    host: str = "127.0.0.1"
    port: int = 8082
    client_timeout_sec: int = 30
    keep_alive_timeout_sec: int = 20
