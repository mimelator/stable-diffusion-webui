# How to Upload Scripts to RunPod Network Storage

## Method 1: Copy-Paste Directly (Easiest - Recommended)

### Step 1: Access Your Pod Terminal
- Go to RunPod Dashboard → Your Pod → Connect → **Web Terminal** or **JupyterLab**

### Step 2: Create the Scripts Using cat

**For `start_comfyui_auto.sh`:**

```bash
cat > /workspace/start_comfyui_auto.sh << 'SCRIPT_END'
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

# Function to verify CUDA
verify_cuda() {
    echo ""
    echo "Step 3: Verifying CUDA..."
    
    if ! python3 -c "import torch; assert torch.cuda.is_available(), 'CUDA not available'; print('  ✓ CUDA available'); print('  ✓ Device:', torch.cuda.get_device_name(0))" 2>/dev/null; then
        echo "  ✗ CUDA not available - cannot start ComfyUI"
        exit 1
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
    echo "  Path: $COMFYUI_PATH"
    echo "  Port: $PORT"
    echo "  Command: python3 main.py --listen 0.0.0.0 --port $PORT"
    echo ""
    echo "=========================================="
    echo "Starting ComfyUI in 2 seconds..."
    echo "Press Ctrl+C to cancel"
    echo "=========================================="
    sleep 2
    
    cd "$COMFYUI_PATH"
    exec python3 main.py --listen 0.0.0.0 --port "$PORT"
}

# Main execution
kill_comfyui
check_port
verify_cuda
verify_comfyui
clear_cache
start_comfyui
SCRIPT_END

chmod +x /workspace/start_comfyui_auto.sh
echo "✓ Created start_comfyui_auto.sh"
```

**For `start_comfyui_background.sh`:**

```bash
cat > /workspace/start_comfyui_background.sh << 'SCRIPT_END'
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

# Verify CUDA
if ! python3 -c "import torch; assert torch.cuda.is_available()" 2>/dev/null; then
    echo "✗ CUDA not available"
    exit 1
fi

# Verify ComfyUI
if [ ! -f "$COMFYUI_PATH/main.py" ]; then
    echo "✗ ComfyUI not found"
    exit 1
fi

# Clear cache
rm -rf "$COMFYUI_PATH/.cache" "$COMFYUI_PATH/__pycache__" 2>/dev/null || true

# Start in background
echo "Starting ComfyUI in background..."
echo "Log file: $LOG_FILE"
echo ""

cd "$COMFYUI_PATH"
nohup python3 main.py --listen 0.0.0.0 --port "$PORT" > "$LOG_FILE" 2>&1 &

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
SCRIPT_END

chmod +x /workspace/start_comfyui_background.sh
echo "✓ Created start_comfyui_background.sh"
```

**Verify they were created:**
```bash
ls -lh /workspace/*.sh
```

---

## Method 2: Using JupyterLab File Upload (Visual)

### Step 1: Access JupyterLab
- RunPod Dashboard → Your Pod → Connect → **JupyterLab**

### Step 2: Upload Files
1. In JupyterLab, navigate to `/workspace/` in the file browser
2. Click **Upload** button (folder with up arrow icon)
3. Select the script files from your local machine:
   - `start_comfyui_auto.sh`
   - `start_comfyui_background.sh`
4. Wait for upload to complete

### Step 3: Make Executable
Open a terminal in JupyterLab and run:
```bash
chmod +x /workspace/start_comfyui_auto.sh
chmod +x /workspace/start_comfyui_background.sh
```

---

## Method 3: Using SCP from Local Machine

If you have SSH access to your Pod:

```bash
# From your local machine
scp start_comfyui_auto.sh root@YOUR_POD_IP:/workspace/
scp start_comfyui_background.sh root@YOUR_POD_IP:/workspace/

# Then SSH in and make executable
ssh root@YOUR_POD_IP
chmod +x /workspace/*.sh
```

---

## Method 4: Using wget/curl (If Hosted Online)

If you host the files somewhere (GitHub Gist, pastebin, etc.):

```bash
# Example with wget
wget -O /workspace/start_comfyui_auto.sh https://your-url-here
wget -O /workspace/start_comfyui_background.sh https://your-url-here

chmod +x /workspace/*.sh
```

---

## Quick Test After Upload

```bash
# Verify files exist and are executable
ls -lh /workspace/*.sh

# Test the script (it will start ComfyUI)
/workspace/start_comfyui_auto.sh
```

---

## Recommended: Method 1 (Copy-Paste)

**Why Method 1 is best:**
- ✅ No file transfer needed
- ✅ Works immediately
- ✅ Files saved directly to network storage
- ✅ No external dependencies
- ✅ Works in any terminal (Web Terminal, JupyterLab, SSH)

**Just copy-paste the cat commands above into your RunPod terminal!**
