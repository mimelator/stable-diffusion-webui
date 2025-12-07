#!/bin/bash
# Verify ComfyUI setup on RunPod network volume

COMFYUI_ROOT="/workspace/runpod-slim/ComfyUI"

echo "=== ComfyUI Setup Verification ==="
echo ""

# Check ComfyUI directory exists
if [ ! -d "$COMFYUI_ROOT" ]; then
    echo "✗ ERROR: ComfyUI not found at $COMFYUI_ROOT"
    exit 1
fi

echo "✓ ComfyUI found at: $COMFYUI_ROOT"
echo ""

# Check for main.py
if [ -f "$COMFYUI_ROOT/main.py" ]; then
    echo "✓ main.py found"
else
    echo "✗ WARNING: main.py not found"
fi

echo ""
echo "=== Model Files Check ==="
echo ""

# Check UNet
UNET_FILE="$COMFYUI_ROOT/models/unet/z_image_turbo_bf16.safetensors"
if [ -f "$UNET_FILE" ]; then
    SIZE=$(du -h "$UNET_FILE" | cut -f1)
    echo "✓ UNet: $UNET_FILE ($SIZE)"
else
    echo "✗ UNet: NOT FOUND at $UNET_FILE"
fi

# Check CLIP
CLIP_FILE="$COMFYUI_ROOT/models/clip/qwen_3_4b.safetensors"
if [ -f "$CLIP_FILE" ]; then
    SIZE=$(du -h "$CLIP_FILE" | cut -f1)
    echo "✓ CLIP: $CLIP_FILE ($SIZE)"
else
    echo "✗ CLIP: NOT FOUND at $CLIP_FILE"
fi

# Check VAE
VAE_FILE="$COMFYUI_ROOT/models/vae/ae.safetensors"
if [ -f "$VAE_FILE" ]; then
    SIZE=$(du -h "$VAE_FILE" | cut -f1)
    echo "✓ VAE: $VAE_FILE ($SIZE)"
else
    echo "✗ VAE: NOT FOUND at $VAE_FILE"
fi

echo ""
echo "=== Directory Structure ==="
echo "Models directory:"
ls -lh "$COMFYUI_ROOT/models/" 2>/dev/null | head -10

echo ""
echo "UNet directory:"
ls -lh "$COMFYUI_ROOT/models/unet/" 2>/dev/null

echo ""
echo "CLIP directory:"
ls -lh "$COMFYUI_ROOT/models/clip/" 2>/dev/null

echo ""
echo "VAE directory:"
ls -lh "$COMFYUI_ROOT/models/vae/" 2>/dev/null

echo ""
echo "=== File Permissions ==="
if [ -f "$UNET_FILE" ]; then
    PERMS=$(stat -c "%a" "$UNET_FILE" 2>/dev/null || stat -f "%OLp" "$UNET_FILE" 2>/dev/null)
    echo "UNet permissions: $PERMS"
fi

echo ""
echo "=== CUDA Check ==="
python3 -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('CUDA device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')" 2>/dev/null || echo "✗ Could not check CUDA (Python/torch may not be available)"

echo ""
echo "=== Network Volume Status ==="
df -h /workspace

echo ""
echo "=== Ready to Start ComfyUI ==="
echo "Command:"
echo "  cd $COMFYUI_ROOT"
echo "  python3 main.py --listen 0.0.0.0 --port 8188"
