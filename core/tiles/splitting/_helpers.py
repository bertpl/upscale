import math
from dataclasses import dataclass

from core.tiles.tile_dim_spec import TileDimSpec
from utils.misc import spaced_ints


@dataclass(frozen=True)
class IntervalSplitSolution:
    size: int
    starts: list[int]


def split_in_overlapping_intervals(
    size: int, specs: TileDimSpec, interval_overlap_fraction: float
) -> IntervalSplitSolution:
    """
    Splits the interval [0, size-1] into n sub-intervals, that cover the whole interval, with the following conditions:
      - each sub-interval has the same size
      - sub-interval sizes should adhere to the provided 'specs'
      - subsequent sub-intervals overlap by a given minimum fraction of the size of the sub-interval
      - the solution with the least number of sub-intervals is returned, with the smallest sub-interval size being
          selected within this group of solutions

    Result is returned as (sub_interval_size, [start1, start2, ..., startN]), so each sub-interval is defined by
    as [start_i, start_i + sub_interval_size - 1].
    """

    # --- prep --------------------------------------------

    # largest interval size <= size that satisfies the specs
    max_interval_size = specs.round_down(size)

    # min / max # of intervals
    n_intervals_min = math.ceil(size / max_interval_size)
    n_intervals_max = math.ceil(size / (max_interval_size * (1 - interval_overlap_fraction))) + 2

    # --- main loop ---------------------------------------
    for n in range(n_intervals_min, n_intervals_max + 1):
        for sub_interval_size in specs.valid_values():
            # calculate the start points of the sub-intervals
            proposed_solution = IntervalSplitSolution(
                size=sub_interval_size,
                starts=spaced_ints(0, size - sub_interval_size, n),
            )

            # check if the solution is valid
            if is_solution_valid(proposed_solution, specs, interval_overlap_fraction, size):
                return proposed_solution

    # --- no solution found -------------------------------
    raise ValueError(
        f"Cannot split interval of size {size} into intervals with "
        + f"{interval_overlap_fraction} overlap fraction and provided specs {specs}."
    )


def is_solution_valid(
    solution: IntervalSplitSolution,
    specs: TileDimSpec,
    interval_overlap_fraction: float,
    size: int,
) -> bool:
    """
    Checks if the provided solution, covers the entire interval and has the requested overlap.
    """

    # check if interval size is valid
    if not specs.is_valid(solution.size):
        return False

    # check if all intervals jointly cover the whole interval
    if len({i for start in solution.starts for i in range(start, start + solution.size)}) < size:
        return False

    # absolute minimum overlap size
    min_overlap = math.ceil(solution.size * interval_overlap_fraction)

    # check if sub-intervals cover the whole interval
    for i_start_prev, i_start_next in zip(solution.starts[:-1], solution.starts[1:]):
        overlap = (i_start_prev + solution.size) - i_start_next
        if overlap < min_overlap:
            return False

    # no issue found, so we're good
    return True
