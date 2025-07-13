import numpy as np
import pytest
from PIL import Image

from core.tiles import TileDimSpec
from core.tiles.merging import TileMerger
from core.tiles.splitting.splitter import TileSplitter


@pytest.mark.parametrize(
    "max_tile_size, overlap",
    [
        (300, 0.0),
        (250, 0.1),
        (200, 0.2),
        (150, 0.3),
    ],
)
def test_paste_merger(max_tile_size: int, overlap: float):
    """
    Test both split & merge using the TileSplitter & PasteMerger class.
    """

    # --- arrange -----------------------------------------
    img = Image.fromarray(
        np.random.randint(0, 255, size=(256, 256, 3), dtype=np.uint8),
        mode="RGB",
    )
    tiles = TileSplitter(
        tile_width_spec=TileDimSpec(min_value=2, max_value=max_tile_size, multiplier=2),
        tile_height_spec=TileDimSpec(min_value=2, max_value=max_tile_size, multiplier=2),
        overlap_fraction=overlap,
    ).split_image(img)

    paste_merger = TileMerger.paste()

    # --- act ---------------------------------------------
    img_merged = paste_merger.merge(tiles)

    # --- assert ------------------------------------------
    assert img.size == img_merged.size
    assert img.mode == img_merged.mode
    np.testing.assert_array_equal(np.array(img), np.array(img_merged))
