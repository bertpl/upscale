from dataclasses import dataclass


@dataclass(frozen=True)
class TileRange:
    left: int
    top: int
    width: int
    height: int

    @property
    def right(self) -> int:
        """Right-most pixel of the tile range, inclusive."""
        return self.left + self.width - 1

    @property
    def bottom(self) -> int:
        """Bottom-most pixel of the tile range, inclusive."""
        return self.top + self.height - 1
