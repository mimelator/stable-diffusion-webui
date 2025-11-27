# RunPod ComfyUI - z_image_turbo Installation Guide

## Overview

This guide helps you download and install the z_image_turbo model components (safetensors, text encoders, VAE) to your ComfyUI installation on RunPod.

**Model Repository**: https://huggingface.co/Comfy-Org/z_image_turbo

---

## Quick Installation Script

### Python Notebook Script

Run this in your RunPod Python notebook:

```python
import os
import requests
from pathlib import Path
from huggingface_hub import hf_hub_download, snapshot_download
from huggingface_hub import login

# Your Hugging Face API key
HF_API_KEY = os.getenv("HF_API_KEY", "YOUR_HF_API_KEY_HERE")

# Login to Hugging Face
login(token=HF_API_KEY)

# ComfyUI directories (adjust paths if needed)
# Typical RunPod ComfyUI structure:
COMFYUI_ROOT = "/workspace/ComfyUI"  # Adjust if different
MODELS_DIR = f"{COMFYUI_ROOT}/models"
CHECKPOINTS_DIR = f"{MODELS_DIR}/checkpoints"
CLIP_DIR = f"{MODELS_DIR}/clip"
VAE_DIR = f"{MODELS_DIR}/vae"

# Create directories if they don't exist
os.makedirs(CHECKPOINTS_DIR, exist_ok=True)
os.makedirs(CLIP_DIR, exist_ok=True)
os.makedirs(VAE_DIR, exist_ok=True)

# Model repository
REPO_ID = "Comfy-Org/z_image_turbo"

print("=" * 60)
print("Downloading z_image_turbo model components...")
print("=" * 60)

# Download main safetensors file
print("\n1. Downloading main model (safetensors)...")
try:
    model_file = hf_hub_download(
        repo_id=REPO_ID,
        filename="split_files/diffusion_models/z_image_turbo_bf16.safetensors",
        local_dir=CHECKPOINTS_DIR,
        local_dir_use_symlinks=False
    )
    print(f"✓ Downloaded: {model_file}")
except Exception as e:
    print(f"✗ Error downloading model: {e}")

# Download text encoder (CLIP)
print("\n2. Downloading text encoder (CLIP)...")
try:
    # Check what CLIP files are available
    clip_files = [
        "split_files/clip/t5xxl_fp16.safetensors",
        "split_files/clip/clip_l.safetensors",
        # Add other CLIP files if they exist
    ]
    
    for clip_file in clip_files:
        try:
            clip_path = hf_hub_download(
                repo_id=REPO_ID,
                filename=clip_file,
                local_dir=CLIP_DIR,
                local_dir_use_symlinks=False
            )
            print(f"✓ Downloaded: {clip_path}")
        except Exception as e:
            print(f"⚠ Could not download {clip_file}: {e}")
except Exception as e:
    print(f"✗ Error downloading CLIP: {e}")

# Download VAE
print("\n3. Downloading VAE...")
try:
    vae_files = [
        "split_files/vae/vae_fp16.safetensors",
        "split_files/vae/vae.safetensors",
        # Add other VAE files if they exist
    ]
    
    for vae_file in vae_files:
        try:
            vae_path = hf_hub_download(
                repo_id=REPO_ID,
                filename=vae_file,
                local_dir=VAE_DIR,
                local_dir_use_symlinks=False
            )
            print(f"✓ Downloaded: {vae_path}")
            break  # Only need one VAE file
        except Exception as e:
            print(f"⚠ Could not download {vae_file}: {e}")
except Exception as e:
    print(f"✗ Error downloading VAE: {e}")

print("\n" + "=" * 60)
print("Download complete!")
print("=" * 60)
print(f"\nFiles installed to:")
print(f"  Checkpoints: {CHECKPOINTS_DIR}")
print(f"  CLIP: {CLIP_DIR}")
print(f"  VAE: {VAE_DIR}")
print("\nRestart ComfyUI to load the new model.")
```

---

## Alternative: Download All Files at Once

If you want to download everything from the repository:

```python
import os
from huggingface_hub import snapshot_download, login

# Login
HF_API_KEY = os.getenv("HF_API_KEY", "YOUR_HF_API_KEY_HERE")
login(token=HF_API_KEY)

# ComfyUI root (adjust if needed)
COMFYUI_ROOT = "/workspace/ComfyUI"
MODELS_DIR = f"{COMFYUI_ROOT}/models"

# Download entire repository
print("Downloading z_image_turbo repository...")
try:
    snapshot_download(
        repo_id="Comfy-Org/z_image_turbo",
        local_dir=f"{MODELS_DIR}/z_image_turbo",
        local_dir_use_symlinks=False
    )
    print("✓ Download complete!")
    
    # Now move files to correct locations
    import shutil
    
    source_dir = f"{MODELS_DIR}/z_image_turbo/split_files"
    
    # Move model
    if os.path.exists(f"{source_dir}/diffusion_models/z_image_turbo_bf16.safetensors"):
        shutil.move(
            f"{source_dir}/diffusion_models/z_image_turbo_bf16.safetensors",
            f"{MODELS_DIR}/checkpoints/z_image_turbo_bf16.safetensors"
        )
        print("✓ Moved model to checkpoints")
    
    # Move CLIP files
    clip_source = f"{source_dir}/clip"
    if os.path.exists(clip_source):
        for file in os.listdir(clip_source):
            shutil.move(
                f"{clip_source}/{file}",
                f"{MODELS_DIR}/clip/{file}"
            )
        print("✓ Moved CLIP files")
    
    # Move VAE files
    vae_source = f"{source_dir}/vae"
    if os.path.exists(vae_source):
        for file in os.listdir(vae_source):
            shutil.move(
                f"{vae_source}/{file}",
                f"{MODELS_DIR}/vae/{file}"
            )
        print("✓ Moved VAE files")
    
    # Clean up
    shutil.rmtree(f"{MODELS_DIR}/z_image_turbo")
    print("✓ Cleanup complete")
    
except Exception as e:
    print(f"✗ Error: {e}")
```

---

## Step-by-Step Manual Installation

### Step 1: Install Required Libraries

```python
# Install huggingface_hub if not already installed
!pip install huggingface_hub
```

### Step 2: Set Up Authentication

```python
from huggingface_hub import login

HF_API_KEY = os.getenv("HF_API_KEY", "YOUR_HF_API_KEY_HERE")
login(token=HF_API_KEY)
```

### Step 3: Find ComfyUI Directories

```python
# Check ComfyUI structure
import os

# Common RunPod ComfyUI locations
possible_paths = [
    "/workspace/ComfyUI",
    "/workspace/comfyui",
    "/ComfyUI",
    "/comfyui"
]

for path in possible_paths:
    if os.path.exists(path):
        print(f"Found ComfyUI at: {path}")
        print(f"  Models: {path}/models")
        print(f"  Checkpoints: {path}/models/checkpoints")
        print(f"  CLIP: {path}/models/clip")
        print(f"  VAE: {path}/models/vae")
        break
else:
    print("ComfyUI not found in common locations.")
    print("Please check your RunPod setup and adjust paths.")
```

### Step 4: Download Files

```python
from huggingface_hub import hf_hub_download

REPO_ID = "Comfy-Org/z_image_turbo"
COMFYUI_ROOT = "/workspace/ComfyUI"  # Adjust if needed

# Download main model
model_file = hf_hub_download(
    repo_id=REPO_ID,
    filename="split_files/diffusion_models/z_image_turbo_bf16.safetensors",
    local_dir=f"{COMFYUI_ROOT}/models/checkpoints"
)

# Download CLIP files
clip_files = [
    "split_files/clip/t5xxl_fp16.safetensors",
    "split_files/clip/clip_l.safetensors"
]

for clip_file in clip_files:
    try:
        hf_hub_download(
            repo_id=REPO_ID,
            filename=clip_file,
            local_dir=f"{COMFYUI_ROOT}/models/clip"
        )
    except:
        print(f"Could not download {clip_file}")

# Download VAE
vae_file = hf_hub_download(
    repo_id=REPO_ID,
    filename="split_files/vae/vae_fp16.safetensors",
    local_dir=f"{COMFYUI_ROOT}/models/vae"
)
```

---

## Using wget/curl (Alternative Method)

If you prefer using wget or curl:

```bash
# Set your API key
export HF_TOKEN="YOUR_HF_API_KEY_HERE"

# Create directories
mkdir -p /workspace/ComfyUI/models/{checkpoints,clip,vae}

# Download main model
wget --header="Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/diffusion_models/z_image_turbo_bf16.safetensors" \
  -O /workspace/ComfyUI/models/checkpoints/z_image_turbo_bf16.safetensors

# Download CLIP files
wget --header="Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/clip/t5xxl_fp16.safetensors" \
  -O /workspace/ComfyUI/models/clip/t5xxl_fp16.safetensors

wget --header="Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/clip/clip_l.safetensors" \
  -O /workspace/ComfyUI/models/clip/clip_l.safetensors

# Download VAE
wget --header="Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/vae/vae_fp16.safetensors" \
  -O /workspace/ComfyUI/models/vae/vae_fp16.safetensors
```

---

## Verify Installation

After downloading, verify files are in place:

```python
import os

COMFYUI_ROOT = "/workspace/ComfyUI"  # Adjust if needed

print("Checking installed files...")
print("\nCheckpoints:")
checkpoints = os.listdir(f"{COMFYUI_ROOT}/models/checkpoints")
for f in checkpoints:
    if "z_image_turbo" in f.lower():
        size = os.path.getsize(f"{COMFYUI_ROOT}/models/checkpoints/{f}") / (1024**3)
        print(f"  ✓ {f} ({size:.2f} GB)")

print("\nCLIP:")
clip_files = os.listdir(f"{COMFYUI_ROOT}/models/clip")
for f in clip_files:
    if any(x in f.lower() for x in ["t5", "clip"]):
        size = os.path.getsize(f"{COMFYUI_ROOT}/models/clip/{f}") / (1024**2)
        print(f"  ✓ {f} ({size:.2f} MB)")

print("\nVAE:")
vae_files = os.listdir(f"{COMFYUI_ROOT}/models/vae")
for f in vae_files:
    if "vae" in f.lower():
        size = os.path.getsize(f"{COMFYUI_ROOT}/models/vae/{f}") / (1024**2)
        print(f"  ✓ {f} ({size:.2f} MB)")
```

---

## ComfyUI Directory Structure

After installation, your ComfyUI should have:

```
/workspace/ComfyUI/
├── models/
│   ├── checkpoints/
│   │   └── z_image_turbo_bf16.safetensors  ← Main model
│   ├── clip/
│   │   ├── t5xxl_fp16.safetensors          ← Text encoder
│   │   └── clip_l.safetensors              ← CLIP encoder
│   └── vae/
│       └── vae_fp16.safetensors             ← VAE
```

---

## Using the Model in ComfyUI

After installation:

1. **Restart ComfyUI** (if running)
2. **Load the model** in your workflow:
   - Use "CheckpointLoaderSimple" node
   - Select "z_image_turbo_bf16.safetensors"
3. **Set up text encoders**:
   - Use "CLIPTextEncode" nodes
   - ComfyUI should auto-detect the CLIP files
4. **Set VAE** (if needed):
   - Use "VAELoader" node
   - Select "vae_fp16.safetensors"

---

## Troubleshooting

### Issue: Files not downloading

**Solution**:
```python
# Check authentication
from huggingface_hub import whoami
print(whoami())

# Should show your username
```

### Issue: Wrong directory paths

**Solution**:
```python
# Find ComfyUI location
import subprocess
result = subprocess.run(['find', '/workspace', '-name', 'ComfyUI', '-type', 'd'], 
                       capture_output=True, text=True)
print(result.stdout)
```

### Issue: Out of disk space

**Solution**:
```python
# Check disk space
import shutil
total, used, free = shutil.disk_usage("/workspace")
print(f"Total: {total // (1024**3)} GB")
print(f"Used: {used // (1024**3)} GB")
print(f"Free: {free // (1024**3)} GB")
```

### Issue: Model not appearing in ComfyUI

**Solutions**:
1. Check file permissions: `chmod 644 /workspace/ComfyUI/models/checkpoints/*`
2. Restart ComfyUI
3. Check ComfyUI logs for errors
4. Verify file names match exactly

---

## Complete Installation Script (All-in-One)

```python
#!/usr/bin/env python3
"""
Complete z_image_turbo installation script for RunPod ComfyUI
"""

import os
import sys
from pathlib import Path
from huggingface_hub import hf_hub_download, login, list_repo_files

# Configuration
HF_API_KEY = os.getenv("HF_API_KEY", "YOUR_HF_API_KEY_HERE")
REPO_ID = "Comfy-Org/z_image_turbo"

# Find ComfyUI (common RunPod locations)
COMFYUI_PATHS = [
    "/workspace/ComfyUI",
    "/workspace/comfyui",
    "/ComfyUI",
    "/comfyui"
]

COMFYUI_ROOT = None
for path in COMFYUI_PATHS:
    if os.path.exists(path):
        COMFYUI_ROOT = path
        break

if not COMFYUI_ROOT:
    print("Error: ComfyUI not found!")
    print("Please set COMFYUI_ROOT manually")
    sys.exit(1)

print(f"Found ComfyUI at: {COMFYUI_ROOT}")

# Set up directories
MODELS_DIR = f"{COMFYUI_ROOT}/models"
CHECKPOINTS_DIR = f"{MODELS_DIR}/checkpoints"
CLIP_DIR = f"{MODELS_DIR}/clip"
VAE_DIR = f"{MODELS_DIR}/vae"

for dir_path in [CHECKPOINTS_DIR, CLIP_DIR, VAE_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# Login to Hugging Face
print("\nLogging in to Hugging Face...")
login(token=HF_API_KEY)

# List available files
print("\nChecking available files in repository...")
try:
    files = list_repo_files(repo_id=REPO_ID, repo_type="model")
    print(f"Found {len(files)} files")
except Exception as e:
    print(f"Warning: Could not list files: {e}")
    files = []

# Files to download
files_to_download = {
    "checkpoints": [
        "split_files/diffusion_models/z_image_turbo_bf16.safetensors"
    ],
    "clip": [
        "split_files/clip/t5xxl_fp16.safetensors",
        "split_files/clip/clip_l.safetensors"
    ],
    "vae": [
        "split_files/vae/vae_fp16.safetensors",
        "split_files/vae/vae.safetensors"
    ]
}

# Download files
print("\n" + "=" * 60)
print("Downloading files...")
print("=" * 60)

for category, file_list in files_to_download.items():
    print(f"\n{category.upper()}:")
    target_dir = {
        "checkpoints": CHECKPOINTS_DIR,
        "clip": CLIP_DIR,
        "vae": VAE_DIR
    }[category]
    
    for filename in file_list:
        try:
            print(f"  Downloading {filename}...")
            downloaded = hf_hub_download(
                repo_id=REPO_ID,
                filename=filename,
                local_dir=target_dir,
                local_dir_use_symlinks=False
            )
            size_mb = os.path.getsize(downloaded) / (1024**2)
            print(f"  ✓ Downloaded: {os.path.basename(downloaded)} ({size_mb:.2f} MB)")
        except Exception as e:
            print(f"  ✗ Error downloading {filename}: {e}")

print("\n" + "=" * 60)
print("Installation complete!")
print("=" * 60)
print(f"\nFiles installed to:")
print(f"  Checkpoints: {CHECKPOINTS_DIR}")
print(f"  CLIP: {CLIP_DIR}")
print(f"  VAE: {VAE_DIR}")
print("\nNext steps:")
print("1. Restart ComfyUI")
print("2. Load 'z_image_turbo_bf16.safetensors' in your workflow")
```

---

## Quick Copy-Paste for Notebook

Copy this entire block into your RunPod notebook:

```python
# Install dependencies
!pip install huggingface_hub -q

# Import and setup
import os
from huggingface_hub import hf_hub_download, login

# Configuration
HF_API_KEY = os.getenv("HF_API_KEY", "YOUR_HF_API_KEY_HERE")
REPO_ID = "Comfy-Org/z_image_turbo"
COMFYUI_ROOT = "/workspace/ComfyUI"  # Adjust if needed

# Create directories
for d in ["checkpoints", "clip", "vae"]:
    os.makedirs(f"{COMFYUI_ROOT}/models/{d}", exist_ok=True)

# Login
login(token=HF_API_KEY)

# Download files
print("Downloading z_image_turbo...")
hf_hub_download(REPO_ID, "split_files/diffusion_models/z_image_turbo_bf16.safetensors", 
                local_dir=f"{COMFYUI_ROOT}/models/checkpoints")
hf_hub_download(REPO_ID, "split_files/clip/t5xxl_fp16.safetensors", 
                local_dir=f"{COMFYUI_ROOT}/models/clip")
hf_hub_download(REPO_ID, "split_files/clip/clip_l.safetensors", 
                local_dir=f"{COMFYUI_ROOT}/models/clip")
hf_hub_download(REPO_ID, "split_files/vae/vae_fp16.safetensors", 
                local_dir=f"{COMFYUI_ROOT}/models/vae")

print("✓ Installation complete! Restart ComfyUI.")
```

---

## Summary

**Easiest Method**: Use the "Quick Copy-Paste for Notebook" section above - just paste it into your RunPod notebook and run it.

**Files Installed**:
- ✅ Model: `z_image_turbo_bf16.safetensors` → `models/checkpoints/`
- ✅ CLIP: `t5xxl_fp16.safetensors`, `clip_l.safetensors` → `models/clip/`
- ✅ VAE: `vae_fp16.safetensors` → `models/vae/`

**After Installation**: Restart ComfyUI and the model will be available in your workflows!

