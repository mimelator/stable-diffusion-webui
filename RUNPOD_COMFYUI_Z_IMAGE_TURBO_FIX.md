# RunPod ComfyUI - z_image_turbo Fix (Finding Correct Files)

## Issue

The main model downloaded successfully, but CLIP and VAE files returned 404 errors. This means those files don't exist at those exact paths. We need to find the correct file paths.

## Solution: List and Download Correct Files

Run this script in your notebook to find and download the correct files:

```python
# Install dependencies
!pip install huggingface_hub -q

import os
from huggingface_hub import list_repo_files, hf_hub_download, login

# Configuration
HF_API_KEY = os.getenv("HF_API_KEY", "YOUR_HF_API_KEY_HERE")
REPO_ID = "Comfy-Org/z_image_turbo"
COMFYUI_ROOT = "/workspace/ComfyUI"

# Login
login(token=HF_API_KEY)

# List ALL files in the repository
print("=" * 60)
print("Listing all files in repository...")
print("=" * 60)
all_files = list_repo_files(repo_id=REPO_ID, repo_type="model")

# Filter and display relevant files
print("\n📁 Available files:")
print("-" * 60)

clip_files = [f for f in all_files if 'clip' in f.lower()]
vae_files = [f for f in all_files if 'vae' in f.lower()]
model_files = [f for f in all_files if 'diffusion' in f.lower() or 'model' in f.lower()]

print("\n🔹 Model files:")
for f in model_files:
    print(f"  - {f}")

print("\n🔹 CLIP files:")
for f in clip_files:
    print(f"  - {f}")

print("\n🔹 VAE files:")
for f in vae_files:
    print(f"  - {f}")

# Create directories
for d in ["checkpoints", "clip", "vae"]:
    os.makedirs(f"{COMFYUI_ROOT}/models/{d}", exist_ok=True)

# Download correct files
print("\n" + "=" * 60)
print("Downloading files...")
print("=" * 60)

# Download CLIP files (if any found)
if clip_files:
    print("\n📥 Downloading CLIP files...")
    for clip_file in clip_files:
        try:
            print(f"  Downloading: {clip_file}")
            hf_hub_download(
                repo_id=REPO_ID,
                filename=clip_file,
                local_dir=f"{COMFYUI_ROOT}/models/clip"
            )
            print(f"  ✓ Downloaded: {os.path.basename(clip_file)}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
else:
    print("\n⚠ No CLIP files found in repository")
    print("  Note: z_image_turbo may use different text encoders")
    print("  Check ComfyUI documentation for required CLIP models")

# Download VAE files (if any found)
if vae_files:
    print("\n📥 Downloading VAE files...")
    for vae_file in vae_files:
        try:
            print(f"  Downloading: {vae_file}")
            hf_hub_download(
                repo_id=REPO_ID,
                filename=vae_file,
                local_dir=f"{COMFYUI_ROOT}/models/vae"
            )
            print(f"  ✓ Downloaded: {os.path.basename(vae_file)}")
        except Exception as e:
            print(f"  ✗ Error: {e}")
else:
    print("\n⚠ No VAE files found in repository")
    print("  Note: z_image_turbo may use standard VAE or include it in the model")
    print("  Check if VAE is included in the model file or use default VAE")

print("\n" + "=" * 60)
print("Download complete!")
print("=" * 60)

# Verify what was downloaded
print("\n📋 Installed files:")
print("-" * 60)

print("\nCheckpoints:")
for f in os.listdir(f"{COMFYUI_ROOT}/models/checkpoints"):
    if "z_image_turbo" in f.lower():
        size_gb = os.path.getsize(f"{COMFYUI_ROOT}/models/checkpoints/{f}") / (1024**3)
        print(f"  ✓ {f} ({size_gb:.2f} GB)")

print("\nCLIP:")
if os.path.exists(f"{COMFYUI_ROOT}/models/clip"):
    clip_files_downloaded = os.listdir(f"{COMFYUI_ROOT}/models/clip")
    if clip_files_downloaded:
        for f in clip_files_downloaded:
            size_mb = os.path.getsize(f"{COMFYUI_ROOT}/models/clip/{f}") / (1024**2)
            print(f"  ✓ {f} ({size_mb:.2f} MB)")
    else:
        print("  (no files)")

print("\nVAE:")
if os.path.exists(f"{COMFYUI_ROOT}/models/vae"):
    vae_files_downloaded = os.listdir(f"{COMFYUI_ROOT}/models/vae")
    if vae_files_downloaded:
        for f in vae_files_downloaded:
            size_mb = os.path.getsize(f"{COMFYUI_ROOT}/models/vae/{f}") / (1024**2)
            print(f"  ✓ {f} ({size_mb:.2f} MB)")
    else:
        print("  (no files)")

print("\n" + "=" * 60)
print("Next steps:")
print("1. Check the file list above to see what was downloaded")
print("2. z_image_turbo may use standard CLIP/VAE from ComfyUI")
print("3. Restart ComfyUI and test the model")
print("=" * 60)
```

---

## Alternative: Check Repository Structure

If the above doesn't work, check the repository structure directly:

```python
from huggingface_hub import list_repo_files, login

login(token=os.getenv("HF_API_KEY", "YOUR_HF_API_KEY_HERE"))

# List all files
files = list_repo_files(repo_id="Comfy-Org/z_image_turbo", repo_type="model")

# Print all files (to see structure)
for f in sorted(files):
    print(f)
```

---

## Important Notes

### z_image_turbo May Use Standard Components

**z_image_turbo** might:
1. **Use standard CLIP models** that come with ComfyUI
2. **Include VAE in the model file** (some models do this)
3. **Use different file structure** than expected

### Check ComfyUI Requirements

1. **Check ComfyUI documentation** for z_image_turbo requirements
2. **Check the model's Hugging Face page** for usage instructions
3. **Try loading the model** - ComfyUI may auto-detect what's needed

### Standard CLIP Models

If CLIP files aren't in the repository, z_image_turbo likely uses:
- **T5-XXL** encoder (standard, may already be in ComfyUI)
- **CLIP-L** encoder (standard, may already be in ComfyUI)

These are usually downloaded automatically by ComfyUI when needed.

### Standard VAE

If VAE files aren't in the repository:
- The model may use ComfyUI's default VAE
- Or the VAE may be included in the model file
- Or you may need to download a standard VAE separately

---

## Quick Fix: Try Loading the Model

After downloading the main model, try loading it in ComfyUI:

1. **Restart ComfyUI**
2. **Load the model** in your workflow
3. **Check for errors** - ComfyUI will tell you what's missing
4. **Download missing components** based on error messages

ComfyUI is usually good at telling you exactly what files are needed!

---

## Verify Model Installation

```python
import os

COMFYUI_ROOT = "/workspace/ComfyUI"

# Check if model file exists
model_path = f"{COMFYUI_ROOT}/models/checkpoints/split_files/diffusion_models/z_image_turbo_bf16.safetensors"

if os.path.exists(model_path):
    size_gb = os.path.getsize(model_path) / (1024**3)
    print(f"✓ Model found: {size_gb:.2f} GB")
    
    # Move to correct location (if needed)
    # The file is in a subdirectory, might need to move it
    correct_path = f"{COMFYUI_ROOT}/models/checkpoints/z_image_turbo_bf16.safetensors"
    if not os.path.exists(correct_path):
        print(f"\nMoving model to correct location...")
        os.makedirs(os.path.dirname(correct_path), exist_ok=True)
        os.rename(model_path, correct_path)
        print(f"✓ Moved to: {correct_path}")
else:
    print("✗ Model not found")
```

---

## Fix: Move Model to Correct Location

The model downloaded to a subdirectory. Move it to the correct location:

```python
import os
import shutil

COMFYUI_ROOT = "/workspace/ComfyUI"

# Current location (with subdirectory)
current_path = f"{COMFYUI_ROOT}/models/checkpoints/split_files/diffusion_models/z_image_turbo_bf16.safetensors"

# Correct location
correct_path = f"{COMFYUI_ROOT}/models/checkpoints/z_image_turbo_bf16.safetensors"

if os.path.exists(current_path):
    print(f"Moving model from subdirectory to correct location...")
    os.makedirs(os.path.dirname(correct_path), exist_ok=True)
    
    if os.path.exists(correct_path):
        print("Model already exists at correct location")
    else:
        shutil.move(current_path, correct_path)
        print(f"✓ Moved to: {correct_path}")
        
        # Clean up empty directories
        try:
            os.removedirs(f"{COMFYUI_ROOT}/models/checkpoints/split_files/diffusion_models")
            os.removedirs(f"{COMFYUI_ROOT}/models/checkpoints/split_files")
        except:
            pass
else:
    print("Model file not found at expected location")
```

---

## Complete Fixed Script

Here's the complete script that handles everything:

```python
# Install dependencies
!pip install huggingface_hub -q

import os
import shutil
from huggingface_hub import list_repo_files, hf_hub_download, login

# Configuration
HF_API_KEY = os.getenv("HF_API_KEY", "YOUR_HF_API_KEY_HERE")
REPO_ID = "Comfy-Org/z_image_turbo"
COMFYUI_ROOT = "/workspace/ComfyUI"

# Login
login(token=HF_API_KEY)

# Create directories
for d in ["checkpoints", "clip", "vae"]:
    os.makedirs(f"{COMFYUI_ROOT}/models/{d}", exist_ok=True)

# List all files to find correct paths
print("=" * 60)
print("Finding available files...")
print("=" * 60)
all_files = list_repo_files(repo_id=REPO_ID, repo_type="model")

# Find relevant files
clip_files = [f for f in all_files if 'clip' in f.lower()]
vae_files = [f for f in all_files if 'vae' in f.lower()]

print(f"\nFound {len(all_files)} total files")
print(f"  CLIP files: {len(clip_files)}")
print(f"  VAE files: {len(vae_files)}")

# Download CLIP files if they exist
if clip_files:
    print("\n📥 Downloading CLIP files...")
    for clip_file in clip_files:
        try:
            hf_hub_download(REPO_ID, clip_file, local_dir=f"{COMFYUI_ROOT}/models/clip")
            print(f"  ✓ {os.path.basename(clip_file)}")
        except Exception as e:
            print(f"  ✗ Error: {e}")

# Download VAE files if they exist
if vae_files:
    print("\n📥 Downloading VAE files...")
    for vae_file in vae_files:
        try:
            hf_hub_download(REPO_ID, vae_file, local_dir=f"{COMFYUI_ROOT}/models/vae")
            print(f"  ✓ {os.path.basename(vae_file)}")
        except Exception as e:
            print(f"  ✗ Error: {e}")

# Fix model location (move from subdirectory)
print("\n📁 Fixing model location...")
model_subdir = f"{COMFYUI_ROOT}/models/checkpoints/split_files/diffusion_models/z_image_turbo_bf16.safetensors"
model_correct = f"{COMFYUI_ROOT}/models/checkpoints/z_image_turbo_bf16.safetensors"

if os.path.exists(model_subdir) and not os.path.exists(model_correct):
    shutil.move(model_subdir, model_correct)
    print(f"  ✓ Moved model to correct location")
    
    # Clean up empty directories
    try:
        os.removedirs(os.path.dirname(model_subdir))
        os.removedirs(os.path.dirname(os.path.dirname(model_subdir)))
    except:
        pass
elif os.path.exists(model_correct):
    print(f"  ✓ Model already at correct location")

print("\n" + "=" * 60)
print("Installation complete!")
print("=" * 60)
print(f"\nModel: {COMFYUI_ROOT}/models/checkpoints/z_image_turbo_bf16.safetensors")
print("\nNote: If CLIP/VAE files weren't found, z_image_turbo may use:")
print("  - Standard CLIP models (auto-downloaded by ComfyUI)")
print("  - Default VAE (or included in model)")
print("\nTry loading the model in ComfyUI - it will tell you what's needed!")
```

---

## Summary

1. **Model downloaded successfully** ✓ (12.3 GB)
2. **CLIP/VAE files don't exist** at those paths
3. **Solution**: Run the script above to:
   - List all available files
   - Download correct CLIP/VAE files (if they exist)
   - Move model to correct location
   - Handle missing files gracefully

**Most likely**: z_image_turbo uses standard CLIP/VAE that ComfyUI will download automatically when you load the model.

