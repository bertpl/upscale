"""
Tile upscaling class based on Stable Diffusion 2 supporting 4x upscaling.
Essentially, this is a wrapper class around the following Hugging Face pipeline:
    https://huggingface.co/stabilityai/stable-diffusion-x4-upscaler
"""

from functools import cached_property

import torch
from diffusers import StableDiffusionUpscalePipeline
from PIL import Image

from core.tiles import TileDimSpec
from utils import tqdm_override

from ._base import TileUpscaler


class TileUpscaler_SD2_4x(TileUpscaler):
    """
    Tile upscaler based on Stable Diffusion 2, supporting 4x upscaling.
    """

    # -------------------------------------------------------------------------
    #  Constructor & Main API
    # -------------------------------------------------------------------------
    def __init__(self):
        super().__init__(
            name="sd2_4x",
            scale_factor=4,
            tile_width_spec=TileDimSpec(16, 256, 4),
            tile_height_spec=TileDimSpec(16, 256, 4),
        )

    def _upscale(self, image: Image.Image, prompt: str = "") -> Image.Image:
        return self._sd_pipeline(prompt=prompt, image=image).images[0]

    # -------------------------------------------------------------------------
    #  Internal methods
    # -------------------------------------------------------------------------
    @cached_property
    def _sd_pipeline(self) -> StableDiffusionUpscalePipeline:
        """Construct & return the Stable Diffusion Upscale Pipeline, configured for the right GPU/CPU."""

        # instantiate the pipeline
        model_id = "stabilityai/stable-diffusion-x4-upscaler"
        pipeline = StableDiffusionUpscalePipeline.from_pretrained(model_id)

        # configure for the right device
        if torch.cuda.is_available():
            pipeline = pipeline.to("cuda")
        elif torch.mps.is_available():
            pipeline = pipeline.to("mps")
        else:
            pipeline = pipeline.to("cpu")

        # other
        pipeline.set_progress_bar_config(disable=True)

        # return
        return pipeline
