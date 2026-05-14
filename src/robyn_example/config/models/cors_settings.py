# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from pydantic import BaseModel


class CORSSettings(BaseModel):
    allow_origins: list[str] = [
        "http://localhost:8000",
        "http://localhost:8080",
        "http://localhost:8081",
        "http://localhost:8082",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8081",
        "http://127.0.0.1:8082",
    ]
    allow_headers: list[str] = [
        "Content-Type",
        "Accept",
        "Origin",
        "X-Requested-With",
        "Authorization",
    ]
