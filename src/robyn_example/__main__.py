# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT


class InitError(Exception): ...


try:
    from .logger import setup_logging

    setup_logging()

    from .robyn import run_robyn_app

    run_robyn_app()

except InitError:
    import sys

    from .logger import log

    log.exception("Unexpected error")
    sys.exit(1)
