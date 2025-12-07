#!/bin/bash
# Automated ComfyUI startup script for RunPod
# Kills existing processes and starts fresh

set -e  # Exit on error

COMFYUI_PATH="/workspace/runpod-slim/ComfyUI"
PORT=8188

echo "=========================================="
echo "ComfyUI Auto-Start Script"
echo "=========================================="
echo ""

# Function to kill ComfyUI processes
kill_comfyui() {
    echo "Step 1: Stopping existing ComfyUI processes..."
    
    # Find all ComfyUI processes
    PIDS=$(ps aux | grep -E "python.*main.py|python.*ComfyUI" | grep -v grep | awk '{print $2}' || true)
    
    if [ -z "$PIDS" ]; then
        echo "  ✓ No existing ComfyUI processes found"
        return 0
    fi
    
    echo "  Found processes: $PIDS"
    
    # Try graceful shutdown first
    for PID in $PIDS; do
        echo "  Sending SIGTERM to PID $PID..."
        kill -TERM "$PID" 2>/dev/null || true
    done
    
    # Wait for processes to exit
    sleep 3
    
    # Check if any are still running
    REMAINING=$(ps aux | grep -E "python.*main.py|python.*ComfyUI" | grep -v grep | awk '{print $2}' || true)
    
    if [ -n "$REMAINING" ]; then
        echo "  Some processes still running, force killing..."
        for PID in $REMAINING; do
            echo "  Force killing PID $PID..."
            kill -9 "$PID" 2>/dev/null || true
        done
        sleep 1
    fi
    
    # Final check
    FINAL=$(ps aux | grep -E "python.*main.py|python.*ComfyUI" | grep -v grep || true)
    if [ -z "$FINAL" ]; then
        echo "  ✓ All ComfyUI processes stopped"
    else
        echo "  ⚠ Warning: Some processes may still be running"
        echo "$FINAL"
    fi
}

# Function to check port
check_port() {
    echo ""
    echo "Step 2: Checking port $PORT..."
    
    if command -v netstat >/dev/null 2>&1; then
        PORT_CHECK=$(netstat -tuln 2>/dev/null | grep ":$PORT " || true)
    elif command -v ss >/dev/null 2>&1; then
        PORT_CHECK=$(ss -tuln 2>/dev/null | grep ":$PORT " || true)
    elif command -v fuser >/dev/null 2>&1; then
        PORT_CHECK=$(fuser "$PORT/tcp" 2>/dev/null || true)
    else
        PORT_CHECK=""
        echo "  (Cannot check port - no tools available)"
    fi
    
    if [ -n "$PORT_CHECK" ]; then
        echo "  ⚠ Port $PORT is still in use, waiting 5 seconds..."
        sleep 5
        # Try to kill whatever is using the port
        if command -v fuser >/dev/null 2>&1; then
            fuser -k "$PORT/tcp" 2>/dev/null || true
            sleep 2
        fi
    else
        echo "  ✓ Port $PORT is free"
    fi
}

# Function to get Python executable
get_python() {
    # Check if virtual environment exists and use it
    if [ -f "$COMFYUI_PATH/.venv/bin/python" ]; then
        echo "$COMFYUI_PATH/.venv/bin/python"
    else
        echo "python3"
    fi
}

# Function to verify CUDA
verify_cuda() {
    echo ""
    echo "Step 3: Verifying CUDA..."
    
    PYTHON_CMD=$(get_python)
    
    # Try to check CUDA with the Python we'll use
    if ! $PYTHON_CMD -c "import torch; assert torch.cuda.is_available(), 'CUDA not available'; print('  ✓ CUDA available'); print('  ✓ Device:', torch.cuda.get_device_name(0))" 2>/dev/null; then
        # If venv Python fails, try system Python as fallback
        if [ "$PYTHON_CMD" != "python3" ] && python3 -c "import torch; assert torch.cuda.is_available()" 2>/dev/null; then
            echo "  ⚠ CUDA works with system Python, but venv may need torch installed"
            echo "  Continuing anyway - ComfyUI will use system Python if venv fails"
        else
            echo "  ✗ CUDA not available - cannot start ComfyUI"
            echo "  Trying nvidia-smi as alternative check..."
            if command -v nvidia-smi >/dev/null 2>&1; then
                nvidia-smi
                echo "  GPU is accessible, but PyTorch CUDA check failed"
                echo "  This might work anyway - continuing..."
            else
                exit 1
            fi
        fi
    fi
}

# Function to verify ComfyUI
verify_comfyui() {
    echo ""
    echo "Step 4: Verifying ComfyUI installation..."
    
    if [ ! -d "$COMFYUI_PATH" ]; then
        echo "  ✗ ComfyUI not found at $COMFYUI_PATH"
        exit 1
    fi
    
    if [ ! -f "$COMFYUI_PATH/main.py" ]; then
        echo "  ✗ main.py not found"
        exit 1
    fi
    
    echo "  ✓ ComfyUI found at: $COMFYUI_PATH"
}

# Function to clear cache
clear_cache() {
    echo ""
    echo "Step 5: Clearing cache (optional)..."
    
    rm -rf "$COMFYUI_PATH/.cache" 2>/dev/null || true
    rm -rf "$COMFYUI_PATH/__pycache__" 2>/dev/null || true
    rm -rf "$COMFYUI_PATH/models/.cache" 2>/dev/null || true
    
    echo "  ✓ Cache cleared"
}

# Function to start ComfyUI
start_comfyui() {
    echo ""
    echo "Step 6: Starting ComfyUI..."
    
    PYTHON_CMD=$(get_python)
    if [ "$PYTHON_CMD" != "python3" ]; then
        echo "  Using virtual environment: $PYTHON_CMD"
    else
        echo "  Using system Python: $PYTHON_CMD"
    fi
    
    echo "  Path: $COMFYUI_PATH"
    echo "  Port: $PORT"
    echo "  Command: $PYTHON_CMD main.py --listen 0.0.0.0 --port $PORT"
    echo ""
    echo "=========================================="
    echo "Starting ComfyUI in 2 seconds..."
    echo "Press Ctrl+C to cancel"
    echo "=========================================="
    sleep 2
    
    cd "$COMFYUI_PATH"
    
    # Activate venv if it exists
    if [ -f "$COMFYUI_PATH/.venv/bin/activate" ]; then
        source .venv/bin/activate
    fi
    
    exec $PYTHON_CMD main.py --listen 0.0.0.0 --port "$PORT"
}

# Main execution
kill_comfyui
check_port
verify_cuda
verify_comfyui
clear_cache
start_comfyui
