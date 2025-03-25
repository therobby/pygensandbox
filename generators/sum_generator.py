from typing import Generator


def sum_generator() -> Generator[int, int, None]:
    sum_value: int = 0
    while True:
        sum_value += yield sum_value
