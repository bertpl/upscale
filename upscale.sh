#!/bin/bash
# ==================================================================================
#  Upscale images using generative AI (eg Stable Diffusion); run 'upscale.sh [--help]' for help.
# ==================================================================================

# --- activate conda environment ---
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate upscale  # UPDATE TO YOUR ENVIRONMENT NAME

# --- run upscale.py with absolute path ---
SCRIPT_DIR=$(realpath "$(dirname "$0")")
python "$SCRIPT_DIR/upscale.py" "$@"