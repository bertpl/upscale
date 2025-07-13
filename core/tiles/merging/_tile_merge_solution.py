import math
from dataclasses import dataclass

import numpy as np
from PIL import Image

from core.tiles.tile_range import TileRange


@dataclass
class TileMergeSolution:
    """
    Class that represents a solution for merging tiles, as returned by the TileMerger.merge(...) method.
    """

    # -------------------------------------------------------------------------
    #  Primary fields
    # -------------------------------------------------------------------------
    img: Image.Image  # merged image
    tile_ranges: list[TileRange]  # list of tile ranges of source tiles
    pixel_sources: np.ndarray  # (n_rows, n_cols) uint16 array with pixel source indices

    # -------------------------------------------------------------------------
    #  Properties & helpers
    # -------------------------------------------------------------------------
    def n_tiles(self) -> int:
        return len(self.tile_ranges)

    def pixel_sources_img(self) -> Image.Image:
        """
        Returns a PIL Image representation of the pixel sources.
        """
        c1 = math.floor(255 / self.n_tiles())
        c0 = c1 // 2
        return Image.fromarray((c1 * self.pixel_sources + c0).astype(np.uint8), mode="L")

    def img_overlayed(
        self,
        tile_range_clr: tuple[int, int, int] | None = (0, 255, 0),
        seam_clr: tuple[int, int, int] | None = (255, 255, 255),
    ) -> Image.Image:
        """
        Returns an image with tile ranges and/or seams overlayed.
        """

        # --- initialize ----------------------------------
        img = self.img.copy()

        # --- draw tile ranges ----------------------------
        if tile_range_clr is not None:
            for i in range(img.height):
                for j in range(img.width):
                    if (i + j) % 2 == 0:
                        # check if this pixel is on any tile range border
                        draw = False
                        for tr in self.tile_ranges:
                            if (i == tr.top) or (i == tr.bottom) or (j == tr.left) or (j == tr.right):
                                draw = True

                        # draw pixel
                        if draw:
                            img.putpixel((j, i), tile_range_clr)

        # --- draw seams ----------------------------------
        if seam_clr is not None:
            for i in range(img.height):
                for j in range(img.width):
                    # check if we're on a seam
                    if i < img.height - 1:
                        if self.pixel_sources[i, j] != self.pixel_sources[i + 1, j]:
                            img.putpixel((j, i), seam_clr)

                    if j < img.width - 1:
                        if self.pixel_sources[i, j] != self.pixel_sources[i, j + 1]:
                            img.putpixel((j, i), seam_clr)

        # --- and we're done ------------------------------
        return img
