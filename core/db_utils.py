from collections.abc import Mapping
from typing import Any

from sqlalchemy.engine import Row


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


def to_nested_list(rows: list[Row]) -> list[dict]:
    return [_to_nested_dict(_) for _ in rows]
