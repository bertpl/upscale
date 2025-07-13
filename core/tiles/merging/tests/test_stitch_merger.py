import numpy as np
import pytest
from PIL import Image

from core.tiles import TileDimSpec
from core.tiles.merging import TileMerger
from core.tiles.splitting.splitter import TileSplitter


@pytest.mark.parametrize(
    "max_hor_tile_size, max_vert_tile_size",
    [
        (200, 200),  # 2x2 tiles
        (200, 100),  # 2x3 tiles
    ],
)
def test_paste_merger(max_hor_tile_size: int, max_vert_tile_size: int):
    """
    Test both split & merge using the TileSplitter & PasteMerger class.
    """

    # --- arrange -----------------------------------------
    img = Image.fromarray(
        np.random.randint(0, 255, size=(256, 256, 3), dtype=np.uint8),
        mode="RGB",
    )
    tiles = TileSplitter(
        tile_width_spec=TileDimSpec(min_value=2, max_value=max_hor_tile_size, multiplier=2),
        tile_height_spec=TileDimSpec(min_value=2, max_value=max_vert_tile_size, multiplier=2),
        overlap_fraction=0.1,
    ).split_image(img)

    stitch_merger = TileMerger.stitch()

    # --- act ---------------------------------------------
    img_merged = stitch_merger.merge(tiles)

    # --- assert ------------------------------------------
    assert img.size == img_merged.size
    assert img.mode == img_merged.mode
    np.testing.assert_array_equal(np.array(img), np.array(img_merged))
