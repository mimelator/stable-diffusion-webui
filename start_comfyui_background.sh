#!/bin/bash
# Automated ComfyUI startup script for RunPod (runs in background)
# Kills existing processes and starts fresh in background

set -e

COMFYUI_PATH="/workspace/runpod-slim/ComfyUI"
PORT=8188
LOG_FILE="/workspace/comfyui.log"

echo "=========================================="
echo "ComfyUI Auto-Start Script (Background)"
echo "=========================================="
echo ""

# Kill existing processes
echo "Stopping existing ComfyUI processes..."
PIDS=$(ps aux | grep -E "python.*main.py|python.*ComfyUI" | grep -v grep | awk '{print $2}' || true)

if [ -n "$PIDS" ]; then
    for PID in $PIDS; do
        kill -TERM "$PID" 2>/dev/null || true
    done
    sleep 3
    REMAINING=$(ps aux | grep -E "python.*main.py|python.*ComfyUI" | grep -v grep | awk '{print $2}' || true)
    if [ -n "$REMAINING" ]; then
        for PID in $REMAINING; do
            kill -9 "$PID" 2>/dev/null || true
        done
        sleep 1
    fi
fi

# Check port
if command -v fuser >/dev/null 2>&1; then
    fuser -k "$PORT/tcp" 2>/dev/null || true
    sleep 2
fi

# Determine Python executable
if [ -f "$COMFYUI_PATH/.venv/bin/python" ]; then
    PYTHON_CMD="$COMFYUI_PATH/.venv/bin/python"
else
    PYTHON_CMD="python3"
fi

# Verify CUDA (try venv Python first, fallback to system)
if ! $PYTHON_CMD -c "import torch; assert torch.cuda.is_available()" 2>/dev/null; then
    # Fallback to system Python
    if [ "$PYTHON_CMD" != "python3" ] && python3 -c "import torch; assert torch.cuda.is_available()" 2>/dev/null; then
        echo "⚠ CUDA works with system Python, using that instead"
        PYTHON_CMD="python3"
    else
        echo "✗ CUDA not available"
        # Check nvidia-smi as last resort
        if command -v nvidia-smi >/dev/null 2>&1; then
            nvidia-smi
            echo "GPU accessible, continuing anyway..."
        else
            exit 1
        fi
    fi
fi

# Verify ComfyUI
if [ ! -f "$COMFYUI_PATH/main.py" ]; then
    echo "✗ ComfyUI not found"
    exit 1
fi

# Clear cache
rm -rf "$COMFYUI_PATH/.cache" "$COMFYUI_PATH/__pycache__" 2>/dev/null || true

# Determine Python executable (set above during CUDA check)
if [ "$PYTHON_CMD" != "python3" ]; then
    echo "Using virtual environment Python"
else
    echo "Using system Python"
fi

# Start in background
echo "Starting ComfyUI in background..."
echo "Log file: $LOG_FILE"
echo ""

cd "$COMFYUI_PATH"

# Activate venv if it exists
if [ -f "$COMFYUI_PATH/.venv/bin/activate" ]; then
    source .venv/bin/activate
fi

nohup $PYTHON_CMD main.py --listen 0.0.0.0 --port "$PORT" > "$LOG_FILE" 2>&1 &

# Get PID
COMFYUI_PID=$!
echo "✓ ComfyUI started (PID: $COMFYUI_PID)"
echo ""
echo "To view logs:"
echo "  tail -f $LOG_FILE"
echo ""
echo "To stop ComfyUI:"
echo "  kill $COMFYUI_PID"
echo ""
echo "To check if running:"
echo "  ps aux | grep $COMFYUI_PID"
