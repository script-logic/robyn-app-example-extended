# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

import json

from pydantic import BaseModel
from robyn.robyn import QueryParams


def parse_query_params[T: BaseModel](params: QueryParams, model: type[T]) -> T:
    result = {}
    for field_name in model.model_fields:
        if v := params.get(field_name, default=None):
            result[field_name] = v
    return model.model_validate(result)


def try_format_json(
    raw: str | bytes | bytearray,
) -> str | bytes | bytearray:
    try:
        parsed = json.loads(raw)
        return json.dumps(parsed, default=str, indent=2)
    except json.JSONDecodeError, TypeError:
        return raw
