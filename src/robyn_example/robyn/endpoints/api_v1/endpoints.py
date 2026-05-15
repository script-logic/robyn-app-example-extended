# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from robyn import Robyn
from robyn.types import PathParams
from robyn_example.database import CrimesTable, DatabaseManager
from robyn_example.database.crime_repository import (
    create_crime_repo,
    delete_crime_repo,
    get_crime_repo,
    get_crimes_repo,
    update_crime_repo,
)
from robyn_example.di import Ioc
from robyn_example.domain import CrimeEntity
from robyn_example.robyn.endpoints.helpers import (
    crime_exist_policy,
    parse_query_params,
)

from .enums import CrimePathEnum
from .schemas import (
    CrimeId,
    CrimeResponse,
    DeleteCrimeResponse,
    GetCrimesModel,
    GetCrimesQueryParams,
)

prefix = "/api/v1"
app: Robyn = Ioc.robyn_app.resolve_sync()


@app.post(f"{prefix}/crime/add")
async def add_crime(
    crime: CrimeEntity,
) -> CrimeResponse:
    db_crime = CrimesTable(**crime.model_dump())
    db: DatabaseManager = await Ioc.db.resolve()

    async with db.session as session:
        new_crime = await create_crime_repo(db_crime, session)

    return CrimeResponse.model_validate(new_crime)


@app.get(f"{prefix}/crimes/get")
async def get_crimes(
    query_params: GetCrimesQueryParams,
) -> list[CrimeResponse]:
    validated = parse_query_params(query_params, GetCrimesModel)
    db: DatabaseManager = await Ioc.db.resolve()

    async with db.session as session:
        crimes = await get_crimes_repo(
            validated.skip, validated.limit, session
        )
    return [CrimeResponse.model_validate(c) for c in crimes]


@app.get(
    f"{prefix}/crime/:{CrimePathEnum.crime_id}",
    auth_required=True,
)
async def get_crime(path_params: PathParams) -> CrimeResponse:
    validated = CrimeId.model_validate(path_params)
    db: DatabaseManager = await Ioc.db.resolve()

    async with db.session as session:
        crime = crime_exist_policy(
            await get_crime_repo(validated.crime_id, session)
        )
    return CrimeResponse.model_validate(crime)


@app.put(f"{prefix}/crime/update/:{CrimePathEnum.crime_id}")
async def update_crime(
    path_params: PathParams,
    new_crime_data: CrimeEntity,
) -> CrimeResponse:
    validated = CrimeId.model_validate(path_params)
    db: DatabaseManager = await Ioc.db.resolve()

    async with db.session as session:
        db_crime = crime_exist_policy(
            await get_crime_repo(validated.crime_id, session)
        )
        for key, value in new_crime_data.model_dump().items():
            setattr(db_crime, key, value)
        updated_crime = await update_crime_repo(db_crime, session)
    return CrimeResponse.model_validate(updated_crime)


@app.delete(f"{prefix}/crime/:{CrimePathEnum.crime_id}")
async def delete_crime(
    path_params: PathParams,
) -> DeleteCrimeResponse:
    validated = CrimeId.model_validate(path_params, from_attributes=True)
    db: DatabaseManager = await Ioc.db.resolve()

    async with db.session as session:
        db_crime = crime_exist_policy(
            await get_crime_repo(validated.crime_id, session)
        )
        _deleted_crime = await delete_crime_repo(db_crime, session)
    return DeleteCrimeResponse()
