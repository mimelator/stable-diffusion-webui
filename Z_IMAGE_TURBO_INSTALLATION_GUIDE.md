# Complete z_image_turbo Installation Guide for ComfyUI

## Overview

This guide covers the complete installation of **z_image_turbo** model components for ComfyUI on RunPod (or any ComfyUI instance). z_image_turbo uses a split model format with separate UNet, CLIP, and VAE files.

**Model Repository**: [Comfy-Org/z_image_turbo](https://huggingface.co/Comfy-Org/z_image_turbo)

---

## Prerequisites

- ComfyUI installed and running
- Hugging Face account (for API access)
- Python environment with `huggingface_hub` library
- Sufficient disk space (~20 GB total)

---

## Required Files

z_image_turbo requires **three separate files**:

1. **UNet (Diffusion Model)**: `z_image_turbo_bf16.safetensors` (~11.46 GB)
   - Location: `models/unet/`

2. **CLIP (Text Encoder)**: `qwen_3_4b.safetensors` (~7.49 GB)
   - Location: `models/clip/`

3. **VAE (Variational Autoencoder)**: `ae.safetensors` (~0.31 GB)
   - Location: `models/vae/`

**Total Size**: ~19.26 GB

---

## Installation Steps

### Step 1: Install Dependencies

In your RunPod notebook or terminal:

```python
!pip install huggingface_hub -q
```

### Step 2: Set Up Configuration

```python
import os
from huggingface_hub import hf_hub_download, login

# Configuration
HF_API_KEY = "your_huggingface_api_key_here"  # Get from https://huggingface.co/settings/tokens
REPO_ID = "Comfy-Org/z_image_turbo"
COMFYUI_ROOT = "/workspace/runpod-slim/ComfyUI"  # Adjust for your setup
```

**Note**: For RunPod templates, the path is typically `/workspace/runpod-slim/ComfyUI`. For local installations, it's usually `./ComfyUI` or your custom path.

### Step 3: Login to Hugging Face

```python
login(token=HF_API_KEY)
print("✓ Logged into Hugging Face")
```

### Step 4: Create Required Directories

```python
# Create all necessary directories
directories = [
    f"{COMFYUI_ROOT}/models/unet",
    f"{COMFYUI_ROOT}/models/clip",
    f"{COMFYUI_ROOT}/models/vae",
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"✓ Created: {directory}")
```

### Step 5: Download UNet (Diffusion Model)

```python
print("\n📥 Downloading UNet (z_image_turbo_bf16.safetensors)...")
print("This is the largest file (~11.46 GB) and may take 10-20 minutes...")

unet_path = hf_hub_download(
    repo_id=REPO_ID,
    filename="z_image_turbo_bf16.safetensors",
    local_dir=f"{COMFYUI_ROOT}/models/unet",
    local_dir_use_symlinks=False
)

# Verify download
if os.path.exists(f"{COMFYUI_ROOT}/models/unet/z_image_turbo_bf16.safetensors"):
    size_gb = os.path.getsize(f"{COMFYUI_ROOT}/models/unet/z_image_turbo_bf16.safetensors") / (1024**3)
    print(f"✓ UNet downloaded: {size_gb:.2f} GB")
else:
    print("⚠ File may be in subdirectory, checking...")
    # Handle subdirectory case
    import shutil
    for root, dirs, files in os.walk(f"{COMFYUI_ROOT}/models/unet"):
        for file in files:
            if file == "z_image_turbo_bf16.safetensors":
                file_path = os.path.join(root, file)
                target = f"{COMFYUI_ROOT}/models/unet/{file}"
                if file_path != target:
                    shutil.move(file_path, target)
                    print(f"✓ Moved to correct location: {target}")
```

### Step 6: Download CLIP (Text Encoder)

```python
print("\n📥 Downloading CLIP (qwen_3_4b.safetensors)...")
print("This file is ~7.49 GB and may take 5-10 minutes...")

clip_path = hf_hub_download(
    repo_id=REPO_ID,
    filename="split_files/text_encoders/qwen_3_4b.safetensors",
    local_dir=f"{COMFYUI_ROOT}/models/clip",
    local_dir_use_symlinks=False
)

# Move from subdirectory if needed
import shutil
clip_file = f"{COMFYUI_ROOT}/models/clip/split_files/text_encoders/qwen_3_4b.safetensors"
target_clip = f"{COMFYUI_ROOT}/models/clip/qwen_3_4b.safetensors"

if os.path.exists(clip_file) and not os.path.exists(target_clip):
    shutil.move(clip_file, target_clip)
    # Clean up empty directories
    try:
        os.removedirs(f"{COMFYUI_ROOT}/models/clip/split_files/text_encoders")
        os.removedirs(f"{COMFYUI_ROOT}/models/clip/split_files")
    except:
        pass

if os.path.exists(target_clip):
    size_gb = os.path.getsize(target_clip) / (1024**3)
    print(f"✓ CLIP downloaded: {size_gb:.2f} GB")
```

### Step 7: Download VAE

```python
print("\n📥 Downloading VAE (ae.safetensors)...")
print("This file is ~0.31 GB and should download quickly...")

vae_path = hf_hub_download(
    repo_id=REPO_ID,
    filename="split_files/vae/ae.safetensors",
    local_dir=f"{COMFYUI_ROOT}/models/vae",
    local_dir_use_symlinks=False
)

# Move from subdirectory if needed
vae_file = f"{COMFYUI_ROOT}/models/vae/split_files/vae/ae.safetensors"
target_vae = f"{COMFYUI_ROOT}/models/vae/ae.safetensors"

if os.path.exists(vae_file) and not os.path.exists(target_vae):
    shutil.move(vae_file, target_vae)
    # Clean up empty directories
    try:
        os.removedirs(f"{COMFYUI_ROOT}/models/vae/split_files/vae")
        os.removedirs(f"{COMFYUI_ROOT}/models/vae/split_files")
    except:
        pass

if os.path.exists(target_vae):
    size_gb = os.path.getsize(target_vae) / (1024**3)
    print(f"✓ VAE downloaded: {size_gb:.2f} GB")
```

### Step 8: Verify Installation

```python
print("\n" + "=" * 60)
print("Installation Verification")
print("=" * 60)

files_to_check = {
    "UNet": f"{COMFYUI_ROOT}/models/unet/z_image_turbo_bf16.safetensors",
    "CLIP": f"{COMFYUI_ROOT}/models/clip/qwen_3_4b.safetensors",
    "VAE": f"{COMFYUI_ROOT}/models/vae/ae.safetensors"
}

all_found = True
total_size = 0

for component, file_path in files_to_check.items():
    if os.path.exists(file_path):
        size_gb = os.path.getsize(file_path) / (1024**3)
        total_size += size_gb
        print(f"✓ {component}: {size_gb:.2f} GB")
        print(f"  Location: {file_path}")
    else:
        print(f"✗ {component}: NOT FOUND")
        print(f"  Expected: {file_path}")
        all_found = False

print("\n" + "-" * 60)
print(f"Total size: {total_size:.2f} GB")

if all_found:
    print("\n🎉 All files installed successfully!")
    print("\nNext steps:")
    print("1. Restart ComfyUI or wait 30-60 seconds for rescan")
    print("2. Load your workflow")
    print("3. The model should be available in ComfyUI")
else:
    print("\n⚠ Some files are missing - check the errors above")
```

---

## Complete Installation Script

Here's a complete script you can run all at once:

```python
#!/usr/bin/env python3
"""
Complete z_image_turbo Installation Script for ComfyUI
Run this in your RunPod notebook or terminal
"""

import os
import shutil
from huggingface_hub import hf_hub_download, login

# ============================================================================
# CONFIGURATION - EDIT THESE VALUES
# ============================================================================
HF_API_KEY = "your_huggingface_api_key_here"  # Get from https://huggingface.co/settings/tokens
REPO_ID = "Comfy-Org/z_image_turbo"
COMFYUI_ROOT = "/workspace/runpod-slim/ComfyUI"  # Adjust for your setup

# ============================================================================
# INSTALLATION
# ============================================================================

print("=" * 60)
print("z_image_turbo Installation for ComfyUI")
print("=" * 60)

# Step 1: Login
print("\n1. Logging into Hugging Face...")
try:
    login(token=HF_API_KEY)
    print("   ✓ Logged in")
except Exception as e:
    print(f"   ⚠ Login error (may already be logged in): {e}")

# Step 2: Create directories
print("\n2. Creating directories...")
directories = {
    "unet": f"{COMFYUI_ROOT}/models/unet",
    "clip": f"{COMFYUI_ROOT}/models/clip",
    "vae": f"{COMFYUI_ROOT}/models/vae",
}

for name, path in directories.items():
    os.makedirs(path, exist_ok=True)
    print(f"   ✓ {name}/ directory ready")

# Step 3: Download UNet
print("\n3. Downloading UNet (z_image_turbo_bf16.safetensors)...")
print("   This is ~11.46 GB - may take 10-20 minutes...")
try:
    unet_path = hf_hub_download(
        repo_id=REPO_ID,
        filename="z_image_turbo_bf16.safetensors",
        local_dir=f"{COMFYUI_ROOT}/models/unet",
        local_dir_use_symlinks=False
    )
    # Handle subdirectory case
    unet_file = f"{COMFYUI_ROOT}/models/unet/z_image_turbo_bf16.safetensors"
    if not os.path.exists(unet_file):
        for root, dirs, files in os.walk(f"{COMFYUI_ROOT}/models/unet"):
            for file in files:
                if file == "z_image_turbo_bf16.safetensors":
                    shutil.move(os.path.join(root, file), unet_file)
                    break
    if os.path.exists(unet_file):
        size_gb = os.path.getsize(unet_file) / (1024**3)
        print(f"   ✓ UNet downloaded: {size_gb:.2f} GB")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Step 4: Download CLIP
print("\n4. Downloading CLIP (qwen_3_4b.safetensors)...")
print("   This is ~7.49 GB - may take 5-10 minutes...")
try:
    clip_path = hf_hub_download(
        repo_id=REPO_ID,
        filename="split_files/text_encoders/qwen_3_4b.safetensors",
        local_dir=f"{COMFYUI_ROOT}/models/clip",
        local_dir_use_symlinks=False
    )
    # Move from subdirectory
    clip_file = f"{COMFYUI_ROOT}/models/clip/split_files/text_encoders/qwen_3_4b.safetensors"
    target_clip = f"{COMFYUI_ROOT}/models/clip/qwen_3_4b.safetensors"
    if os.path.exists(clip_file) and not os.path.exists(target_clip):
        shutil.move(clip_file, target_clip)
        try:
            os.removedirs(f"{COMFYUI_ROOT}/models/clip/split_files/text_encoders")
            os.removedirs(f"{COMFYUI_ROOT}/models/clip/split_files")
        except:
            pass
    if os.path.exists(target_clip):
        size_gb = os.path.getsize(target_clip) / (1024**3)
        print(f"   ✓ CLIP downloaded: {size_gb:.2f} GB")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Step 5: Download VAE
print("\n5. Downloading VAE (ae.safetensors)...")
print("   This is ~0.31 GB - should download quickly...")
try:
    vae_path = hf_hub_download(
        repo_id=REPO_ID,
        filename="split_files/vae/ae.safetensors",
        local_dir=f"{COMFYUI_ROOT}/models/vae",
        local_dir_use_symlinks=False
    )
    # Move from subdirectory
    vae_file = f"{COMFYUI_ROOT}/models/vae/split_files/vae/ae.safetensors"
    target_vae = f"{COMFYUI_ROOT}/models/vae/ae.safetensors"
    if os.path.exists(vae_file) and not os.path.exists(target_vae):
        shutil.move(vae_file, target_vae)
        try:
            os.removedirs(f"{COMFYUI_ROOT}/models/vae/split_files/vae")
            os.removedirs(f"{COMFYUI_ROOT}/models/vae/split_files")
        except:
            pass
    if os.path.exists(target_vae):
        size_gb = os.path.getsize(target_vae) / (1024**3)
        print(f"   ✓ VAE downloaded: {size_gb:.2f} GB")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Step 6: Verify
print("\n" + "=" * 60)
print("Verification")
print("=" * 60)

files_to_check = {
    "UNet": f"{COMFYUI_ROOT}/models/unet/z_image_turbo_bf16.safetensors",
    "CLIP": f"{COMFYUI_ROOT}/models/clip/qwen_3_4b.safetensors",
    "VAE": f"{COMFYUI_ROOT}/models/vae/ae.safetensors"
}

all_found = True
total_size = 0

for component, file_path in files_to_check.items():
    if os.path.exists(file_path):
        size_gb = os.path.getsize(file_path) / (1024**3)
        total_size += size_gb
        print(f"✓ {component}: {size_gb:.2f} GB")
    else:
        print(f"✗ {component}: NOT FOUND")
        all_found = False

print(f"\nTotal: {total_size:.2f} GB")

if all_found:
    print("\n🎉 Installation Complete!")
    print("\nNext steps:")
    print("1. Restart ComfyUI or wait 30-60 seconds")
    print("2. Load your workflow")
    print("3. Enjoy z_image_turbo!")
else:
    print("\n⚠ Some files are missing - check errors above")

print("=" * 60)
```

---

## Workflow Configuration

### Required Nodes

Your ComfyUI workflow needs these three loader nodes:

1. **UNETLoader** (Node 16):
   ```json
   {
     "inputs": {
       "unet_name": "z_image_turbo_bf16.safetensors",
       "weight_dtype": "default"
     },
     "class_type": "UNETLoader"
   }
   ```

2. **CLIPLoader** (Node 18):
   ```json
   {
     "inputs": {
       "clip_name": "qwen_3_4b.safetensors",
       "type": "qwen_image",
       "device": "default"
     },
     "class_type": "CLIPLoader"
   }
   ```

3. **VAELoader** (Node 17):
   ```json
   {
     "inputs": {
       "vae_name": "ae.safetensors"
     },
     "class_type": "VAELoader"
   }
   ```

### Important Notes

- **CLIP Type**: Must be `"qwen_image"` (not `"z_image"` or other types)
- **File Locations**: Files must be in the correct directories:
  - UNet: `models/unet/` (NOT `models/checkpoints/`)
  - CLIP: `models/clip/`
  - VAE: `models/vae/`

---

## Troubleshooting

### Files Not Detected by ComfyUI

**Problem**: ComfyUI doesn't show the files in dropdown menus.

**Solutions**:
1. **Restart ComfyUI completely** (not just refresh browser)
2. **Wait 30-60 seconds** for ComfyUI to rescan directories
3. **Check file permissions**: Files should be readable (644)
4. **Verify file locations**: Use the verification script above
5. **Hard refresh browser**: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)

### Wrong Directory Errors

**Problem**: Error says file not found or "not in list".

**Solutions**:
- **UNet**: Must be in `models/unet/`, NOT `models/checkpoints/`
- **CLIP**: Must be in `models/clip/` (or `models/text_encoders/` for some setups)
- **VAE**: Must be in `models/vae/`

### CLIP Type Error

**Problem**: Error says `type: 'z_image' not in [...]`

**Solution**: Change CLIP type to `"qwen_image"` in your workflow JSON.

### Download Errors

**Problem**: 404 errors or download failures.

**Solutions**:
1. **Check API key**: Ensure your Hugging Face token is valid
2. **Check repository**: Verify files exist at https://huggingface.co/Comfy-Org/z_image_turbo
3. **Retry download**: Network issues can cause temporary failures
4. **Manual download**: Download files directly from Hugging Face UI if needed

### File Size Mismatch

**Problem**: Downloaded file size doesn't match expected size.

**Solutions**:
1. **Re-download**: File may have been corrupted during download
2. **Check disk space**: Ensure you have enough free space
3. **Verify checksum**: Compare file sizes with repository

---

## Verification Checklist

After installation, verify:

- [ ] UNet file exists: `models/unet/z_image_turbo_bf16.safetensors` (~11.46 GB)
- [ ] CLIP file exists: `models/clip/qwen_3_4b.safetensors` (~7.49 GB)
- [ ] VAE file exists: `models/vae/ae.safetensors` (~0.31 GB)
- [ ] All files are readable (permissions 644)
- [ ] ComfyUI has been restarted or rescanned
- [ ] Workflow uses correct node types and file names
- [ ] CLIP type is set to `"qwen_image"`

---

## Quick Reference

### File Locations

```
ComfyUI/
├── models/
│   ├── unet/
│   │   └── z_image_turbo_bf16.safetensors  (11.46 GB)
│   ├── clip/
│   │   └── qwen_3_4b.safetensors          (7.49 GB)
│   └── vae/
│       └── ae.safetensors                  (0.31 GB)
```

### Workflow Node Configuration

- **UNETLoader**: `unet_name = "z_image_turbo_bf16.safetensors"`
- **CLIPLoader**: `clip_name = "qwen_3_4b.safetensors"`, `type = "qwen_image"`
- **VAELoader**: `vae_name = "ae.safetensors"`

### Download URLs

- **UNet**: `https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/z_image_turbo_bf16.safetensors`
- **CLIP**: `https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/text_encoders/qwen_3_4b.safetensors`
- **VAE**: `https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/vae/ae.safetensors`

---

## Additional Resources

- **Model Repository**: https://huggingface.co/Comfy-Org/z_image_turbo
- **ComfyUI Examples**: https://comfyanonymous.github.io/ComfyUI_examples/z_image/
- **Hugging Face API**: https://huggingface.co/settings/tokens

---

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify file locations match the expected structure
3. Check ComfyUI logs for specific error messages
4. Ensure all three components are installed (UNet, CLIP, VAE)
5. Verify workflow JSON uses correct node types and file names

---

**Last Updated**: Based on z_image_turbo installation experience
**ComfyUI Version**: Compatible with ComfyUI Manager v3.37.2+
**Model Format**: Split model (UNet + CLIP + VAE)

