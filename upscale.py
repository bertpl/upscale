import os
from pathlib import Path

import click
from PIL import Image

from core import ImageUpscaler, TileUpscaler


# =================================================================================================
#  Upscaling command
# =================================================================================================
@click.command()
@click.option("--input-file", "-i", type=click.Path(exists=True), required=True, help="Input file path")
@click.option(
    "--output-file",
    "-o",
    type=click.Path(),
    required=False,
    help="Output file path; when omitted <filename>_upscaled.png.",
)
@click.option("--scale", "-s", type=float, default=4.0, help="Scaling factor (default: 4.0)")
@click.option(
    "--stitch-overlap-fraction",
    "-sof",
    type=float,
    default=0.0,
    help="Fractional tile overlap for stitch seam optimization",
)
@click.option(
    "--model",
    "-m",
    type=click.Choice(TileUpscaler.SUPPORTED_MODELS),
    default=TileUpscaler.SUPPORTED_MODELS[0],
    help=f"Upscaling model ({TileUpscaler.SUPPORTED_MODELS})",
)
@click.option("--prompt", "-p", type=str, default="", help="Prompt to guide the upscaling process")
@click.option(
    "--debug",
    "-d",
    type=bool,
    default=False,
    is_flag=True,
    help="Enable extra debug output",
)
def upscale(
    input_file: str,
    output_file: str | None,
    scale: float,
    stitch_overlap_fraction: float,
    model: str,
    prompt: str,
    debug: bool,
):
    """Upscale an image by a given factor."""

    # --- path handling -------------------------
    if isinstance(input_file, str):
        input_file = Path(input_file)
    if not output_file:
        output_file = _construct_output_file_path(input_file)
    elif isinstance(output_file, str):
        output_file = Path(output_file)

    # --- show what we're going to do -----------
    click.echo(f"Upscaling {input_file} by a factor of {scale} to {output_file}")

    # --- actual upscaling ----------------------

    # load
    img = Image.open(input_file).convert("RGB")

    # upscale
    image_upscaler = ImageUpscaler.multi_tile(
        tile_upscaler=TileUpscaler.from_name(model),
        stitch_overlap_fraction=stitch_overlap_fraction,
        debug=debug,
    )
    img = image_upscaler.upscale(img, scale, prompt=prompt)

    # save
    img.save(output_file)


def _construct_output_file_path(input_file: Path) -> Path:
    """Construct the output file name based on the input file and scale."""
    folder, file = input_file.parent, input_file.stem
    basename, ext = os.path.splitext(file)
    return folder / f"{basename}_upscaled.png"


# =================================================================================================
#  Entrypoint
# =================================================================================================
if __name__ == "__main__":
    upscale()
