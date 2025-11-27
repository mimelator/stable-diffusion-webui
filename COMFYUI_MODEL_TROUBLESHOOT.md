# ComfyUI Model Not Showing - Troubleshooting Guide

## Issue: Models Not Appearing in ComfyUI Manager

If models aren't showing up after restart, check the following:

---

## Quick Diagnostic Script

Run this in your RunPod notebook to check everything:

```python
import os
from pathlib import Path

COMFYUI_ROOT = "/workspace/ComfyUI"

print("=" * 60)
print("ComfyUI Model Diagnostic")
print("=" * 60)

# Check ComfyUI directory structure
print("\n1. Checking ComfyUI directory structure...")
if os.path.exists(COMFYUI_ROOT):
    print(f"✓ ComfyUI found at: {COMFYUI_ROOT}")
    
    models_dir = f"{COMFYUI_ROOT}/models"
    if os.path.exists(models_dir):
        print(f"✓ Models directory exists: {models_dir}")
        
        # Check subdirectories
        subdirs = ["checkpoints", "clip", "vae", "loras", "upscale_models"]
        for subdir in subdirs:
            subdir_path = f"{models_dir}/{subdir}"
            if os.path.exists(subdir_path):
                files = os.listdir(subdir_path)
                print(f"  ✓ {subdir}: {len(files)} files")
                if files:
                    for f in files[:5]:  # Show first 5 files
                        file_path = f"{subdir_path}/{f}"
                        if os.path.isfile(file_path):
                            size = os.path.getsize(file_path)
                            if size > 1024**3:  # > 1GB
                                print(f"    - {f} ({size/(1024**3):.2f} GB)")
                            elif size > 1024**2:  # > 1MB
                                print(f"    - {f} ({size/(1024**2):.2f} MB)")
                            else:
                                print(f"    - {f} ({size/1024:.2f} KB)")
            else:
                print(f"  ✗ {subdir}: directory not found")
    else:
        print(f"✗ Models directory not found: {models_dir}")
else:
    print(f"✗ ComfyUI not found at: {COMFYUI_ROOT}")
    print("\nTrying to find ComfyUI...")
    possible_paths = [
        "/workspace/ComfyUI",
        "/workspace/comfyui",
        "/ComfyUI",
        "/comfyui",
        "/workspace"
    ]
    for path in possible_paths:
        if os.path.exists(path):
            print(f"  Found: {path}")
            # Check if it's ComfyUI
            if os.path.exists(f"{path}/main.py") or os.path.exists(f"{path}/web"):
                print(f"    → This might be ComfyUI!")

# Check for z_image_turbo model specifically
print("\n2. Checking for z_image_turbo model...")
checkpoints_dir = f"{COMFYUI_ROOT}/models/checkpoints"
if os.path.exists(checkpoints_dir):
    files = os.listdir(checkpoints_dir)
    turbo_files = [f for f in files if "turbo" in f.lower() or "z_image" in f.lower()]
    
    if turbo_files:
        print(f"✓ Found {len(turbo_files)} turbo-related files:")
        for f in turbo_files:
            file_path = f"{checkpoints_dir}/{f}"
            if os.path.isfile(file_path):
                size_gb = os.path.getsize(file_path) / (1024**3)
                print(f"  ✓ {f} ({size_gb:.2f} GB)")
    else:
        print("✗ No z_image_turbo files found")
        print(f"\nFiles in checkpoints directory:")
        for f in files[:10]:
            print(f"  - {f}")
else:
    print(f"✗ Checkpoints directory not found: {checkpoints_dir}")

# Check file permissions
print("\n3. Checking file permissions...")
if os.path.exists(checkpoints_dir):
    files = os.listdir(checkpoints_dir)
    if files:
        test_file = f"{checkpoints_dir}/{files[0]}"
        if os.path.exists(test_file):
            perms = oct(os.stat(test_file).st_mode)[-3:]
            print(f"  File permissions: {perms}")
            if perms == "644" or perms == "755":
                print("  ✓ Permissions look good")
            else:
                print("  ⚠ Permissions might be restrictive")

print("\n" + "=" * 60)
print("Diagnostic Complete")
print("=" * 60)
```

---

## Common Issues & Fixes

### Issue 1: Model File in Wrong Location

**Problem**: Model downloaded to subdirectory instead of directly in checkpoints folder.

**Fix**:
```python
import os
import shutil

COMFYUI_ROOT = "/workspace/ComfyUI"
checkpoints_dir = f"{COMFYUI_ROOT}/models/checkpoints"

# Find model file (wherever it is)
def find_model_file():
    for root, dirs, files in os.walk(checkpoints_dir):
        for file in files:
            if "z_image_turbo" in file.lower() and file.endswith(".safetensors"):
                return os.path.join(root, file)
    return None

model_file = find_model_file()

if model_file:
    print(f"Found model at: {model_file}")
    
    # Move to correct location if needed
    correct_location = f"{checkpoints_dir}/z_image_turbo_bf16.safetensors"
    
    if model_file != correct_location:
        print(f"Moving to: {correct_location}")
        if os.path.exists(correct_location):
            print("  File already exists at correct location")
        else:
            shutil.move(model_file, correct_location)
            print("  ✓ Moved successfully")
            
            # Clean up empty directories
            try:
                os.removedirs(os.path.dirname(model_file))
            except:
                pass
    else:
        print("  ✓ Model already at correct location")
else:
    print("✗ Model file not found")
```

### Issue 2: ComfyUI Not Scanning Correct Directory

**Problem**: ComfyUI might be looking in a different location.

**Fix**: Check ComfyUI's config or find where it's actually looking:

```python
import os
import json

COMFYUI_ROOT = "/workspace/ComfyUI"

# Check for config files
config_files = [
    f"{COMFYUI_ROOT}/config.json",
    f"{COMFYUI_ROOT}/.config.json",
    f"{COMFYUI_ROOT}/extra_model_paths.yaml",
]

for config_file in config_files:
    if os.path.exists(config_file):
        print(f"Found config: {config_file}")
        try:
            with open(config_file, 'r') as f:
                if config_file.endswith('.yaml'):
                    import yaml
                    config = yaml.safe_load(f)
                else:
                    config = json.load(f)
                print(f"  Content: {config}")
        except Exception as e:
            print(f"  Could not read: {e}")
```

### Issue 3: File Permissions

**Problem**: Files might not be readable by ComfyUI.

**Fix**:
```python
import os
import stat

COMFYUI_ROOT = "/workspace/ComfyUI"
checkpoints_dir = f"{COMFYUI_ROOT}/models/checkpoints"

# Fix permissions
if os.path.exists(checkpoints_dir):
    for root, dirs, files in os.walk(checkpoints_dir):
        for d in dirs:
            os.chmod(os.path.join(root, d), stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        for f in files:
            os.chmod(os.path.join(root, f), stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    
    print("✓ Fixed file permissions")
```

### Issue 4: ComfyUI Manager Needs Refresh

**Problem**: ComfyUI Manager cache might be stale.

**Fix**:
1. **Hard refresh browser**: Ctrl+Shift+R or Cmd+Shift+R
2. **Clear browser cache** for the RunPod URL
3. **Restart ComfyUI** completely (not just refresh)
4. **Check ComfyUI logs** for errors

---

## Complete Fix Script

Run this comprehensive fix:

```python
import os
import shutil
import stat
from pathlib import Path

COMFYUI_ROOT = "/workspace/ComfyUI"

print("=" * 60)
print("ComfyUI Model Fix Script")
print("=" * 60)

# Step 1: Find model file
print("\n1. Finding model file...")
checkpoints_dir = f"{COMFYUI_ROOT}/models/checkpoints"

def find_all_model_files():
    """Find all safetensors files"""
    model_files = []
    if os.path.exists(checkpoints_dir):
        for root, dirs, files in os.walk(checkpoints_dir):
            for file in files:
                if file.endswith((".safetensors", ".ckpt", ".pt")):
                    model_files.append(os.path.join(root, file))
    return model_files

all_models = find_all_model_files()
print(f"Found {len(all_models)} model files")

# Find z_image_turbo specifically
turbo_models = [m for m in all_models if "turbo" in m.lower() or "z_image" in m.lower()]
if turbo_models:
    print(f"\nFound {len(turbo_models)} z_image_turbo files:")
    for m in turbo_models:
        size_gb = os.path.getsize(m) / (1024**3)
        print(f"  - {m} ({size_gb:.2f} GB)")
        
        # Move to correct location if in subdirectory
        if "split_files" in m or "diffusion_models" in m:
            correct_path = f"{checkpoints_dir}/z_image_turbo_bf16.safetensors"
            if not os.path.exists(correct_path):
                print(f"    Moving to: {correct_path}")
                shutil.move(m, correct_path)
                print(f"    ✓ Moved")
            else:
                print(f"    Already exists at correct location")
else:
    print("✗ No z_image_turbo files found")

# Step 2: Ensure correct directory structure
print("\n2. Ensuring directory structure...")
for subdir in ["checkpoints", "clip", "vae", "loras"]:
    dir_path = f"{COMFYUI_ROOT}/models/{subdir}"
    os.makedirs(dir_path, exist_ok=True)
    print(f"  ✓ {subdir}")

# Step 3: Fix permissions
print("\n3. Fixing file permissions...")
if os.path.exists(checkpoints_dir):
    for root, dirs, files in os.walk(checkpoints_dir):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o755)
        for f in files:
            os.chmod(os.path.join(root, f), 0o644)
    print("  ✓ Permissions fixed")

# Step 4: Verify final state
print("\n4. Verifying installation...")
final_model = f"{checkpoints_dir}/z_image_turbo_bf16.safetensors"
if os.path.exists(final_model):
    size_gb = os.path.getsize(final_model) / (1024**3)
    print(f"  ✓ Model at correct location: {size_gb:.2f} GB")
else:
    # Check if it's named differently
    files = os.listdir(checkpoints_dir)
    safetensor_files = [f for f in files if f.endswith(".safetensors")]
    if safetensor_files:
        print(f"  Found {len(safetensor_files)} safetensors files:")
        for f in safetensor_files:
            print(f"    - {f}")
    else:
        print("  ✗ No safetensors files found in checkpoints directory")

print("\n" + "=" * 60)
print("Fix Complete")
print("=" * 60)
print("\nNext steps:")
print("1. Hard refresh browser (Ctrl+Shift+R)")
print("2. Check ComfyUI Manager - models should appear")
print("3. If still not showing, check ComfyUI logs for errors")
print("=" * 60)
```

---

## Manual Check Commands

Run these commands in your RunPod terminal/notebook:

```bash
# Check if model file exists
ls -lh /workspace/ComfyUI/models/checkpoints/ | grep -i turbo

# Check file permissions
ls -la /workspace/ComfyUI/models/checkpoints/

# Find all safetensors files
find /workspace/ComfyUI/models -name "*.safetensors" -type f

# Check ComfyUI directory structure
tree -L 3 /workspace/ComfyUI/models/ 2>/dev/null || find /workspace/ComfyUI/models -maxdepth 3 -type d
```

---

## ComfyUI Manager Specific Issues

### If Using ComfyUI Manager Extension

1. **Check Manager Settings**:
   - Go to ComfyUI Manager settings
   - Verify model paths are correct
   - Check if custom paths are configured

2. **Refresh Model List**:
   - Look for "Refresh" or "Rescan" button in Manager
   - Or restart ComfyUI completely

3. **Check Manager Logs**:
   - Look for error messages in ComfyUI console
   - Check browser console (F12) for JavaScript errors

### Alternative: Use ComfyUI Directly

If Manager isn't working, you can still use models directly:

1. **Load model in workflow**:
   - Use "CheckpointLoaderSimple" node
   - Type model filename manually: `z_image_turbo_bf16.safetensors`
   - ComfyUI should find it

2. **Check ComfyUI's model list API**:
```python
import requests

# Check what ComfyUI sees
response = requests.get("https://h2gpcwjzl8iavs-8188.proxy.runpod.net/api/v1/models")
if response.status_code == 200:
    models = response.json()
    print("Models ComfyUI sees:")
    print(models)
else:
    print(f"Error: {response.status_code}")
```

---

## Quick Fix: Move Model to Root of Checkpoints

If the model is in a subdirectory, move it:

```python
import os
import shutil
import glob

COMFYUI_ROOT = "/workspace/ComfyUI"
checkpoints_dir = f"{COMFYUI_ROOT}/models/checkpoints"

# Find the model file (wherever it is)
model_pattern = f"{checkpoints_dir}/**/z_image_turbo*.safetensors"
model_files = glob.glob(model_pattern, recursive=True)

if model_files:
    for model_file in model_files:
        # Get just the filename
        filename = os.path.basename(model_file)
        target = f"{checkpoints_dir}/{filename}"
        
        if model_file != target:
            print(f"Moving: {model_file} → {target}")
            if os.path.exists(target):
                print(f"  Target already exists, skipping")
            else:
                shutil.move(model_file, target)
                print(f"  ✓ Moved")
                
                # Clean up empty parent directories
                try:
                    parent = os.path.dirname(model_file)
                    while parent != checkpoints_dir:
                        if not os.listdir(parent):
                            os.rmdir(parent)
                            parent = os.path.dirname(parent)
                        else:
                            break
                except:
                    pass
else:
    print("No z_image_turbo model files found")
    print(f"\nChecking what's in checkpoints directory:")
    if os.path.exists(checkpoints_dir):
        for item in os.listdir(checkpoints_dir):
            item_path = f"{checkpoints_dir}/{item}"
            if os.path.isdir(item_path):
                print(f"  Directory: {item}")
                # Check subdirectory
                for subitem in os.listdir(item_path):
                    print(f"    - {subitem}")
            else:
                size = os.path.getsize(item_path) / (1024**3)
                print(f"  File: {item} ({size:.2f} GB)")
```

---

## Summary

Most likely issues:
1. **Model in subdirectory** - Move to `models/checkpoints/` root
2. **File permissions** - Fix with chmod
3. **ComfyUI Manager cache** - Hard refresh browser
4. **Wrong directory** - Verify ComfyUI is looking in the right place

Run the diagnostic script first to identify the exact issue!

