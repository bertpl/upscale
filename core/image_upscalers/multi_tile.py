import math
import os
from datetime import datetime
from pathlib import Path

from PIL import Image
from tqdm import tqdm

from core.tile_upscalers import TileUpscaler
from core.tiles import TileMerger, TileSplitter

from ._base import ImageUpscaler


# =================================================================================================
#  ImageUpscaler implementation
# =================================================================================================
class ImageUpscaler_MultiTile(ImageUpscaler):
    """
    Class that upscales images of any sizes by splitting it up in tiles and calling the TileUpscaler on each tile.
    This process is repeated until the image is large enough, i.e. the target size is reached.
    """

    def __init__(self, tile_upscaler: TileUpscaler, stitch_overlap_fraction: float = 0.0, debug: bool = False):
        """
        :param tile_upscaler:
        :param stitch_overlap_fraction: float >= 0.0, fraction of overlap between tiles to stitch.
                                If set to 0.0, no overlap is enforced and no stitching is performed,
                                  even if the tile size multiplier forces tiles to slightly overlap.
        """
        self._stitch_overlap_fraction = stitch_overlap_fraction
        super().__init__(tile_upscaler, debug)

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

        # --- main loop -----------------------------------
        i = 0
        atomic_factor = self._tile_upscaler.scale_factor
        while (image.width != w_target) or (image.height != h_target):
            remaining_factor = max(w_target / image.width, h_target / image.height)
            if remaining_factor <= 1.0:
                # we don't have the exact target size yet, but the image is already large enough
                # so we down-sample and then we should be done
                print(f"Downsampling image [{image.width:>5}x{image.height:>5}] -> [{w_target:>5}x{h_target:>5}]")
                image = image.resize(size=(w_target, h_target), resample=Image.LANCZOS)
            elif i == 0:
                # as a first operation, if we still need to upscale, we do a full upscale even if the result would be
                # far too large, because we don't want to lose information in the first iteration.
                image = self._upscale_image(image, prompt)
            elif remaining_factor > 0.9 * atomic_factor:
                # also in the case where the remaining factor is close to 1 full remaining upscale,
                # we will do this without downsampling first.
                image = self._upscale_image(image, prompt)
            else:
                # this is not the first operation and the result of a full upscale will be significantly too large,
                # so we downsample first, so we avoid excessive computations / # of tiles.
                w_target_tmp = math.ceil(w_target / atomic_factor)
                h_target_tmp = math.ceil(h_target / atomic_factor)
                print(
                    f"Downsampling image [{image.width:>5}x{image.height:>5}] -> [{w_target_tmp:>5}x{h_target_tmp:>5}]"
                )
                image = image.resize(size=(w_target_tmp, h_target_tmp), resample=Image.LANCZOS)
            i += 1

        # --- and we're done ------------------------------
        return image

    # -------------------------------------------------------------------------
    #  Internal methods
    # -------------------------------------------------------------------------
    def _upscale_image(self, image: Image.Image, prompt: str = "") -> Image.Image:
        """
        Upscale the given image 1 time using the tile upscaler, possibly splitting in multiple tiles & stitching.
        """

        # --- prep ----------------------------------------
        atomic_scale = int(self._tile_upscaler.scale_factor)

        # --- split in tiles --------------------------
        tile_splitter = TileSplitter(
            tile_width_spec=self._tile_upscaler.tile_width_spec,
            tile_height_spec=self._tile_upscaler.tile_height_spec,
            overlap_fraction=self._stitch_overlap_fraction,
        )
        tiles = tile_splitter.split_image(image)

        # --- upscale each tile ----------------------
        upscaled_tiles = [
            self._tile_upscaler.upscale(tile, prompt)
            for tile in tqdm(
                tiles,
                desc=f"Upscaling image    [{image.width:>5}x{image.height:>5}] -> "
                + f"[{image.width * atomic_scale:>5}x{image.height * atomic_scale:>5}] "
                + f"using {len(tiles):>3} tile(s)",
                unit="tile",
            )
        ]

        # --- merge tiles ---------------------------
        if len(tiles) == 1:
            # no merging required
            image = upscaled_tiles[0].img
        else:
            if self._stitch_overlap_fraction == 0:
                tile_merger = TileMerger.paste()  # just paste, we don't have overlap for seam optimization
            else:
                tile_merger = TileMerger.stitch()  # we have some overlap, so we can optimize seams

            solution = tile_merger.merge(upscaled_tiles)
            image = solution.img

            if self.debug:
                slug = f"{datetime.now().strftime("%H%M%S")}_{image.width}x{image.height}_{len(tiles)}tiles"
                solution.pixel_sources_img().save(Path(os.getcwd()) / f"debug_{slug}_pixel_sources.png")
                solution.img_overlayed().save(Path(os.getcwd()) / f"debug_{slug}_stitches.png")

        # --- and we're done ------------------------------
        return image
