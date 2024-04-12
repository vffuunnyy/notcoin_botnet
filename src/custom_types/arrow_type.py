from datetime import datetime
from typing import Annotated

import arrow

from pydantic import BeforeValidator, PlainSerializer


def validate(v: datetime | str | int | float | None) -> arrow.Arrow | None:
    if v is None:
        return None
    if isinstance(v, arrow.Arrow):
        return v
    try:
        return arrow.get(v)
    except Exception as e:
        raise ValueError(f"Could not parse datetime string: {v}") from e


def serialize(v: arrow.Arrow | None) -> datetime | None:
    if v is None:
        return None
    return v.datetime


ArrowType = Annotated[arrow.Arrow | None, BeforeValidator(validate), PlainSerializer(serialize)]
