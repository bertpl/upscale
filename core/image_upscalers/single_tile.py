from PIL import Image

from core.tiles import Tile

from ._base import ImageUpscaler


class ImageUpscaler_SingleTile(ImageUpscaler):
    """
    Class that upscales images by just calling a TileUpscaler once for the entire image.
    """

    def upscale(self, image: Image.Image, scale: float, prompt: str = "") -> Image.Image:
        """
        Upscales the given image by the requested scale factor and using the provided prompt as guidance.

        :param image: The image to upscale as bytes.
        :param scale: float > 0.0, scaling factor to apply to the image.
                      If scale <= 1.0, no actual upscaling is performed, potentially just an image resize.
        :param prompt: Optional prompt to guide the upscaling process.
        :return: The upscaled image as bytes.
        """

        # --- init ----------------------------------------
        w_target = int(image.width * scale)  # target width
        h_target = int(image.height * scale)  # target height

        # --- ensure image size is a valid tile size ------
        if not self._tile_upscaler.is_tile_size_supported(image.width, image.height):
            w_new, h_new = self._tile_upscaler.get_nearest_supported_tile_size(
                tile_width=image.width,
                tile_height=image.height,
                larger_if_possible=True,  # preferrably larger, such that the image can be upscaled by the tile upscaler
            )
            image = image.resize(size=(w_new, h_new), resample=Image.LANCZOS)

        # --- upscale -------------------------------------
        while (image.width < w_target) and (image.height < h_target):
            image = self._upscale_image_once(image, prompt)

        # --- downsample if necessary -------------------
        if (image.width > w_target) or (image.height > h_target):
            image = image.resize(size=(w_target, h_target), resample=Image.LANCZOS)

        # --- and we're done ----------------------------
        return image

    # -------------------------------------------------------------------------
    #  Internal methods
    # -------------------------------------------------------------------------
    def _upscale_image_once(self, image: Image.Image, prompt: str = "") -> Image.Image:
        """
        Upscale the given image once using the tile upscaler and exactly by the scale factor of the tile upscaler.
        """

        return self._tile_upscaler.upscale(Tile(image, 0, 0), prompt=prompt).img
