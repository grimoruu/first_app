from decimal import Decimal

from sqlalchemy.engine import Row

from core.config.settings import settings


def number_length_check(number: Decimal) -> bool:
    count_of_digits = len(str(number).split(".")[1])
    return True if count_of_digits > settings.max_count.max_count else False


def get_count(items: list[Row]) -> int:
    s = 0
    total_count = 0
    for i in range(len(items)):
        if items[i].list_id != s:
            total_count += items[i].total
            s = items[i].list_id
    return total_count
