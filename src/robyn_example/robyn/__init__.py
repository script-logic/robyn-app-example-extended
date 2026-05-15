# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

"""Import all endpoint modules here to activate them at app initialization."""

from .auth import auth_handler as auth_handler
from .endpoints import health as health
from .endpoints.api_v1 import endpoints as endpoints
from .runner import run_robyn_app as run_robyn_app
