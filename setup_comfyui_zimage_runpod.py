#!/usr/bin/env python3
"""
Complete ComfyUI z_image_turbo Setup Script for RunPod
Run this in your RunPod JupyterLab notebook or terminal

This script:
1. Finds ComfyUI installation
2. Downloads all z_image_turbo components
3. Verifies installation
4. Provides next steps
"""

import os
import shutil
from huggingface_hub import hf_hub_download, login

# ============================================================================
# CONFIGURATION - EDIT THESE VALUES
# ============================================================================
HF_API_KEY = os.getenv("HF_API_KEY", "YOUR_HF_API_KEY_HERE")  # Get from https://huggingface.co/settings/tokens
REPO_ID = "Comfy-Org/z_image_turbo"

# Find ComfyUI location (adjust if needed)
COMFYUI_PATHS = [
    "/workspace/ComfyUI",
    "/workspace/runpod-slim/ComfyUI",
    "/ComfyUI",
    "/workspace/comfyui",
    "/comfyui"
]

COMFYUI_ROOT = None
for path in COMFYUI_PATHS:
    if os.path.exists(path):
        COMFYUI_ROOT = path
        break

if not COMFYUI_ROOT:
    print("⚠️  ComfyUI not found in common locations!")
    print("Please set COMFYUI_ROOT manually in the script")
    COMFYUI_ROOT = "/workspace/ComfyUI"  # Default fallback

print("=" * 70)
print("ComfyUI z_image_turbo Installation Script")
print("=" * 70)
print(f"\nComfyUI Location: {COMFYUI_ROOT}")

# Verify ComfyUI exists
if not os.path.exists(COMFYUI_ROOT):
    print(f"\n⚠️  Warning: ComfyUI not found at {COMFYUI_ROOT}")
    print("Please verify the path or install ComfyUI first")
    print("\nCommon RunPod ComfyUI templates:")
    print("  - Qwen Template: https://get.runpod.io/qwen-template")
    print("  - Standard ComfyUI template from RunPod Hub")
    exit(1)

# ============================================================================
# INSTALLATION
# ============================================================================

# Step 1: Login
print("\n1. Logging into Hugging Face...")
try:
    login(token=HF_API_KEY)
    print("   ✓ Logged in")
except Exception as e:
    print(f"   ⚠ Login error (may already be logged in): {e}")
    print("   Continuing anyway...")

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

# Step 3: Download UNet (Main Model)
print("\n3. Downloading UNet (z_image_turbo_bf16.safetensors)...")
print("   This is ~11.46 GB - may take 10-20 minutes...")
print("   Please be patient...")

unet_success = False
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
        unet_success = True
    else:
        print(f"   ✗ UNet file not found after download")
except Exception as e:
    print(f"   ✗ Error downloading UNet: {e}")

# Step 4: Download CLIP (Text Encoder)
print("\n4. Downloading CLIP (qwen_3_4b.safetensors)...")
print("   This is ~7.49 GB - may take 5-10 minutes...")
print("   Please be patient...")

clip_success = False
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
        clip_success = True
    else:
        print(f"   ✗ CLIP file not found after download")
except Exception as e:
    print(f"   ✗ Error downloading CLIP: {e}")

# Step 5: Download VAE
print("\n5. Downloading VAE (ae.safetensors)...")
print("   This is ~0.31 GB - should download quickly...")

vae_success = False
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
        vae_success = True
    else:
        print(f"   ✗ VAE file not found after download")
except Exception as e:
    print(f"   ✗ Error downloading VAE: {e}")

# Step 6: Verify
print("\n" + "=" * 70)
print("Verification")
print("=" * 70)

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

print(f"\nTotal: {total_size:.2f} GB")

# Final summary
print("\n" + "=" * 70)
if all_found:
    print("🎉 Installation Complete!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Restart ComfyUI or wait 30-60 seconds for rescan")
    print("2. Access ComfyUI via RunPod proxy URL (usually port 8188)")
    print("3. Load your workflow (z-image-workflow.json)")
    print("4. The model should be available in ComfyUI")
    print("\nFile locations:")
    print(f"  UNet: {COMFYUI_ROOT}/models/unet/")
    print(f"  CLIP: {COMFYUI_ROOT}/models/clip/")
    print(f"  VAE: {COMFYUI_ROOT}/models/vae/")
else:
    print("⚠ Installation Incomplete")
    print("=" * 70)
    print("\nSome files are missing. Check the errors above.")
    print("\nTroubleshooting:")
    print("1. Verify HF_API_KEY is set correctly")
    print("2. Check internet connection")
    print("3. Verify disk space: df -h /workspace")
    print("4. Try downloading files manually from:")
    print("   https://huggingface.co/Comfy-Org/z_image_turbo")

print("=" * 70)

