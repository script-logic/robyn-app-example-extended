# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from datetime import datetime

from pydantic import BaseModel, Field


class CrimeEntity(BaseModel):
    type: str = Field(default="Laugh")
    description: str = Field(default="Very long")
    location: str = Field(default="Gotham")
    suspect_name: str = Field(default="Jocker")
    date_time: datetime = Field(default=...)
    latitude: float = Field(default=24.5)
    longitude: float = Field(default=-12.8)


class RequestMiddlewareEntity(BaseModel):
    query_params: dict[str, list[str]]
    headers: str
    path_params: dict[str, str]
    body: str | bytes
    method: str
    url: str
    form_data: dict[str, str]
    files: dict[str, bytes]
    ip_addr: str | None
    identity: str | None
