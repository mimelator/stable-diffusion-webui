#!/bin/bash
# Quick fix for CUDA check issue

COMFYUI_PATH="/workspace/runpod-slim/ComfyUI"

echo "=== Diagnosing CUDA Check Issue ==="
echo ""

# Check system Python
echo "1. Checking system Python CUDA:"
python3 -c "import torch; print('  CUDA available:', torch.cuda.is_available())" 2>&1 || echo "  ✗ torch not available in system Python"

echo ""

# Check venv Python if it exists
if [ -f "$COMFYUI_PATH/.venv/bin/python" ]; then
    echo "2. Checking venv Python CUDA:"
    $COMFYUI_PATH/.venv/bin/python -c "import torch; print('  CUDA available:', torch.cuda.is_available())" 2>&1 || echo "  ✗ torch not available in venv Python"
    
    echo ""
    echo "3. If venv doesn't have torch, installing it..."
    cd "$COMFYUI_PATH"
    source .venv/bin/activate
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 2>&1 | tail -5
    echo ""
    echo "4. Verifying after install:"
    $COMFYUI_PATH/.venv/bin/python -c "import torch; print('  CUDA available:', torch.cuda.is_available())" 2>&1
else
    echo "2. No venv found - using system Python is fine"
fi

echo ""
echo "=== Done ==="
echo "Now try running the startup script again:"
echo "  /workspace/start_comfyui_auto.sh"
