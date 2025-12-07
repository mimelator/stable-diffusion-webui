#!/bin/bash
# Clean restart of ComfyUI on RunPod

COMFYUI_PATH="/workspace/runpod-slim/ComfyUI"

echo "=== Clean ComfyUI Restart ==="
echo ""

# Step 1: Kill existing ComfyUI processes
echo "1. Stopping existing ComfyUI processes..."
PIDS=$(ps aux | grep -E "python.*main.py|python.*ComfyUI" | grep -v grep | awk '{print $2}')

if [ -n "$PIDS" ]; then
    for PID in $PIDS; do
        echo "  Killing PID $PID..."
        kill -TERM "$PID" 2>/dev/null
    done
    sleep 3
    
    # Force kill if still running
    REMAINING=$(ps aux | grep -E "python.*main.py|python.*ComfyUI" | grep -v grep | awk '{print $2}')
    if [ -n "$REMAINING" ]; then
        for PID in $REMAINING; do
            echo "  Force killing PID $PID..."
            kill -9 "$PID" 2>/dev/null
        done
        sleep 1
    fi
    echo "  ✓ Processes stopped"
else
    echo "  ✓ No processes to stop"
fi

# Step 2: Check port 8188
echo ""
echo "2. Checking port 8188..."
if command -v netstat >/dev/null 2>&1; then
    PORT_IN_USE=$(netstat -tuln 2>/dev/null | grep :8188)
    if [ -n "$PORT_IN_USE" ]; then
        echo "  ⚠ Port 8188 is in use:"
        echo "$PORT_IN_USE"
    else
        echo "  ✓ Port 8188 is free"
    fi
elif command -v ss >/dev/null 2>&1; then
    PORT_IN_USE=$(ss -tuln 2>/dev/null | grep :8188)
    if [ -n "$PORT_IN_USE" ]; then
        echo "  ⚠ Port 8188 is in use:"
        echo "$PORT_IN_USE"
    else
        echo "  ✓ Port 8188 is free"
    fi
else
    echo "  (Cannot check port - netstat/ss not available)"
fi

# Step 3: Verify CUDA
echo ""
echo "3. Verifying CUDA..."
python3 -c "import torch; print('  CUDA available:', torch.cuda.is_available()); print('  Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')" || {
    echo "  ✗ CUDA check failed"
    exit 1
}

# Step 4: Verify ComfyUI path
echo ""
echo "4. Verifying ComfyUI installation..."
if [ ! -d "$COMFYUI_PATH" ]; then
    echo "  ✗ ComfyUI not found at $COMFYUI_PATH"
    exit 1
fi

if [ ! -f "$COMFYUI_PATH/main.py" ]; then
    echo "  ✗ main.py not found"
    exit 1
fi

echo "  ✓ ComfyUI found at: $COMFYUI_PATH"

# Step 5: Clear cache (optional but recommended)
echo ""
echo "5. Clearing cache..."
rm -rf "$COMFYUI_PATH/.cache" "$COMFYUI_PATH/__pycache__" "$COMFYUI_PATH/models/.cache" 2>/dev/null
echo "  ✓ Cache cleared"

# Step 6: Start ComfyUI
echo ""
echo "6. Starting ComfyUI..."
echo "  Command: cd $COMFYUI_PATH && python3 main.py --listen 0.0.0.0 --port 8188"
echo ""
echo "  Starting in 2 seconds..."
sleep 2

cd "$COMFYUI_PATH"
exec python3 main.py --listen 0.0.0.0 --port 8188
