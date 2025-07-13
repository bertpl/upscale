"""
Various implementations of full-image upscaling algorithms, which use TileUpscaler implementations
to upscale images of any size by potentially calling a TileUpscaler multiple times.
"""

from ._base import ImageUpscaler
from .multi_tile import ImageUpscaler_MultiTile
from .single_tile import ImageUpscaler_SingleTile
