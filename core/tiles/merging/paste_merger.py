from core.tiles.tile import Tile

from ._tile_merge_solution import TileMergeSolution
from ._tile_merger_base import TileMerger


class PasteMerger(TileMerger):
    """
    Class that merges tiles back into a single image using simple pasting.
    """

    def merge(self, tiles: list[Tile]) -> TileMergeSolution:
        """
        Merges the given tiles into a single image using pasting.
        """

        # init
        sol = self._init_solution(tiles)

        # paste all tiles into the image
        for i, tile in enumerate(tiles):
            # paste image
            sol.img.paste(tile.img, box=(tile.left, tile.top))

            # set pixel sources
            sol.pixel_sources[tile.top : tile.bottom + 1, tile.left : tile.right + 1] = i

        # return final solution
        return sol
