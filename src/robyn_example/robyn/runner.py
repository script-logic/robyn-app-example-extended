# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT


import json
from contextvars import ContextVar
from time import perf_counter_ns
from uuid import uuid4

from that_depends import Provide, inject

from robyn import ALLOW_CORS, Request, Response, Robyn
from robyn_example.config import AppConfig
from robyn_example.database import DatabaseManager
from robyn_example.di import Ioc
from robyn_example.logger import log

from .endpoints import router as health_router
from .endpoints.api_v1 import router as api_v1_router
from .endpoints.helpers.parsers import try_format_json


@inject
def run_robyn_app(
    app: Robyn = Provide[Ioc.robyn_app],
    cfg: AppConfig = Provide[Ioc.cfg],
    db: DatabaseManager = Provide[Ioc.db],
    request_id_ctx: ContextVar[str] = Provide[Ioc.request_id_ctx],
) -> None:

    async def startup() -> None:
        await Ioc.init_resources()
        await db.init_db()
        await log.ainfo("App startup")

    async def shutdown() -> None:
        await db.dispose()
        await Ioc.tear_down()
        await log.ainfo("App shutdown")

    app.startup_handler(startup)
    app.shutdown_handler(shutdown)

    app.add_request_header("Content-Type", "application/json")
    app.add_response_header("Content-Type", "application/json")

    app.include_router(api_v1_router)
    app.include_router(health_router)

    @app.before_request()
    async def before_middleware(request: Request) -> Request:
        request.headers.set("start_time", f"{perf_counter_ns()}")
        request_id = str(uuid4())
        request_id_ctx.set(request_id)
        request.headers.set("request_id", f"{request_id}")

        await log.ainfo("request_id=%s", request_id)
        await log.adebug(
            "request=%s",
            json.dumps(
                {
                    "query_params": request.query_params.to_dict(),
                    "headers": json.loads(str(request.headers)),
                    "path_params": request.path_params,
                    "body": request.body,
                    "method": request.method,
                    "url": str(request.url.path),
                    "form_data": request.form_data,
                    "files": request.files,
                    "ip_addr": request.ip_addr,
                    "identity": str(request.identity)
                    if request.identity
                    else None,
                },
                default=str,
                indent=2,
            ),
        )
        return request

    @app.after_request()
    async def after_middleware(
        request: Request, response: Response
    ) -> Response:
        request_path = request.url.path
        request_id = request.headers.get("request_id")
        start_time = request.headers.get("start_time")

        if isinstance(start_time, str | int):
            response_duration_ns = perf_counter_ns() - int(start_time)
        else:
            response_duration_ns = None
            await log.awarning("not isinstance(start_time, str | int)")

        await log.ainfo(
            "request_id=%s, request_path=%s, response_duration_ns=%s",
            request_id,
            request_path,
            response_duration_ns,
        )
        await log.adebug(
            "response.description=%s", try_format_json(response.description)
        )
        return response

    ALLOW_CORS(app, cfg.cors.allow_origins, cfg.cors.allow_headers)

    app.start(
        host=cfg.app.host,
        port=cfg.app.port,
        client_timeout=cfg.app.client_timeout_sec,
        keep_alive_timeout=cfg.app.keep_alive_timeout_sec,
    )
