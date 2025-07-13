from __future__ import annotations

from abc import ABC, abstractmethod

from PIL import Image

from core.tile_upscalers import TileUpscaler


class ImageUpscaler(ABC):
    """
    Abstract Base class that can upscale images of any size and with any given factor
    using the specified TileUpscaler model.
    """

    # -------------------------------------------------------------------------
    #  Constructor & Main API
    # -------------------------------------------------------------------------
    def __init__(self, tile_upscaler: TileUpscaler, debug: bool = False):
        self._tile_upscaler = tile_upscaler
        self.debug = debug

    @abstractmethod
    def upscale(self, image: Image.Image, scale: float, prompt: str = "") -> Image.Image:
        """
        Upscales the given image by the requested scale factor and using the provided prompt as guidance.

        :param image: The image to upscale as bytes.
        :param scale: float > 0.0, scaling factor to apply to the image.
                      If scale <= 1.0, no actual upscaling is performed, potentially just an image resize.
        :param prompt: Optional prompt to guide the upscaling process.
        :return: The upscaled image as bytes.
        """
        raise NotImplementedError()

    # -------------------------------------------------------------------------
    #  Factory Methods
    # -------------------------------------------------------------------------
    @classmethod
    def single_tile(cls, tile_upscaler: TileUpscaler) -> ImageUpscaler:
        from .single_tile import ImageUpscaler_SingleTile

        return ImageUpscaler_SingleTile(tile_upscaler)

    @classmethod
    def multi_tile(cls, tile_upscaler: TileUpscaler, stitch_overlap_fraction: float, debug: bool) -> ImageUpscaler:
        from .multi_tile import ImageUpscaler_MultiTile

        return ImageUpscaler_MultiTile(tile_upscaler, stitch_overlap_fraction, debug=debug)
