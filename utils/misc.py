import numpy as np


def spaced_ints(int_min: int, int_max: int, n: int) -> list[int]:
    return [int(x) for x in np.linspace(int_min, int_max, n, dtype=int)]


def round_up(value: int, multiple: int) -> int:
    """
    Round up the given value to the nearest multiple of the specified value.
    If value is already a multiple, it is returned unchanged.
    """
    if value % multiple == 0:
        return value
    return value + (multiple - (value % multiple))


def round_down(value: int, multiple: int) -> int:
    """
    Round down the given value to the nearest multiple of the specified value.
    If value is already a multiple, it is returned unchanged.
    """
    if value % multiple == 0:
        return value
    return value - (value % multiple)
