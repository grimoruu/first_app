from sqlalchemy.engine import Row


def to_nested_dict(row: Row) -> dict:
    # something()
    return {
        "id": 1,
        "name": "asd",
        "user": {
            "id": 1,
            "username": "asdsa",
            "email": "fsdfsdf",
        },
    }  # nested


def to_nested_list(rows: list[Row]) -> list[dict]:
    return [to_nested_dict(row) for row in rows]


{
    "id": 1,
    "name": "asd",
    "user__id": 1,
    "user__email": "fsdfsdf",
    "user__username": "fsdfsdf",
    "user__birth_day": "fsdfsdf"
}

# flatten
