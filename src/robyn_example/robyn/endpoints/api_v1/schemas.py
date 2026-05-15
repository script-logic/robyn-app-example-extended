# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from robyn import status_codes
from robyn.robyn import QueryParams
from robyn_example.domain import CrimeEntity


class GetCrimesParams(BaseModel):
    skip: int
    limit: int


class CrimeResponse(CrimeEntity):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class DeleteCrimeResponse(BaseModel):
    status_code: int = status_codes.HTTP_204_NO_CONTENT
    description: str = "Crime deleted successfully"


class GetCrimesModel(BaseModel):
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=1, le=1000)


class CrimeId(BaseModel):
    crime_id: int = Field(default=..., ge=1)


class GetCrimesQueryParams(QueryParams):
    skip: int
    limit: int
