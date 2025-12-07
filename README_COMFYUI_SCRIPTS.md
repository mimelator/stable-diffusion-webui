# ComfyUI Automation Scripts for RunPod

## Quick Start

### Option 1: Start in Foreground (Recommended for first time)
```bash
chmod +x /workspace/start_comfyui_auto.sh
/workspace/start_comfyui_auto.sh
```
- Runs in foreground so you can see output
- Press Ctrl+C to stop
- Good for debugging

### Option 2: Start in Background
```bash
chmod +x /workspace/start_comfyui_background.sh
/workspace/start_comfyui_background.sh
```
- Runs in background
- Logs to `/workspace/comfyui.log`
- Good for production use

---

## Scripts Overview

### `start_comfyui_auto.sh`
**Full-featured startup script that:**
1. ✅ Kills any existing ComfyUI processes
2. ✅ Checks and frees port 8188
3. ✅ Verifies CUDA is available
4. ✅ Verifies ComfyUI installation
5. ✅ Clears cache
6. ✅ Starts ComfyUI in foreground

**Usage:**
```bash
chmod +x /workspace/start_comfyui_auto.sh
/workspace/start_comfyui_auto.sh
```

**When to use:**
- First time setup
- Debugging issues
- When you want to see live output

---

### `start_comfyui_background.sh`
**Background startup script that:**
1. ✅ Kills existing processes
2. ✅ Frees port 8188
3. ✅ Verifies CUDA
4. ✅ Starts ComfyUI in background
5. ✅ Logs to `/workspace/comfyui.log`

**Usage:**
```bash
chmod +x /workspace/start_comfyui_background.sh
/workspace/start_comfyui_background.sh
```

**When to use:**
- Production/regular use
- When you want to run other commands
- When you want to close terminal

**View logs:**
```bash
tail -f /workspace/comfyui.log
```

**Check if running:**
```bash
ps aux | grep "python.*main.py" | grep -v grep
```

**Stop ComfyUI:**
```bash
pkill -f "python.*main.py"
```

---

## Making Scripts Persistent

### Option 1: Add to `.bashrc` (runs on login)
```bash
# Add alias to ~/.bashrc
echo 'alias start-comfyui="/workspace/start_comfyui_auto.sh"' >> ~/.bashrc
source ~/.bashrc

# Then just run:
start-comfyui
```

### Option 2: Create a systemd service (advanced)
Not recommended for RunPod Pods, but possible if you have systemd.

### Option 3: Add to Pod startup command
In RunPod dashboard, you can set a startup command that runs when Pod starts:
```bash
/workspace/start_comfyui_background.sh
```

---

## Quick Commands Reference

### Start ComfyUI
```bash
# Foreground
/workspace/start_comfyui_auto.sh

# Background
/workspace/start_comfyui_background.sh
```

### Stop ComfyUI
```bash
pkill -f "python.*main.py"
```

### Check if Running
```bash
ps aux | grep "python.*main.py" | grep -v grep
```

### View Logs (if using background script)
```bash
tail -f /workspace/comfyui.log
```

### Restart ComfyUI
```bash
# Just run the start script - it kills old processes first
/workspace/start_comfyui_auto.sh
```

---

## Troubleshooting

### Script says "CUDA not available"
- Check: `nvidia-smi`
- Check: `python3 -c "import torch; print(torch.cuda.is_available())"`
- Verify Pod has GPU attached in RunPod dashboard

### Script says "ComfyUI not found"
- Check path: `ls -la /workspace/runpod-slim/ComfyUI`
- Update `COMFYUI_PATH` in script if different

### Port 8188 still in use
- Script should handle this, but if not:
  ```bash
  fuser -k 8188/tcp
  # Or
  kill $(lsof -t -i :8188)
  ```

### Process won't die
- Force kill: `pkill -9 -f "python.*main.py"`
- Then restart with script

---

## Customization

### Change Port
Edit the script and change:
```bash
PORT=8188  # Change to your desired port
```

### Change ComfyUI Path
Edit the script and change:
```bash
COMFYUI_PATH="/workspace/runpod-slim/ComfyUI"  # Update if different
```

### Add Startup Arguments
Edit the `start_comfyui()` function and add arguments:
```bash
exec python3 main.py --listen 0.0.0.0 --port "$PORT" --lowvram
```

---

## Best Practices

1. **Always use the script** - Don't manually start ComfyUI, use the script to avoid conflicts
2. **Check logs** - If using background mode, check logs for errors
3. **Wait after Pod start** - If Pod just started, wait 10 seconds before running script
4. **One instance only** - The script ensures only one ComfyUI instance runs
5. **Save scripts to network volume** - Put scripts in `/workspace/` so they persist

---

## Example Workflow

```bash
# 1. After Pod starts, wait a moment
sleep 10

# 2. Start ComfyUI in background
/workspace/start_comfyui_background.sh

# 3. Check it started
ps aux | grep "python.*main.py" | grep -v grep

# 4. View logs if needed
tail -f /workspace/comfyui.log

# 5. Access ComfyUI via RunPod proxy URL
# (Dashboard → Pod → Connect → Port 8188)
```

---

## Files

- `start_comfyui_auto.sh` - Foreground startup script
- `start_comfyui_background.sh` - Background startup script
- `stop_comfyui.sh` - Manual stop script (if needed)
- `restart_comfyui_clean.sh` - Manual restart script (if needed)
