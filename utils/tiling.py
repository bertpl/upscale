import math

from .misc import round_down, spaced_ints


def split_in_overlapping_intervals(
    size: int, max_interval_size: int, interval_size_multiplier: int, interval_overlap_fraction: float
) -> tuple[int, list[int]]:
    """
    Splits the interval [0, size-1] into n sub-intervals, that cover the whole interval, with the following conditions:
      - each sub-interval has the same size
      - sub-interval sizes should lie withing [multiplier, max_interval_size] and should be a multiple of 'multiplier'
      - subsequent sub-intervals overlap by a given minimum fraction of the size of the sub-interval
      - the solution with the least number of sub-intervals is returned, with the smallest sub-interval size being
          selected within this group of solutions

    Result is returned as (sub_interval_size, [start1, start2, ..., startN]), so each sub-interval is defined by
    as [start_i, start_i + sub_interval_size - 1].
    """

    # --- prep --------------------------------------------

    # largest interval size that is a multiple of the interval size multiplier, that fits into the interval size
    max_interval_size = round_down(min(max_interval_size, size), interval_size_multiplier)

    # min / max # of intervals
    n_intervals_min = math.ceil(size / max_interval_size)
    n_intervals_max = math.ceil(size / (max_interval_size * (1 - interval_overlap_fraction))) + 2

    # --- main loop ---------------------------------------
    for n in range(n_intervals_min, n_intervals_max + 1):
        for sub_interval_size in range(
            interval_size_multiplier,
            max_interval_size + 1,
            interval_size_multiplier,
        ):
            # calculate the start points of the sub-intervals
            sub_interval_start_points = spaced_ints(0, size - sub_interval_size, n)

            # check if the sub-intervals cover the whole interval
            if _has_sufficient_overlap(size, sub_interval_size, interval_overlap_fraction, sub_interval_start_points):
                return sub_interval_size, sub_interval_start_points

    # --- no solution found -------------------------------
    raise ValueError(
        f"Cannot split interval of size {size} into intervals with "
        + f"max size {max_interval_size} and {interval_overlap_fraction} overlap"
    )


def _has_sufficient_overlap(
    size: int,
    sub_interval_size: int,
    interval_overlap_fraction: float,
    sub_interval_start_points: list[int],
) -> bool:
    """
    Checks if the sub-interval size & start points is sufficient
    to cover the whole interval with the given overlap fraction.
    """

    # check if the sub-interval size is large enough
    if sub_interval_start_points[-1] + sub_interval_size < size:
        # last interval does not cover the end of the interval
        return False

    # absolute minimum overlap size
    min_overlap = math.ceil(sub_interval_size * interval_overlap_fraction)

    # check if sub-intervals cover the whole interval
    for i_start_prev, i_start_next in zip(sub_interval_start_points[:-1], sub_interval_start_points[1:]):
        overlap = (i_start_prev + sub_interval_size) - i_start_next
        if overlap < min_overlap:
            return False

    # no issue found, so we're good
    return True
