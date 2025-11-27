# ComfyUI Manager Not Showing Models - Fix Guide

## Model File Verified ✓

Your model is correctly located at:
- `/workspace/ComfyUI/models/checkpoints/z_image_turbo_bf16.safetensors` (11.46 GB) ✓

But ComfyUI Manager isn't showing it. Here's how to fix:

---

## Solution 1: Force ComfyUI to Rescan Models

### Method A: Restart ComfyUI Completely

1. **Stop ComfyUI** completely (not just refresh)
2. **Wait 10 seconds**
3. **Start ComfyUI** again
4. **Hard refresh browser**: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)

### Method B: Clear ComfyUI Cache

Run this in your notebook:

```python
import os
import shutil

COMFYUI_ROOT = "/workspace/ComfyUI"

# Clear ComfyUI cache
cache_dirs = [
    f"{COMFYUI_ROOT}/.cache",
    f"{COMFYUI_ROOT}/__pycache__",
    f"{COMFYUI_ROOT}/models/.cache",
]

for cache_dir in cache_dirs:
    if os.path.exists(cache_dir):
        print(f"Clearing cache: {cache_dir}")
        shutil.rmtree(cache_dir)
        print(f"  ✓ Cleared")

print("\nCache cleared. Restart ComfyUI.")
```

---

## Solution 2: Check ComfyUI Manager Settings

### Via Web UI

1. Go to your ComfyUI Manager interface
2. Look for **Settings** or **Configuration** button
3. Check **Model Paths** settings:
   - Verify it's looking at: `/workspace/ComfyUI/models/checkpoints`
   - Check if there are custom paths configured
   - Look for "Rescan" or "Refresh Models" button

### Via API

Check what ComfyUI actually sees:

```python
import requests

# Your RunPod URL
BASE_URL = "https://h2gpcwjzl8iavs-8188.proxy.runpod.net"

# Check available models via API
try:
    response = requests.get(f"{BASE_URL}/api/v1/models")
    if response.status_code == 200:
        models = response.json()
        print("Models ComfyUI API sees:")
        print(f"  Checkpoints: {models.get('checkpoints', [])}")
        print(f"  Total: {len(models.get('checkpoints', []))} models")
        
        # Check if z_image_turbo is in the list
        checkpoints = models.get('checkpoints', [])
        turbo_models = [m for m in checkpoints if 'turbo' in m.lower()]
        if turbo_models:
            print(f"\n✓ Found z_image_turbo in API response:")
            for m in turbo_models:
                print(f"  - {m}")
        else:
            print("\n✗ z_image_turbo NOT found in API response")
            print("  This means ComfyUI isn't detecting it")
    else:
        print(f"API Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
```

---

## Solution 3: Verify File Permissions

```python
import os
import stat

COMFYUI_ROOT = "/workspace/ComfyUI"
model_file = f"{COMFYUI_ROOT}/models/checkpoints/z_image_turbo_bf16.safetensors"

if os.path.exists(model_file):
    # Check current permissions
    current_perms = oct(os.stat(model_file).st_mode)[-3:]
    print(f"Current permissions: {current_perms}")
    
    # Fix permissions (readable by all)
    os.chmod(model_file, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    new_perms = oct(os.stat(model_file).st_mode)[-3:]
    print(f"New permissions: {new_perms}")
    print("✓ Permissions fixed")
    
    # Also fix directory permissions
    checkpoints_dir = f"{COMFYUI_ROOT}/models/checkpoints"
    os.chmod(checkpoints_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    print("✓ Directory permissions fixed")
else:
    print("Model file not found")
```

---

## Solution 4: Check ComfyUI Logs

Look for errors in ComfyUI startup logs:

```python
# Check if there are log files
import os
import glob

COMFYUI_ROOT = "/workspace/ComfyUI"

log_files = glob.glob(f"{COMFYUI_ROOT}/**/*.log", recursive=True)
log_files += glob.glob(f"{COMFYUI_ROOT}/**/logs/**/*", recursive=True)

if log_files:
    print("Found log files:")
    for log_file in log_files[:5]:  # Show first 5
        print(f"  - {log_file}")
        # Check last few lines for errors
        try:
            with open(log_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    print(f"    Last line: {lines[-1].strip()}")
        except:
            pass
else:
    print("No log files found")
    print("\nCheck ComfyUI console output for errors")
```

---

## Solution 5: Manual Model Loading Test

Test if ComfyUI can actually load the model (bypass Manager):

### Create Test Workflow JSON

```python
import json

# Test workflow to load z_image_turbo
test_workflow = {
    "1": {
        "inputs": {
            "ckpt_name": "z_image_turbo_bf16.safetensors"
        },
        "class_type": "CheckpointLoaderSimple",
        "_meta": {
            "title": "Load Checkpoint"
        }
    },
    "2": {
        "inputs": {
            "text": "test prompt",
            "clip": ["1", 1]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {
            "title": "CLIP Text Encode (Prompt)"
        }
    }
}

# Save workflow
with open("/tmp/test_workflow.json", "w") as f:
    json.dump(test_workflow, f, indent=2)

print("Test workflow created: /tmp/test_workflow.json")
print("\nTry loading this workflow in ComfyUI to test if model loads")
```

### Or Test via API

```python
import requests
import json

BASE_URL = "https://h2gpcwjzl8iavs-8188.proxy.runpod.net"

# Simple test - queue a generation with the model
test_prompt = {
    "prompt": {
        "1": {
            "inputs": {
                "ckpt_name": "z_image_turbo_bf16.safetensors"
            },
            "class_type": "CheckpointLoaderSimple"
        },
        "2": {
            "inputs": {
                "text": "test",
                "clip": ["1", 1]
            },
            "class_type": "CLIPTextEncode"
        }
    }
}

try:
    response = requests.post(f"{BASE_URL}/api/v1/prompt", json=test_prompt)
    if response.status_code == 200:
        print("✓ Workflow queued successfully - model can be loaded!")
        print(response.json())
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Error: {e}")
```

---

## Solution 6: Check ComfyUI Manager Extension

### If Using ComfyUI Manager Extension

1. **Check Extension Status**:
   - Go to ComfyUI Manager settings
   - Verify extension is enabled
   - Check for updates

2. **Reinstall/Update Manager**:
   ```bash
   cd /workspace/ComfyUI
   # If Manager is a custom_nodes extension
   cd custom_nodes
   # Check if ComfyUI-Manager exists
   ls -la | grep -i manager
   ```

3. **Manual Refresh**:
   - Look for "Refresh Models" button
   - Or "Rescan" button
   - Or restart ComfyUI

---

## Solution 7: Direct File Check

Verify ComfyUI can actually read the file:

```python
import os

COMFYUI_ROOT = "/workspace/ComfyUI"
model_file = f"{COMFYUI_ROOT}/models/checkpoints/z_image_turbo_bf16.safetensors"

# Check file exists and is readable
if os.path.exists(model_file):
    print(f"✓ File exists: {model_file}")
    
    # Check if readable
    if os.access(model_file, os.R_OK):
        print("✓ File is readable")
    else:
        print("✗ File is NOT readable - fixing permissions...")
        os.chmod(model_file, 0o644)
        print("✓ Permissions fixed")
    
    # Check file size
    size_gb = os.path.getsize(model_file) / (1024**3)
    print(f"✓ File size: {size_gb:.2f} GB")
    
    # Check file extension
    if model_file.endswith(".safetensors"):
        print("✓ File extension is correct (.safetensors)")
    else:
        print("⚠ File extension might be wrong")
    
    # Try to read first few bytes (sanity check)
    try:
        with open(model_file, 'rb') as f:
            header = f.read(16)
            print(f"✓ File is readable (header: {header[:8]})")
    except Exception as e:
        print(f"✗ Cannot read file: {e}")
else:
    print(f"✗ File not found: {model_file}")
```

---

## Most Likely Solutions (In Order)

1. **Hard refresh browser** + **Full ComfyUI restart** (most common fix)
2. **Check ComfyUI Manager settings** - verify model paths
3. **Clear cache** and restart
4. **Check file permissions** - ensure readable
5. **Test via API** - see if ComfyUI can actually load it

---

## Quick All-in-One Fix

Run this complete fix script:

```python
import os
import stat
import requests

COMFYUI_ROOT = "/workspace/ComfyUI"
BASE_URL = "https://h2gpcwjzl8iavs-8188.proxy.runpod.net"
model_file = f"{COMFYUI_ROOT}/models/checkpoints/z_image_turbo_bf16.safetensors"

print("=" * 60)
print("Complete ComfyUI Model Fix")
print("=" * 60)

# Step 1: Verify file exists
print("\n1. Verifying model file...")
if os.path.exists(model_file):
    size_gb = os.path.getsize(model_file) / (1024**3)
    print(f"  ✓ Model file exists ({size_gb:.2f} GB)")
else:
    print("  ✗ Model file not found!")
    exit(1)

# Step 2: Fix permissions
print("\n2. Fixing permissions...")
os.chmod(model_file, 0o644)
os.chmod(f"{COMFYUI_ROOT}/models/checkpoints", 0o755)
print("  ✓ Permissions fixed")

# Step 3: Check what ComfyUI API sees
print("\n3. Checking ComfyUI API...")
try:
    response = requests.get(f"{BASE_URL}/api/v1/models", timeout=5)
    if response.status_code == 200:
        models = response.json()
        checkpoints = models.get('checkpoints', [])
        print(f"  ComfyUI sees {len(checkpoints)} checkpoint(s)")
        
        turbo_models = [m for m in checkpoints if 'turbo' in m.lower()]
        if turbo_models:
            print(f"  ✓ z_image_turbo found in API!")
            for m in turbo_models:
                print(f"    - {m}")
        else:
            print("  ✗ z_image_turbo NOT in API response")
            print("  → ComfyUI needs to be restarted")
    else:
        print(f"  ⚠ API returned: {response.status_code}")
except Exception as e:
    print(f"  ⚠ Could not check API: {e}")

print("\n" + "=" * 60)
print("Fix Complete!")
print("=" * 60)
print("\nNext steps:")
print("1. FULLY restart ComfyUI (stop and start)")
print("2. Hard refresh browser (Ctrl+Shift+R)")
print("3. Check ComfyUI Manager - model should appear")
print("4. If still not showing, check Manager settings")
print("=" * 60)
```

---

## Summary

Your model file is in the correct location. The issue is likely:

1. **ComfyUI Manager cache** - needs hard refresh + restart
2. **ComfyUI needs full restart** - not just page refresh
3. **Manager extension issue** - may need update or reconfiguration

**Try these in order**:
1. Hard refresh browser (`Ctrl+Shift+R`)
2. Fully restart ComfyUI (stop completely, wait, start again)
3. Run the API check script above to see if ComfyUI detects it
4. Check ComfyUI Manager settings/paths

The model file itself is fine - it's just a matter of getting ComfyUI Manager to detect it!

