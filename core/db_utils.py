from collections import defaultdict
from functools import reduce
from operator import getitem
from typing import Any

from ndicts.ndicts import NestedDict
from sqlalchemy.engine import Row


# def _nest_dict_rec(key: str, value: Any, result: dict[str, Any]):
#     key, *rest = key.split('__')
#     if rest:
#         _nest_dict_rec(rest[0], value, result.setdefault(key, {}))
#     else:
#         result[key] = value
#
#
# def _to_nested_dict(row: Row) -> dict[Any]:
#     row = {**row}
#     result = {}
#     for key, value in row.items():
#         _nest_dict_rec(key, value, result)
#     return result
#
#
# def to_nested_list(rows: list[Row]) -> list[dict]:
#     return [_to_nested_dict(row) for row in rows] #oldold

##############################################################
#
# def _get_from_dict(data_dict, map_list):
#     """Iterate nested dictionary"""
#     result = reduce(getitem, map_list, data_dict)
#     return result
#
#
# # instantiate nested defaultdict of defaultdicts
# tree = lambda: defaultdict(tree)
# d = tree()
#
#
# def _to_nested_dict(row: Row):
#     row = {**row}
#     for key, value in row.items():
#         *keys, final_key = key.split('__')
#         print(*keys, final_key)
#         _get_from_dict(d, keys)[final_key] = value
#
#
# def to_nested_list(rows: list[Row]) -> list[dict]:
#     return [_to_nested_dict(row) for row in rows]

##############################################################

def _to_nested_dict(row: Row) -> dict:
    row = {**row}
    nd = NestedDict()
    for key, value in row.items():
        n_key = tuple(key.split('__'))
        nd[n_key] = value
    return nd.to_dict()


def to_nested_list(rows: list[Row]) -> list[dict]:
    return [_to_nested_dict(row) for row in rows]
