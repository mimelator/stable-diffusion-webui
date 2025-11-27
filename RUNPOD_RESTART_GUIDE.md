# RunPod - Restarting ComfyUI Guide

## Overview

Different methods to restart ComfyUI on RunPod depending on how it's running.

---

## Method 1: RunPod Template/Service (Most Common)

If ComfyUI was started via RunPod template or as a service:

### Via RunPod Web UI

1. **Go to RunPod Dashboard**: https://www.runpod.io/console/pods
2. **Find your pod** (the one running ComfyUI)
3. **Click on the pod** to open details
4. **Click "Stop"** button (or "Pause" if available)
5. **Wait 10-15 seconds** for complete shutdown
6. **Click "Start"** or "Resume" button
7. **Wait for pod to start** (check status indicator)
8. **Access ComfyUI** via the proxy URL

### Via RunPod API

```python
import requests

# Your RunPod API key (get from RunPod dashboard)
RUNPOD_API_KEY = "your_api_key_here"
POD_ID = "your_pod_id_here"  # Find in RunPod dashboard

# Stop pod
stop_response = requests.post(
    f"https://api.runpod.io/graphql",
    headers={"Authorization": f"Bearer {RUNPOD_API_KEY}"},
    json={
        "query": """
        mutation {
            podStop(input: {podId: "%s"}) {
                id
                desiredStatus
            }
        }
        """ % POD_ID
    }
)

# Wait
import time
time.sleep(15)

# Start pod
start_response = requests.post(
    f"https://api.runpod.io/graphql",
    headers={"Authorization": f"Bearer {RUNPOD_API_KEY}"},
    json={
        "query": """
        mutation {
            podStart(input: {podId: "%s"}) {
                id
                desiredStatus
            }
        }
        """ % POD_ID
    }
)
```

---

## Method 2: Jupyter Notebook/Terminal (If Running Manually)

If ComfyUI is running in a terminal or Jupyter notebook:

### Stop ComfyUI Process

**In Terminal**:
```bash
# Find ComfyUI process
ps aux | grep -i comfy

# Kill the process (replace PID with actual process ID)
kill -9 <PID>

# Or kill all Python processes (be careful!)
pkill -f comfy
```

**In Jupyter Notebook**:
```python
import os
import signal
import subprocess

# Find ComfyUI process
result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
lines = result.stdout.split('\n')
comfy_processes = [l for l in lines if 'comfy' in l.lower() or 'python' in l.lower()]

for line in comfy_processes:
    if line.strip():
        parts = line.split()
        if len(parts) > 1:
            pid = int(parts[1])
            print(f"Killing process: {pid}")
            os.kill(pid, signal.SIGTERM)

print("ComfyUI stopped. Wait 10 seconds, then restart.")
```

### Restart ComfyUI

**In Terminal**:
```bash
cd /workspace/ComfyUI

# If using a startup script
./start.sh

# Or directly
python main.py --listen 0.0.0.0 --port 8188

# Or with specific options
python main.py --listen 0.0.0.0 --port 8188 --enable-cors-header "*"
```

**In Jupyter Notebook**:
```python
import subprocess
import time

# Stop any existing processes first
subprocess.run(['pkill', '-f', 'comfy'], capture_output=True)
time.sleep(5)

# Start ComfyUI in background
comfy_process = subprocess.Popen(
    ['python', 'main.py', '--listen', '0.0.0.0', '--port', '8188'],
    cwd='/workspace/ComfyUI',
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

print(f"ComfyUI started with PID: {comfy_process.pid}")
print("Check logs or wait a moment, then access ComfyUI")
```

---

## Method 3: Systemd Service (If Set Up)

If ComfyUI is running as a systemd service:

```bash
# Stop service
sudo systemctl stop comfyui

# Wait
sleep 10

# Start service
sudo systemctl start comfyui

# Check status
sudo systemctl status comfyui

# Or restart directly
sudo systemctl restart comfyui
```

---

## Method 4: Docker Container (If Using Docker)

If ComfyUI is running in a Docker container:

```bash
# Find container
docker ps | grep comfy

# Stop container
docker stop <container_id>

# Wait
sleep 10

# Start container
docker start <container_id>

# Or restart directly
docker restart <container_id>

# Check logs
docker logs <container_id>
```

---

## Method 5: Complete Pod Restart (Nuclear Option)

If nothing else works, restart the entire RunPod:

### Via Web UI

1. Go to RunPod dashboard
2. Find your pod
3. Click **"Stop"** or **"Terminate"**
4. Wait for pod to fully stop
5. Click **"Start"** or create new pod from template
6. Wait for pod to initialize
7. Access ComfyUI

### Via Terminal (If You Have SSH Access)

```bash
# This will restart the entire pod (use with caution)
sudo reboot

# Or if you have access to RunPod CLI
runpod stop <pod_id>
runpod start <pod_id>
```

---

## Quick Restart Script for RunPod

Create this script to easily restart ComfyUI:

```python
#!/usr/bin/env python3
"""
Quick ComfyUI Restart Script for RunPod
Run this in your Jupyter notebook
"""

import subprocess
import time
import os
import signal

COMFYUI_DIR = "/workspace/ComfyUI"
COMFYUI_PORT = 8188

print("=" * 60)
print("ComfyUI Restart Script")
print("=" * 60)

# Step 1: Find and stop ComfyUI processes
print("\n1. Stopping ComfyUI...")
try:
    # Find processes
    result = subprocess.run(
        ['ps', 'aux'],
        capture_output=True,
        text=True
    )
    
    comfy_processes = []
    for line in result.stdout.split('\n'):
        if 'comfy' in line.lower() or ('python' in line.lower() and 'main.py' in line):
            parts = line.split()
            if len(parts) > 1:
                pid = int(parts[1])
                comfy_processes.append(pid)
    
    if comfy_processes:
        print(f"  Found {len(comfy_processes)} ComfyUI process(es)")
        for pid in comfy_processes:
            try:
                os.kill(pid, signal.SIGTERM)
                print(f"  ✓ Stopped process {pid}")
            except Exception as e:
                print(f"  ✗ Error stopping {pid}: {e}")
    else:
        print("  No ComfyUI processes found")
        
except Exception as e:
    print(f"  Error: {e}")

# Step 2: Wait for processes to fully stop
print("\n2. Waiting for processes to stop...")
time.sleep(10)

# Step 3: Verify processes are stopped
print("\n3. Verifying processes stopped...")
result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
remaining = [l for l in result.stdout.split('\n') if 'comfy' in l.lower() and 'grep' not in l.lower()]
if remaining:
    print(f"  ⚠ {len(remaining)} process(es) still running - forcing kill")
    for line in remaining:
        parts = line.split()
        if len(parts) > 1:
            try:
                os.kill(int(parts[1]), signal.SIGKILL)
            except:
                pass
    time.sleep(5)
else:
    print("  ✓ All processes stopped")

# Step 4: Start ComfyUI
print("\n4. Starting ComfyUI...")
os.chdir(COMFYUI_DIR)

# Start in background
comfy_process = subprocess.Popen(
    [
        'python', 'main.py',
        '--listen', '0.0.0.0',
        '--port', str(COMFYUI_PORT)
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    cwd=COMFYUI_DIR
)

print(f"  ✓ Started ComfyUI (PID: {comfy_process.pid})")
print(f"  Port: {COMFYUI_PORT}")

# Step 5: Wait and verify
print("\n5. Waiting for ComfyUI to start...")
time.sleep(15)

# Check if process is still running
if comfy_process.poll() is None:
    print("  ✓ ComfyUI process is running")
else:
    print("  ✗ ComfyUI process exited")
    stdout, stderr = comfy_process.communicate()
    print(f"  Error output: {stderr.decode()[:500]}")

print("\n" + "=" * 60)
print("Restart Complete!")
print("=" * 60)
print(f"\nComfyUI should be available at your RunPod URL")
print(f"Check the proxy URL provided by RunPod")
print("\nWait 30-60 seconds for ComfyUI to fully start and scan models")
print("=" * 60)
```

---

## Recommended Approach for Your Situation

Since you're using RunPod with ComfyUI Manager v3.37.2:

### Option 1: Via RunPod Dashboard (Easiest)

1. **Go to RunPod Dashboard**: https://www.runpod.io/console/pods
2. **Find your pod**
3. **Click "Stop"** (or "Pause")
4. **Wait 15 seconds**
5. **Click "Start"** (or "Resume")
6. **Wait for pod to be ready** (green status)
7. **Access ComfyUI** - it should rescan models on startup

### Option 2: Via Terminal/Notebook (If You Have Access)

```python
import subprocess
import time

# Stop ComfyUI
subprocess.run(['pkill', '-f', 'comfy'], capture_output=True)
time.sleep(10)

# Start ComfyUI (adjust path/command as needed)
subprocess.Popen(
    ['python', 'main.py', '--listen', '0.0.0.0', '--port', '8188'],
    cwd='/workspace/ComfyUI'
)

print("ComfyUI restarting... wait 30 seconds")
```

---

## After Restart - Verify Models Loaded

After restarting, run this to check if models are detected:

```python
import requests
import time

BASE_URL = "https://h2gpcwjzl8iavs-8188.proxy.runpod.net"

# Wait for ComfyUI to start
print("Waiting for ComfyUI to start...")
time.sleep(30)

# Check API
try:
    response = requests.get(f"{BASE_URL}/api/object_info", timeout=10)
    if response.status_code == 200:
        data = response.json()
        models = data['CheckpointLoaderSimple']['input']['required']['ckpt_name'][0]
        
        if len(models) > 0:
            print(f"✓ Found {len(models)} model(s):")
            for m in models:
                print(f"  - {m}")
            
            turbo = [m for m in models if 'turbo' in m.lower()]
            if turbo:
                print(f"\n✓ z_image_turbo FOUND!")
            else:
                print(f"\n✗ z_image_turbo still not found")
        else:
            print("✗ Model list still empty")
except Exception as e:
    print(f"Error: {e}")
```

---

## Troubleshooting

### ComfyUI Won't Stop

```bash
# Force kill all Python processes (be careful!)
pkill -9 python

# Or kill specific port
lsof -ti:8188 | xargs kill -9
```

### ComfyUI Won't Start

```bash
# Check if port is in use
lsof -i:8188

# Check ComfyUI logs
tail -f /workspace/ComfyUI/logs/*.log

# Check Python version
python --version  # Should be 3.10+

# Check dependencies
pip list | grep torch
```

### Models Still Not Showing After Restart

1. **Check ComfyUI logs** for scanning messages
2. **Verify file permissions**: `chmod 644 /workspace/ComfyUI/models/checkpoints/*.safetensors`
3. **Check file location**: Model should be directly in `checkpoints/` folder
4. **Try manual model load**: Use CheckpointLoaderSimple node and type filename manually

---

## Summary

**Best Method for RunPod**:
1. **Via RunPod Dashboard** - Stop/Start pod (safest, most reliable)
2. **Via Terminal** - `pkill -f comfy` then restart (if you have terminal access)
3. **Via Script** - Use the restart script above (automated)

**After Restart**: Wait 30-60 seconds for ComfyUI to scan models, then check Manager or API.

