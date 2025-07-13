from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
from PIL import Image

from core.tiles.tile import Tile

from ._tile_merge_solution import TileMergeSolution


class TileMerger(ABC):
    """
    Class that merges tiles back into a single image.
    """

    @abstractmethod
    def merge(self, tiles: list[Tile]) -> TileMergeSolution:
        raise NotImplementedError()

    @staticmethod
    def _init_solution(tiles: list[Tile]) -> TileMergeSolution:
        """
        Initializes empty image / array and returns as TileMergeSolution.
        """
        img = Image.new(
            mode="RGB",
            size=(
                max(tile.right for tile in tiles) + 1,
                max(tile.bottom for tile in tiles) + 1,
            ),
        )
        pixel_sources = np.zeros((img.height, img.width), dtype=np.uint16)
        tile_ranges = [tile.range for tile in tiles]

        return TileMergeSolution(
            img=img,
            tile_ranges=tile_ranges,
            pixel_sources=pixel_sources,
        )

    # -------------------------------------------------------------------------
    #  Factory methods
    # -------------------------------------------------------------------------
    @classmethod
    def paste(cls) -> TileMerger:
        from .paste_merger import PasteMerger

        return PasteMerger()

    @classmethod
    def stitch(cls) -> TileMerger:
        from .stitch_merger import StitchMerger

        return StitchMerger()
