from PIL import Image

from core.tiles.tile import Tile
from core.tiles.tile_dim_spec import TileDimSpec

from ._helpers import IntervalSplitSolution, split_in_overlapping_intervals


class TileSplitter:
    """
    Class that allows to split an image into tiles with specified dimension specs and overlap.
    """

    # -------------------------------------------------------------------------
    #  Constructor
    # -------------------------------------------------------------------------
    def __init__(self, tile_width_spec: TileDimSpec, tile_height_spec: TileDimSpec, overlap_fraction: float = 0.0):
        self._tile_width_spec = tile_width_spec
        self._tile_height_spec = tile_height_spec
        self._overlap_fraction = overlap_fraction

    # -------------------------------------------------------------------------
    #  Main API
    # -------------------------------------------------------------------------
    def split_image(self, img: Image.Image) -> list[Tile]:
        """
        Split image in tiles such that they cover the entire image and satisfy specifications provided
        to the constructor.
        """

        # --- hor/vert splits -----------------------------
        # Determine hor. & vert. tile sizes / positions
        sol_hor: IntervalSplitSolution = split_in_overlapping_intervals(
            size=img.width,
            specs=self._tile_width_spec,
            interval_overlap_fraction=self._overlap_fraction,
        )
        sol_vert: IntervalSplitSolution = split_in_overlapping_intervals(
            size=img.height,
            specs=self._tile_height_spec,
            interval_overlap_fraction=self._overlap_fraction,
        )

        # --- generate tiles ------------------------------
        return [
            Tile(
                img=img.crop(
                    box=(
                        left,
                        top,
                        left + sol_hor.size,
                        top + sol_vert.size,
                    )
                ),
                left=left,
                top=top,
            )
            for left in sol_hor.starts
            for top in sol_vert.starts
        ]
