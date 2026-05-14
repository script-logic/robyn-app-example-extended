# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from robyn import (
    AuthenticationHandler,
    Request,
)
from robyn.authentication import BearerGetter
from robyn.robyn import Identity


class AuthHandler(AuthenticationHandler):
    def authenticate(self, request: Request) -> Identity | None:
        token = self.token_getter.get_token(request)
        if token:
            return Identity(claims={})
        return None


token_getter = BearerGetter()
auth_handler = AuthHandler(token_getter)
