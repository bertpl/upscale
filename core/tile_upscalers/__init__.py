"""
Functionality for upscaling single tiles up to a given size.  This abstraction allows us to support
different upscaling methods in the future, each with different inherent scaling factors and supported max tile sizes.
"""

from ._base import TileUpscaler
