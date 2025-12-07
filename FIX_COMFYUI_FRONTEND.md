# Fix ComfyUI Frontend Version Warning

## Problem

You're seeing this warning:
```
WARNING: Installed frontend version 1.30.6 is lower than the recommended version 1.33.10.
Please install the updated requirements.txt file by running:
/workspace/runpod-slim/ComfyUI/.venv/bin/python -m pip install -r /workspace/runpod-slim/ComfyUI/requirements.txt
```

## Solution: Update Requirements on Network Storage

Since you're using network storage, we need to update the requirements in the ComfyUI installation that's stored on your network volume.

---

## Quick Fix (Copy-Paste This)

Run this in your RunPod terminal:

```bash
cat > /workspace/update_comfyui_requirements.sh << 'EOF'
#!/bin/bash
COMFYUI_PATH="/workspace/runpod-slim/ComfyUI"
VENV_PATH="$COMFYUI_PATH/.venv"

echo "=== Updating ComfyUI Requirements ==="

# Check if ComfyUI exists
if [ ! -d "$COMFYUI_PATH" ]; then
    echo "✗ ComfyUI not found at $COMFYUI_PATH"
    exit 1
fi

cd "$COMFYUI_PATH"

# Create venv if it doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate and update
echo "Activating virtual environment..."
source .venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing/updating requirements..."
pip install -r requirements.txt

echo ""
echo "✓ Requirements updated successfully!"
echo ""
echo "The frontend version warning should be gone on next startup."
EOF

chmod +x /workspace/update_comfyui_requirements.sh
/workspace/update_comfyui_requirements.sh
```

---

## What This Does

1. ✅ Creates a script on your network storage
2. ✅ Creates virtual environment if it doesn't exist
3. ✅ Activates the virtual environment
4. ✅ Updates pip
5. ✅ Installs/updates all requirements (including frontend)
6. ✅ Fixes the version warning

---

## After Running

1. **Restart ComfyUI** using your startup script:
   ```bash
   /workspace/start_comfyui_auto.sh
   ```

2. **The warning should be gone!** ✅

---

## Why This Works

- The virtual environment (`.venv`) is stored on your network volume
- Requirements are installed in the venv, not system-wide
- Your updated startup scripts will automatically use the venv Python
- Everything persists on network storage

---

## Manual Method (If Script Doesn't Work)

If you prefer to do it manually:

```bash
cd /workspace/runpod-slim/ComfyUI

# Create venv if needed
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Update requirements
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Verify It Worked

After updating and restarting ComfyUI, you should **NOT** see the frontend version warning anymore.

If you still see it:
1. Make sure you're using the updated startup scripts (they use the venv)
2. Check that the venv was created: `ls -la /workspace/runpod-slim/ComfyUI/.venv`
3. Verify requirements were installed: `/workspace/runpod-slim/ComfyUI/.venv/bin/pip list | grep comfyui`

---

## Notes

- This update is **permanent** on your network storage
- You only need to do this **once** (unless ComfyUI updates requirements again)
- The virtual environment persists across Pod restarts
- Your startup scripts now automatically use the venv if it exists
