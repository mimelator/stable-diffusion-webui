# CUDA Errors with Network Storage - Theory & Solutions

## Overview

When using RunPod network volumes with ComfyUI, CUDA errors can occur due to the interaction between network storage latency, model loading, and GPU initialization. This document theorizes the most likely causes and provides solutions.

---

## Most Likely Causes

### 0. **CUDA Driver Initialization Failed - No GPU Access** ⚠️ **CRITICAL - CHECK FIRST**

**Problem**: 
- The Pod doesn't have GPU access or CUDA drivers aren't properly initialized
- This is the most common cause of "CUDA driver initialization failed" errors
- The error occurs before ComfyUI even tries to load models

**Symptoms**:
- Error: `RuntimeError: CUDA driver initialization failed, you might not have a CUDA gpu.`
- Error occurs at startup during `torch.cuda.current_device()` call
- `nvidia-smi` may or may not work (depends on the issue)

**Immediate Diagnostic Steps**:
```bash
# 1. Check if GPU is accessible
nvidia-smi

# 2. Check PyTorch CUDA
python3 -c "import torch; print('CUDA available:', torch.cuda.is_available())"

# 3. Check for NVIDIA devices
ls -la /dev/nvidia*

# 4. Check CUDA_VISIBLE_DEVICES
echo $CUDA_VISIBLE_DEVICES
```

**Solutions**:

**Solution A: Pod Doesn't Have GPU**
- Go to RunPod dashboard → Your Pod → Check GPU status
- Ensure Pod was deployed with a GPU (not CPU-only)
- If no GPU, terminate and redeploy with GPU selected

**Solution B: GPU Not Visible to Container**
- Restart the Pod (sometimes fixes device visibility)
- Check Pod template has GPU support enabled
- Verify you're using a GPU-enabled template

**Solution C: CUDA Drivers Not Installed**
- Check if nvidia-smi works
- If not, the Pod template may be missing GPU drivers
- Try a different Pod template (e.g., official ComfyUI template)

**Solution D: CUDA_VISIBLE_DEVICES Issue**
```bash
# Unset if incorrectly set
unset CUDA_VISIBLE_DEVICES

# Or set correctly (usually not needed)
export CUDA_VISIBLE_DEVICES=0
```

**Solution E: Start ComfyUI with CPU Fallback (Temporary)**
```bash
# This won't work for generation but helps diagnose
# ComfyUI doesn't officially support CPU-only, but you can check if it starts
cd /workspace/runpod-slim/ComfyUI
CUDA_VISIBLE_DEVICES="" python3 main.py --listen 0.0.0.0 --port 8188 --cpu
```

**Prevention**:
- Always verify GPU is attached when deploying Pod
- Use official RunPod templates that have GPU support
- Check `nvidia-smi` works before starting ComfyUI

---

### 1. **Network Volume Not Fully Mounted When ComfyUI Starts** ⚠️ **MOST LIKELY (if GPU works)**

**Problem**: 
- Network volumes can take a few seconds to fully mount and become accessible
- If ComfyUI starts immediately after Pod deployment, it may try to access model files before the volume is ready
- This causes file I/O errors that manifest as CUDA errors during model loading

**Symptoms**:
- CUDA errors appear immediately on startup
- Errors mention file access, model loading, or tensor operations
- Works fine if you wait a bit before starting ComfyUI

**Solution**:
```bash
# Wait for volume to be fully mounted before starting ComfyUI
# Check if volume is ready:
df -h /workspace

# Verify files are accessible (note: path may be /workspace/runpod-slim/ComfyUI):
ls -lh /workspace/runpod-slim/ComfyUI/models/unet/

# Add a delay in your startup script:
sleep 10  # Wait 10 seconds after Pod starts
cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8188
```

**Prevention**:
- Always verify volume is mounted before starting ComfyUI
- Use a startup script that checks volume readiness
- Wait 10-15 seconds after Pod deployment before starting ComfyUI

---

### 2. **Model Files Corrupted or Incomplete** ⚠️ **VERY LIKELY**

**Problem**:
- Network volumes can have issues during writes
- If a previous Pod terminated while writing models, files might be corrupted
- Partial file writes can cause CUDA errors when loading models

**Symptoms**:
- CUDA errors when loading specific models
- Errors mention "corrupted", "invalid", or "unexpected EOF"
- Some models work, others don't

**Solution**:
```bash
# Check file integrity
cd /workspace/ComfyUI/models

# Check file sizes (should match expected sizes)
# Note: Path may be /workspace/runpod-slim/ComfyUI/models/ or /workspace/ComfyUI/models/
ls -lh /workspace/runpod-slim/ComfyUI/models/unet/z_image_turbo_bf16.safetensors  # Should be ~11.46 GB
ls -lh /workspace/runpod-slim/ComfyUI/models/clip/qwen_3_4b.safetensors            # Should be ~7.49 GB
ls -lh /workspace/runpod-slim/ComfyUI/models/vae/ae.safetensors                    # Should be ~0.31 GB

# Check for incomplete files (smaller than expected)
# Note: Adjust path as needed
find /workspace/runpod-slim/ComfyUI/models -name "*.safetensors" -exec ls -lh {} \; | awk '$5 < 1000000 {print "SUSPICIOUS: " $0}'

# Re-download corrupted files if needed
```

**Prevention**:
- Always verify file sizes after downloads
- Use checksums if available
- Don't terminate Pods while models are downloading

---

### 3. **I/O Timeout During Model Loading** ⚠️ **LIKELY**

**Problem**:
- Network storage has higher latency than local storage
- Large model files (11GB+) take longer to read over network
- If there's a timeout or network hiccup during loading, CUDA operations can fail

**Symptoms**:
- CUDA errors during model loading phase
- Errors might mention "timeout", "connection", or "I/O error"
- Intermittent failures (works sometimes, fails other times)

**Solution**:
```bash
# Pre-load models into memory cache before starting ComfyUI
# This ensures files are accessible

# Option 1: Touch all model files to ensure they're cached
find /workspace/ComfyUI/models -name "*.safetensors" -exec touch {} \;

# Option 2: Read first few MB of each file to warm cache
for file in /workspace/ComfyUI/models/unet/*.safetensors; do
    head -c 10485760 "$file" > /dev/null  # Read first 10MB
done

# Then start ComfyUI
cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8188
```

**Prevention**:
- Use a startup script that pre-warms the cache
- Consider copying critical models to local tmpfs if available
- Monitor network volume performance

---

### 4. **File Permissions Issues** ⚠️ **POSSIBLE**

**Problem**:
- Network volumes might mount with different permissions
- ComfyUI might not have read access to model files
- This causes file access errors that look like CUDA errors

**Symptoms**:
- CUDA errors mentioning "permission denied" or "access denied"
- Errors when trying to open model files

**Solution**:
```bash
# Fix permissions on all model files
# Note: Adjust path as needed (/workspace/runpod-slim/ComfyUI or /workspace/ComfyUI)
chmod -R 644 /workspace/runpod-slim/ComfyUI/models/**/*.safetensors
chmod -R 755 /workspace/runpod-slim/ComfyUI/models

# Verify permissions
ls -la /workspace/runpod-slim/ComfyUI/models/unet/
```

**Prevention**:
- Set correct permissions when initially setting up the volume
- Document permission requirements

---

### 5. **GPU Memory Allocation During Slow I/O** ⚠️ **POSSIBLE**

**Problem**:
- ComfyUI tries to allocate GPU memory while loading models
- If model loading is slow (network I/O), GPU memory allocation can timeout
- This causes CUDA out-of-memory or allocation errors

**Symptoms**:
- CUDA errors mentioning "out of memory" or "allocation failed"
- Errors occur during model loading, not during generation

**Solution**:
```bash
# Start ComfyUI with memory optimizations
cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8188 --lowvram

# Or use medvram
python main.py --listen 0.0.0.0 --port 8188 --medvram

# Check GPU memory before starting
nvidia-smi
```

**Prevention**:
- Use appropriate memory flags for your GPU
- Monitor GPU memory usage
- Consider using a GPU with more VRAM

---

### 6. **Stale Cache or Lock Files** ⚠️ **POSSIBLE**

**Problem**:
- ComfyUI might have cached model information from a previous session
- Lock files from a previous Pod might still exist
- This causes conflicts when loading models

**Symptoms**:
- CUDA errors that mention "locked" or "in use"
- Errors about model already loaded

**Solution**:
```bash
# Clear ComfyUI cache and lock files
# Note: Adjust path as needed
cd /workspace/runpod-slim/ComfyUI

# Remove cache directories
rm -rf .cache __pycache__ models/.cache

# Remove any lock files
find . -name "*.lock" -delete
find . -name "*.tmp" -delete

# Restart ComfyUI
python3 main.py --listen 0.0.0.0 --port 8188
```

**Prevention**:
- Clear cache between Pod sessions
- Use a startup script that cleans up before starting

---

### 7. **Python/CUDA Environment Mismatch** ⚠️ **LESS LIKELY**

**Problem**:
- Different Pods might have slightly different Python/CUDA versions
- Models saved with one version might not load correctly with another
- This can cause CUDA errors

**Symptoms**:
- CUDA errors mentioning version mismatches
- Errors about tensor types or operations

**Solution**:
```bash
# Check Python and CUDA versions
python --version
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.version.cuda)"

# Ensure consistent environment
# Use the same Pod template each time
```

**Prevention**:
- Use the same Pod template for all deployments
- Document Python/CUDA versions
- Consider using a container image

---

## Diagnostic Steps

### Step 1: Verify Volume Mount

```bash
# Check if volume is mounted
df -h /workspace

# Should show your network volume with correct size
# If not mounted, wait a few seconds and check again
```

### Step 2: Verify File Accessibility

```bash
# Check if files are accessible
# Note: Adjust path as needed
cd /workspace/runpod-slim/ComfyUI/models

# List files
ls -lh unet/
ls -lh clip/
ls -lh vae/

# Try reading a small portion of each file
head -c 1024 unet/z_image_turbo_bf16.safetensors > /dev/null && echo "UNet readable"
head -c 1024 clip/qwen_3_4b.safetensors > /dev/null && echo "CLIP readable"
head -c 1024 vae/ae.safetensors > /dev/null && echo "VAE readable"
```

### Step 3: Check File Integrity

```bash
# Verify file sizes match expected values
du -h /workspace/ComfyUI/models/unet/z_image_turbo_bf16.safetensors  # Should be ~11.46 GB
du -h /workspace/ComfyUI/models/clip/qwen_3_4b.safetensors            # Should be ~7.49 GB
du -h /workspace/ComfyUI/models/vae/ae.safetensors                    # Should be ~0.31 GB

# Check for file corruption (this will take a while for large files)
# file /workspace/ComfyUI/models/unet/z_image_turbo_bf16.safetensors
```

### Step 4: Test GPU Access

```bash
# Verify CUDA is available
python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('CUDA device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"

# Check GPU memory
nvidia-smi
```

### Step 5: Start ComfyUI with Verbose Logging

```bash
# Start ComfyUI with more verbose output
# Note: Adjust path as needed
cd /workspace/runpod-slim/ComfyUI
python3 main.py --listen 0.0.0.0 --port 8188 2>&1 | tee comfyui.log

# Watch for errors in the log
# Look for file access errors, CUDA errors, or model loading errors
```

---

## Recommended Startup Script

Create a startup script that handles all these issues:

```bash
#!/bin/bash
# save as: /workspace/start_comfyui.sh

set -e  # Exit on error

echo "=== ComfyUI Startup Script ==="
echo "Waiting for network volume to be ready..."

# Wait for volume to mount
# Note: ComfyUI may be at /workspace/runpod-slim/ComfyUI or /workspace/ComfyUI
MAX_WAIT=30
WAITED=0
COMFYUI_PATH=""

# Try common locations
for path in "/workspace/runpod-slim/ComfyUI" "/workspace/ComfyUI"; do
    if [ -d "$path" ]; then
        COMFYUI_PATH="$path"
        break
    fi
done

# Wait for one of them to appear
while [ -z "$COMFYUI_PATH" ] && [ $WAITED -lt $MAX_WAIT ]; do
    sleep 1
    WAITED=$((WAITED + 1))
    for path in "/workspace/runpod-slim/ComfyUI" "/workspace/ComfyUI"; do
        if [ -d "$path" ]; then
            COMFYUI_PATH="$path"
            break
        fi
    done
    echo "  Waiting... ($WAITED/$MAX_WAIT)"
done

if [ -z "$COMFYUI_PATH" ]; then
    echo "ERROR: ComfyUI directory not found after $MAX_WAIT seconds"
    exit 1
fi

echo "✓ ComfyUI directory found at: $COMFYUI_PATH"

# Verify files are accessible
echo "Verifying model files..."
cd "$COMFYUI_PATH/models"

REQUIRED_FILES=(
    "unet/z_image_turbo_bf16.safetensors"
    "clip/qwen_3_4b.safetensors"
    "vae/ae.safetensors"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "ERROR: Required file not found: $file"
        exit 1
    fi
    echo "  ✓ $file"
done

# Fix permissions
echo "Fixing permissions..."
chmod -R 644 "$COMFYUI_PATH/models"/**/*.safetensors 2>/dev/null || true
chmod -R 755 "$COMFYUI_PATH/models" 2>/dev/null || true

# Clear cache
echo "Clearing cache..."
rm -rf "$COMFYUI_PATH/.cache" "$COMFYUI_PATH/__pycache__" "$COMFYUI_PATH/models/.cache" 2>/dev/null || true

# Pre-warm cache (read first 10MB of each model)
echo "Pre-warming cache..."
for file in "$COMFYUI_PATH/models/unet"/*.safetensors; do
    [ -f "$file" ] && head -c 10485760 "$file" > /dev/null 2>&1 || true
done

# Check CUDA
echo "Checking CUDA..."
python3 -c "import torch; assert torch.cuda.is_available(), 'CUDA not available'; print('✓ CUDA available')" || {
    echo "ERROR: CUDA not available"
    exit 1
}

# Start ComfyUI
echo "Starting ComfyUI..."
cd "$COMFYUI_PATH"
exec python3 main.py --listen 0.0.0.0 --port 8188
```

Make it executable:
```bash
chmod +x /workspace/start_comfyui.sh
```

Use it:
```bash
/workspace/start_comfyui.sh
```

---

## Quick Fix Checklist

When you get CUDA errors, try these in order:

1. ✅ **Wait 10-15 seconds** after Pod starts before launching ComfyUI
2. ✅ **Verify volume is mounted**: `df -h /workspace`
3. ✅ **Check file sizes**: `ls -lh /workspace/runpod-slim/ComfyUI/models/unet/` (or `/workspace/ComfyUI/models/unet/`)
4. ✅ **Fix permissions**: `chmod -R 644 /workspace/runpod-slim/ComfyUI/models/**/*.safetensors`
5. ✅ **Clear cache**: `rm -rf /workspace/runpod-slim/ComfyUI/.cache`
6. ✅ **Pre-warm cache**: `head -c 10485760 /workspace/runpod-slim/ComfyUI/models/unet/*.safetensors > /dev/null`
7. ✅ **Check CUDA**: `python3 -c "import torch; print(torch.cuda.is_available())"`
8. ✅ **Start with verbose logging**: `cd /workspace/runpod-slim/ComfyUI && python3 main.py --listen 0.0.0.0 --port 8188 2>&1 | tee comfyui.log`

---

## Most Common Scenario

Based on the symptoms (CUDA errors on startup with network storage), the **most likely cause is #1: Network volume not fully mounted when ComfyUI starts**.

**Quick fix**: Always wait 10-15 seconds after Pod deployment before starting ComfyUI, or use the startup script above.

---

## Next Steps

1. **When you get the exact error logs**, we can pinpoint the specific issue
2. **Try the startup script** - it handles most common issues automatically
3. **Monitor the logs** - ComfyUI startup logs will show where it's failing
4. **Check RunPod status** - Sometimes network volumes have temporary issues

---

## Additional Resources

- RunPod Network Volumes Docs: https://docs.runpod.io/storage/network-volumes
- ComfyUI Troubleshooting: See `COMFYUI_MODEL_TROUBLESHOOT.md`
- Volume Persistence Test: See `RUNPOD_VOLUME_PERSISTENCE_TEST.md`
