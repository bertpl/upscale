import pytest

from core.tiles.splitting._helpers import IntervalSplitSolution, split_in_overlapping_intervals
from core.tiles.tile_dim_spec import TileDimSpec


@pytest.mark.parametrize(
    "specs, interval_overlap_fraction, expected_solution",
    [
        (
            TileDimSpec(min_value=32, max_value=256, multiplier=4),
            0.0,
            IntervalSplitSolution(size=100, starts=[0]),
        ),
        (
            TileDimSpec(min_value=24, max_value=240, multiplier=6),
            0.0,
            IntervalSplitSolution(size=54, starts=[0, 46]),
        ),
        (
            TileDimSpec(min_value=32, max_value=88, multiplier=4),
            0.0,
            IntervalSplitSolution(size=52, starts=[0, 48]),
        ),
        (
            TileDimSpec(min_value=32, max_value=90, multiplier=2),
            0.0,
            IntervalSplitSolution(size=50, starts=[0, 50]),
        ),
        (
            TileDimSpec(min_value=32, max_value=48, multiplier=2),
            0.0,
            IntervalSplitSolution(size=34, starts=[0, 33, 66]),
        ),
        (
            TileDimSpec(min_value=30, max_value=240, multiplier=6),
            0.2,
            IntervalSplitSolution(size=60, starts=[0, 40]),
        ),
        (
            TileDimSpec(min_value=16, max_value=52, multiplier=4),
            0.2,
            IntervalSplitSolution(size=40, starts=[0, 30, 60]),
        ),
    ],
)
def test_split_in_overlapping_intervals(
    specs: TileDimSpec,
    interval_overlap_fraction: float,
    expected_solution: IntervalSplitSolution,
):
    # --- arrange -----------------------------------------
    size = 100

    # --- act ---------------------------------------------
    sol = split_in_overlapping_intervals(size, specs, interval_overlap_fraction)

    # --- assert ------------------------------------------
    assert sol == expected_solution
