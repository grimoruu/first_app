from collections.abc import Callable
from time import time
from typing import Any

from ndicts.ndicts import NestedDict


def speed_test_dec(try_count: int = 1_000):
    def _decorator(func: Callable[[Any], None]):
        def _wrapper(*args, **kwargs):
            start = time()
            for _ in range(try_count):
                func(*args, **kwargs)
            end = time()

        return _wrapper

    return _decorator


def _nest_dict_rec(key: str, value: Any, result: dict[str, Any]):
    key, *rest = key.split('__')
    if rest:
        _nest_dict_rec(rest[0], value, result.setdefault(key, {}))
    else:
        result[key] = value


@speed_test_dec(1_000)
def to_nested_dict1(row: dict) -> dict[str, Any]:
    result = {}
    for key, value in row.items():
        _nest_dict_rec(key, value, result)
    return result


@speed_test_dec(1_000)
def to_nested_dict2(a: str, row: dict) -> dict:
    # print(a)
    nd = NestedDict()
    for key, value in row.items():
        n_key = tuple(key.split('__'))
        nd[n_key] = value
    return nd.to_dict()


if __name__ == '__main__':
    to_nested_dict1({"a": 1, "b__a": 1, "b__c": 1, "c__d": 1})
    to_nested_dict2("asd", {"a": 1, "b__a": 1, "b__c": 1, "c__d": 1})
