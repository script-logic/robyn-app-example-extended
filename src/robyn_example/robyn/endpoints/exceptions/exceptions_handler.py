# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from collections.abc import Callable, Coroutine
from contextvars import ContextVar
from functools import wraps

from pydantic import BaseModel, ValidationError

from robyn.exceptions import HTTPException
from robyn_example.di import Ioc
from robyn_example.logger import log

from .schemas import (
    ExceptionResponse,
    HTTPExceptionResponse,
    ValidationErrorResponse,
)


class AppError(Exception): ...


def exceptions_handler(e: Exception) -> BaseModel:
    if isinstance(e, ValidationError):
        errors = form_errors(e)
        return ValidationErrorResponse(description=errors)

    if isinstance(e, HTTPException):
        return HTTPExceptionResponse(
            status_code=e.status_code,
            description=str(e.detail),
        )
    request_id_ctx: ContextVar[str] = Ioc.request_id_ctx.resolve_sync()
    request_id = request_id_ctx.get(None)
    return ExceptionResponse(
        description="Internal server error",
        request_id=f"Your request id is {request_id}",
    )


def form_errors(e: ValidationError) -> list[dict[str, str | None]]:
    return [
        {
            "field": ".".join(str(loc) for loc in err["loc"]),
            "message": err["msg"],
            "input": err.get("input"),
        }
        for err in e.errors()
    ]


def alternative_exceptions_handler_endpoints_decorator[**P, S](
    func: Callable[..., Coroutine[None, None, S]],
) -> Callable[..., Coroutine[None, None, S | BaseModel]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> S | BaseModel:
        try:
            return await func(*args, **kwargs)
        except ValidationError as e:
            errors = form_errors(e)
            return ValidationErrorResponse(description=errors)

        except HTTPException as e:
            return HTTPExceptionResponse(
                status_code=e.status_code,
                description=str(e.detail),
            )
        except AppError:
            request_id_ctx: ContextVar[str] = Ioc.request_id_ctx.resolve_sync()
            request_id = request_id_ctx.get("request_id")
            log.exception("Unexpected error for request_id=%s", request_id)
            return ExceptionResponse(
                description="Internal server error",
                request_id=f"Your request id is {request_id}",
            )

    return wrapper
