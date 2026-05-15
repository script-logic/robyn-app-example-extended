# Copyright (c) 2026 script-logic <dev.scriptlogic@gmail.com>
# SPDX-License-Identifier: MIT

from enum import StrEnum

from robyn import status_codes
from robyn.exceptions import HTTPException
from robyn_example.database import CrimesTable


class PoliciesStrings(StrEnum):
    crime_not_found = "Crime not found"


def crime_exist_policy(crime: CrimesTable | None) -> CrimesTable:
    if crime is None:
        raise HTTPException(
            status_codes.HTTP_204_NO_CONTENT,
            detail=PoliciesStrings.crime_not_found,
        )
    return crime
