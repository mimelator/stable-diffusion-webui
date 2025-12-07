#!/bin/bash
# Update ComfyUI requirements on network storage
# Fixes frontend version warnings

COMFYUI_PATH="/workspace/runpod-slim/ComfyUI"
VENV_PATH="$COMFYUI_PATH/.venv"

echo "=== ComfyUI Requirements Update ==="
echo ""

# Check if ComfyUI exists
if [ ! -d "$COMFYUI_PATH" ]; then
    echo "✗ ComfyUI not found at $COMFYUI_PATH"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "⚠ Virtual environment not found, creating..."
    cd "$COMFYUI_PATH"
    python3 -m venv .venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment and update
echo "Updating ComfyUI requirements..."
cd "$COMFYUI_PATH"

# Activate venv and install requirements
source .venv/bin/activate

echo "Installing/updating requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✓ Requirements updated successfully"
echo ""
echo "To use the updated environment, activate it:"
echo "  source $VENV_PATH/bin/activate"
echo ""
echo "Or update your startup script to use the venv Python"
