#!/bin/bash
# Fix GPU lock issue - kill processes holding GPU

echo "=== Fixing GPU Lock Issue ==="
echo ""

# Step 1: Check nvidia-smi
echo "1. Checking GPU status with nvidia-smi..."
if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi
    echo ""
else
    echo "  ✗ nvidia-smi not available"
fi

# Step 2: Find all Python processes
echo "2. Finding all Python processes..."
ps aux | grep python | grep -v grep
echo ""

# Step 3: Kill all ComfyUI/Python processes
echo "3. Killing all ComfyUI and Python processes..."
PIDS=$(ps aux | grep -E "python|ComfyUI" | grep -v grep | awk '{print $2}' || true)

if [ -n "$PIDS" ]; then
    echo "  Found processes: $PIDS"
    for PID in $PIDS; do
        echo "  Killing PID $PID..."
        kill -TERM "$PID" 2>/dev/null || true
    done
    sleep 3
    
    # Force kill remaining
    REMAINING=$(ps aux | grep -E "python|ComfyUI" | grep -v grep | awk '{print $2}' || true)
    if [ -n "$REMAINING" ]; then
        echo "  Force killing remaining processes..."
        for PID in $REMAINING; do
            kill -9 "$PID" 2>/dev/null || true
        done
        sleep 2
    fi
    echo "  ✓ Processes killed"
else
    echo "  ✓ No processes to kill"
fi

# Step 4: Check GPU again
echo ""
echo "4. Checking GPU after cleanup..."
if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi
    echo ""
fi

# Step 5: Wait a moment for GPU to be released
echo "5. Waiting 5 seconds for GPU to be released..."
sleep 5

# Step 6: Test CUDA again
echo ""
echo "6. Testing CUDA availability..."
python3 -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')" 2>&1

echo ""
echo "=== Done ==="
echo "If CUDA is still False, try:"
echo "  1. Restart the Pod"
echo "  2. Check RunPod dashboard - ensure GPU is attached"
echo "  3. Wait 10-15 seconds after Pod starts before running scripts"
