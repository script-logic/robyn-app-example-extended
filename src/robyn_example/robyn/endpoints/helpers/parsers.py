# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from pydantic import BaseModel
from robyn.robyn import QueryParams


def parse_query_params[T: BaseModel](params: QueryParams, model: type[T]) -> T:
    result = {}
    for field_name in model.model_fields:
        if v := params.get(field_name, default=None):
            result[field_name] = v
    return model.model_validate(result)
