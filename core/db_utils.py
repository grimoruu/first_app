from collections.abc import Mapping
from typing import Any

from sqlalchemy import func
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select


def _nest_dict_rec(key: str, value: str, result: dict[str, Any]) -> None:
    key, *rest = key.split("__")
    if rest:
        _nest_dict_rec(rest[0], value, result.setdefault(key, {}))
    else:
        result[key] = value


def _to_nested_dict(row: Mapping[Row, Any]) -> dict:
    rows: dict = {**row}
    result: dict = {}
    for key in rows:
        value = rows[key]
        _nest_dict_rec(key, value, result)
    return result


def to_nested_list(rows: list) -> list[dict]:
    return [_to_nested_dict(row) for row in rows]


def get_paginated(query: Select, limit: int | None, offset: int | None, *, db: Session) -> list[Row]:
    paginate_query = query.limit(limit).offset(offset)
    return db.execute(paginate_query).fetchall()


def get_count_of_queries(query: Select, *, db: Session) -> int:
    total_count = query.order_by(None).limit(None).offset(None).with_only_columns(func.count())
    return db.execute(total_count).scalar_one()
