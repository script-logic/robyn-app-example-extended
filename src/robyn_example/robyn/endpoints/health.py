# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from robyn import SubRouter

from robyn_example.robyn import auth_handler

from .exceptions import (
    exceptions_handler,
)

router = SubRouter(__file__, prefix="/health")
router.exception(exceptions_handler)
router.configure_authentication(auth_handler)


@router.get("", const=True)
def health_check() -> dict[str, str]:
    return {"status": "healthy", "version": "1.0.0"}
