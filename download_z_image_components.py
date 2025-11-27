#!/usr/bin/env python3
"""
Download z_image_turbo CLIP and VAE files
Run this in your RunPod notebook
"""

import os
from huggingface_hub import hf_hub_download, login

# Configuration
HF_API_KEY = os.getenv("HF_API_KEY", "YOUR_HF_API_KEY_HERE")
REPO_ID = "Comfy-Org/z_image_turbo"
COMFYUI_ROOT = "/workspace/runpod-slim/ComfyUI"

# Login
print("=" * 60)
print("Downloading z_image_turbo Components")
print("=" * 60)

try:
    login(token=HF_API_KEY)
    print("✓ Logged into Hugging Face")
except Exception as e:
    print(f"⚠ Login error (may already be logged in): {e}")

# Create directories
print("\nCreating directories...")
os.makedirs(f"{COMFYUI_ROOT}/models/clip", exist_ok=True)
os.makedirs(f"{COMFYUI_ROOT}/models/vae", exist_ok=True)
print("✓ Directories ready")

# Files to download
files_to_download = {
    "CLIP": {
        "repo_path": "split_files/text_encoders/qwen_3_4b.safetensors",
        "local_path": f"{COMFYUI_ROOT}/models/clip/qwen_3_4b.safetensors"
    },
    "VAE": {
        "repo_path": "split_files/vae/ae.safetensors",
        "local_path": f"{COMFYUI_ROOT}/models/vae/ae.safetensors"
    }
}

print("\n" + "=" * 60)
print("Downloading files...")
print("=" * 60)

for component_name, file_info in files_to_download.items():
    repo_path = file_info["repo_path"]
    local_path = file_info["local_path"]
    
    # Check if already exists
    if os.path.exists(local_path):
        size_gb = os.path.getsize(local_path) / (1024**3)
        print(f"\n✓ {component_name} already exists: {size_gb:.2f} GB")
        print(f"  {local_path}")
        continue
    
    print(f"\n📥 Downloading {component_name}...")
    print(f"  From: {REPO_ID}/{repo_path}")
    print(f"  To:   {local_path}")
    
    try:
        downloaded_path = hf_hub_download(
            repo_id=REPO_ID,
            filename=repo_path,
            local_dir=os.path.dirname(local_path),
            local_dir_use_symlinks=False
        )
        
        # Move to correct filename if needed
        if downloaded_path != local_path:
            import shutil
            if os.path.exists(local_path):
                os.remove(local_path)
            shutil.move(downloaded_path, local_path)
        
        if os.path.exists(local_path):
            size_gb = os.path.getsize(local_path) / (1024**3)
            print(f"  ✓ Downloaded successfully: {size_gb:.2f} GB")
        else:
            print(f"  ✗ File not found after download")
            
    except Exception as e:
        print(f"  ✗ Error downloading {component_name}: {e}")
        print(f"  Try manual download from:")
        print(f"  https://huggingface.co/{REPO_ID}/resolve/main/{repo_path}")

# Verify all files
print("\n" + "=" * 60)
print("Verification")
print("=" * 60)

all_files = {
    "Model": f"{COMFYUI_ROOT}/models/checkpoints/z_image_turbo_bf16.safetensors",
    "CLIP": f"{COMFYUI_ROOT}/models/clip/qwen_3_4b.safetensors",
    "VAE": f"{COMFYUI_ROOT}/models/vae/ae.safetensors"
}

all_found = True
for name, path in all_files.items():
    if os.path.exists(path):
        size_gb = os.path.getsize(path) / (1024**3)
        print(f"✓ {name}: {size_gb:.2f} GB")
    else:
        print(f"✗ {name}: NOT FOUND")
        all_found = False

if all_found:
    print("\n🎉 All files downloaded successfully!")
    print("\nNext steps:")
    print("1. Restart ComfyUI or wait for it to rescan")
    print("2. Load the workflow - it should work now!")
else:
    print("\n⚠ Some files are still missing")
    print("Check the error messages above for manual download links")

print("\n" + "=" * 60)

