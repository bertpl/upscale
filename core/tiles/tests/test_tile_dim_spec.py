import pytest

from core.tiles.tile_dim_spec import TileDimSpec


def test_tile_dim_spec_valid_values():
    # --- arrange -----------------------------------------
    tile_dim_spec = TileDimSpec(min_value=64, max_value=256, multiplier=4)

    # --- act ---------------------------------------------
    valid_values = tile_dim_spec.valid_values()

    # --- assert ------------------------------------------
    assert valid_values == list(range(64, 257, 4))


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, False),
        (4, False),
        (64, True),
        (65, False),
        (128, True),
        (255, False),
        (256, True),
        (260, False),
    ],
)
def test_tile_dim_spec_is_valid(value: int, expected: bool):
    # --- arrange -----------------------------------------
    tile_dim_spec = TileDimSpec(min_value=64, max_value=256, multiplier=4)

    # --- act ---------------------------------------------
    is_valid = tile_dim_spec.is_valid(value)

    # --- assert ------------------------------------------
    assert is_valid == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, 64),
        (4, 64),
        (64, 64),
        (65, 68),
        (128, 128),
        (255, 256),
        (256, 256),
        (260, 256),
    ],
)
def test_tile_dim_spec_round_up(value: int, expected: bool):
    # --- arrange -----------------------------------------
    tile_dim_spec = TileDimSpec(min_value=64, max_value=256, multiplier=4)

    # --- act ---------------------------------------------
    rounded = tile_dim_spec.round_up(value)

    # --- assert ------------------------------------------
    assert rounded == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, 64),
        (4, 64),
        (64, 64),
        (65, 64),
        (128, 128),
        (255, 252),
        (256, 256),
        (260, 256),
    ],
)
def test_tile_dim_spec_round_down(value: int, expected: bool):
    # --- arrange -----------------------------------------
    tile_dim_spec = TileDimSpec(min_value=64, max_value=256, multiplier=4)

    # --- act ---------------------------------------------
    rounded = tile_dim_spec.round_down(value)

    # --- assert ------------------------------------------
    assert rounded == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, 64),
        (4, 64),
        (64, 68),
        (65, 68),
        (128, 132),
        (255, 256),
        (256, 256),
        (260, 256),
    ],
)
def test_tile_dim_spec_next(value: int, expected: bool):
    # --- arrange -----------------------------------------
    tile_dim_spec = TileDimSpec(min_value=64, max_value=256, multiplier=4)

    # --- act ---------------------------------------------
    rounded = tile_dim_spec.next(value)

    # --- assert ------------------------------------------
    assert rounded == expected


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, 64),
        (4, 64),
        (64, 64),
        (65, 64),
        (128, 124),
        (255, 252),
        (256, 252),
        (260, 256),
    ],
)
def test_tile_dim_spec_prev(value: int, expected: bool):
    # --- arrange -----------------------------------------
    tile_dim_spec = TileDimSpec(min_value=64, max_value=256, multiplier=4)

    # --- act ---------------------------------------------
    rounded = tile_dim_spec.prev(value)

    # --- assert ------------------------------------------
    assert rounded == expected
