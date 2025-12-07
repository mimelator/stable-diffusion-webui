#!/bin/bash
# Stop all running ComfyUI instances

echo "=== Stopping ComfyUI ==="
echo ""

# Find all ComfyUI processes
echo "Finding ComfyUI processes..."
PROCESSES=$(ps aux | grep -E "python.*main.py|python.*ComfyUI" | grep -v grep)

if [ -z "$PROCESSES" ]; then
    echo "✓ No ComfyUI processes found"
    exit 0
fi

echo "Found ComfyUI processes:"
echo "$PROCESSES"
echo ""

# Get PIDs
PIDS=$(ps aux | grep -E "python.*main.py|python.*ComfyUI" | grep -v grep | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo "✓ No ComfyUI processes to kill"
    exit 0
fi

# Kill processes gracefully first (SIGTERM)
echo "Sending SIGTERM to ComfyUI processes..."
for PID in $PIDS; do
    echo "  Killing PID $PID..."
    kill -TERM "$PID" 2>/dev/null
done

# Wait a moment
sleep 3

# Check if any are still running
REMAINING=$(ps aux | grep -E "python.*main.py|python.*ComfyUI" | grep -v grep | awk '{print $2}')

if [ -n "$REMAINING" ]; then
    echo ""
    echo "Some processes still running, forcing kill..."
    for PID in $REMAINING; do
        echo "  Force killing PID $PID..."
        kill -9 "$PID" 2>/dev/null
    done
    sleep 1
fi

# Final check
FINAL_CHECK=$(ps aux | grep -E "python.*main.py|python.*ComfyUI" | grep -v grep)

if [ -z "$FINAL_CHECK" ]; then
    echo ""
    echo "✓ All ComfyUI processes stopped"
else
    echo ""
    echo "⚠ Warning: Some processes may still be running:"
    echo "$FINAL_CHECK"
fi

# Check if port 8188 is still in use
echo ""
echo "Checking port 8188..."
if command -v lsof >/dev/null 2>&1; then
    PORT_CHECK=$(lsof -i :8188 2>/dev/null)
    if [ -n "$PORT_CHECK" ]; then
        echo "⚠ Port 8188 is still in use:"
        echo "$PORT_CHECK"
    else
        echo "✓ Port 8188 is free"
    fi
elif command -v netstat >/dev/null 2>&1; then
    PORT_CHECK=$(netstat -tuln | grep :8188)
    if [ -n "$PORT_CHECK" ]; then
        echo "⚠ Port 8188 is still in use:"
        echo "$PORT_CHECK"
    else
        echo "✓ Port 8188 is free"
    fi
else
    echo "  (Cannot check port - lsof/netstat not available)"
fi

echo ""
echo "=== Done ==="
