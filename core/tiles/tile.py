from dataclasses import dataclass

from PIL import Image

from .tile_range import TileRange


@dataclass
class Tile:
    """
    Class representing a tile of an image, together with its position and size.
    """

    img: Image.Image  # image, which also defines width and height of the tile
    left: int  # left-most pixel of the tile, inclusive
    top: int  # top-most pixel of the tile, inclusive

    @property
    def width(self) -> int:
        return self.img.width

    @property
    def height(self) -> int:
        return self.img.height

    @property
    def right(self) -> int:
        """Right-most pixel of the tile, inclusive."""
        return self.left + self.img.width - 1

    @property
    def bottom(self) -> int:
        """Bottom-most pixel of the tile, inclusive."""
        return self.top + self.img.height - 1

    @property
    def range(self) -> TileRange:
        """Returns range of this tile, i.e. position & size, without image data."""
        return TileRange(left=self.left, top=self.top, width=self.width, height=self.height)
