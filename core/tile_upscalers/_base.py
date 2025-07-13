from __future__ import annotations

from abc import ABC, abstractmethod

from PIL import Image

from core.tiles import Tile, TileDimSpec


# =================================================================================================
#  Base class for tile upscalers
# =================================================================================================
class TileUpscaler(ABC):
    """
    Base class for tile upscalers.
    """

    # supported model names, i.e. allowable values for the `--model` option in the CLI,
    # as well as the allowable values for the factor method below.
    SUPPORTED_MODELS = ["sd2_4x"]

    def __init__(self, name: str, scale_factor: int, tile_width_spec: TileDimSpec, tile_height_spec: TileDimSpec):
        self.name = name
        self.scale_factor = scale_factor
        self.tile_width_spec = tile_width_spec
        self.tile_height_spec = tile_height_spec

    def is_tile_size_supported(self, tile_width: int, tile_height: int) -> bool:
        return self.tile_width_spec.is_valid(tile_width) and self.tile_height_spec.is_valid(tile_height)

    def get_nearest_supported_tile_size(
        self,
        tile_width: int,
        tile_height: int,
        larger_if_possible: bool,
    ) -> tuple[int, int]:
        """
        Get the nearest supported tile size for the given tile size.
        This will always return a tile size that is not larger than the maximum supported tile size of the model
        and with sizes that are multiples of the tile size multiplier.

        Depending on 'larger_if_possible' we round up or down to satisfy multiplier constraints, whenever there is a choice.

        If the provided tile size is already valid, it is returned unchanged.
        """
        if larger_if_possible:
            return (
                self.tile_width_spec.round_up(tile_width),
                self.tile_height_spec.round_up(tile_height),
            )
        else:
            return (
                self.tile_width_spec.round_down(tile_width),
                self.tile_height_spec.round_down(tile_height),
            )

    def upscale(self, tile: Tile, prompt: str = "") -> Tile:
        """
        Upscale the given image by the scale factor, using the provided prompt as guidance.
        """

        # --- sanity checks -------------------------------
        if not self.is_tile_size_supported(tile.width, tile.height):
            raise ValueError(
                f"Tile size ({tile.width} x {tile.height}) is not supported for TileUpscaler '{self.name}'.)"
            )

        # --- upscale image -------------------------------
        upscaled_img = self._upscale(tile.img, prompt)

        # --- return new Tile object ----------------------
        return Tile(
            img=upscaled_img,
            left=self.scale_factor * tile.left,
            top=self.scale_factor * tile.top,
        )

    @abstractmethod
    def _upscale(self, image: Image.Image, prompt: str = "") -> Image.Image:
        """
        Upscale the given image by the scale factor, using the provided prompt as guidance.
        """
        raise NotImplementedError()

    @classmethod
    def from_name(cls, name: str) -> TileUpscaler:
        """
        Factory method to create a TileUpscaler instance from its name.
        """
        match name:
            case "sd2_4x":
                from .sd2_4x import TileUpscaler_SD2_4x

                return TileUpscaler_SD2_4x()
            case _:
                raise ValueError(
                    f"Unsupported tile upscaler model: {name}. Supported models are: {cls.SUPPORTED_MODELS}"
                )
