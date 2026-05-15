# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from pydantic import BaseModel

from robyn import status_codes


class ValidationErrorResponse(BaseModel):
    status_code: int = status_codes.HTTP_422_UNPROCESSABLE_ENTITY
    description: list[dict[str, str | None]]


class HTTPExceptionResponse(BaseModel):
    status_code: int
    description: str


class ExceptionResponse(BaseModel):
    status_code: int = status_codes.HTTP_500_INTERNAL_SERVER_ERROR
    description: str = "Internal server error"
    request_id: str
