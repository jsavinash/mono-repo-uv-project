from typing import Generator


def count_up_to(max_value: int) -> Generator[int, None, None]:
    """
    A generator that yields integers from 1 up to (and including) max_value.

    - YieldType: int (the type of values produced by yield)
    - SendType: None (nothing is sent back into the generator)
    - ReturnType: None (the function does not return a final value)
    """
    current = 1
    while current <= max_value:
        yield current
        current += 1


# Using the generator
counter = count_up_to(5)
for number in counter:
    print(number)
