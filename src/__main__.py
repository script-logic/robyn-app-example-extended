# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT


class InitError(Exception): ...


try:
    from robyn_example.logger import log, setup_logging

    setup_logging()
    from robyn_example.robyn import run_robyn_app

    run_robyn_app()

except InitError:
    import sys

    log.exception("Unexpected app initialization error")
    sys.exit(1)
