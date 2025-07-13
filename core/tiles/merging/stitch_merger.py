import cv2
import numpy as np
from cv2.detail import DpSeamFinder, GraphCutSeamFinder
from PIL import Image

from core.tiles.tile import Tile

from ._tile_merge_solution import TileMergeSolution
from ._tile_merger_base import TileMerger


class StitchMerger(TileMerger):
    """
    Class that merges tiles back into a single image using seam-optimized stitching using opencv.
    """

    def merge(self, tiles: list[Tile]) -> TileMergeSolution:
        """
        Merges the given tiles into a single image using stitching with seam optimization.
        """

        # --- init ----------------------------------------
        cv_images = [cv2.cvtColor(np.array(tile.img), cv2.COLOR_RGB2BGR) for tile in tiles]  # openCV assumes BGR format
        corners = [(tile.left, tile.top) for tile in tiles]
        masks = [np.full((tile.height, tile.width), 255, dtype=np.uint8) for tile in tiles]

        # --- seam optimization ---------------------------
        seam_finder = DpSeamFinder(costFunc="COLOR_GRAD")
        updated_masks = seam_finder.find(cv_images, corners, masks)

        # --- merge using optimized masks -----------------

        # init
        sol = self._init_solution(tiles)

        # paste all tiles into the image
        for i, (tile, mask) in enumerate(zip(tiles, updated_masks)):
            # paste image with mask
            np_mask = np.array(mask.get())
            sol.img.paste(
                tile.img,
                box=(tile.left, tile.top),
                mask=Image.fromarray(np_mask),
            )

            # set pixel sources
            for row in range(tile.top, tile.bottom + 1):
                for col in range(tile.left, tile.right + 1):
                    if np_mask[row - tile.top, col - tile.left] > 0:
                        sol.pixel_sources[row, col] = i

        # return final solution
        return sol
