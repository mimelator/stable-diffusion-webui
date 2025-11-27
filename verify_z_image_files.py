#!/usr/bin/env python3
"""
Verify z_image_turbo files are in correct locations
Run this in your RunPod notebook
"""

import os

COMFYUI_ROOT = "/workspace/runpod-slim/ComfyUI"

print("=" * 60)
print("Verifying z_image_turbo Files")
print("=" * 60)

# Expected file locations
files_to_check = {
    "Model (UNet)": {
        "path": f"{COMFYUI_ROOT}/models/checkpoints/z_image_turbo_bf16.safetensors",
        "found": False
    },
    "CLIP": {
        "path": f"{COMFYUI_ROOT}/models/clip/qwen_3_4b.safetensors",
        "found": False
    },
    "VAE": {
        "path": f"{COMFYUI_ROOT}/models/vae/ae.safetensors",
        "found": False
    }
}

# Also check alternative locations
alternative_locations = {
    "CLIP": [
        f"{COMFYUI_ROOT}/models/text_encoders/qwen_3_4b.safetensors",
        f"{COMFYUI_ROOT}/models/clip/qwen_3_4b.safetensors",
    ],
    "VAE": [
        f"{COMFYUI_ROOT}/models/vae/ae.safetensors",
    ]
}

print("\nChecking files...")
print("-" * 60)

for file_type, info in files_to_check.items():
    if os.path.exists(info["path"]):
        size_gb = os.path.getsize(info["path"]) / (1024**3)
        print(f"✓ {file_type}: {info['path']} ({size_gb:.2f} GB)")
        info["found"] = True
    else:
        print(f"✗ {file_type}: NOT FOUND at {info['path']}")
        
        # Check alternative locations
        if file_type in alternative_locations:
            for alt_path in alternative_locations[file_type]:
                if os.path.exists(alt_path):
                    size_gb = os.path.getsize(alt_path) / (1024**3)
                    print(f"  → Found at alternative location: {alt_path} ({size_gb:.2f} GB)")
                    info["found"] = True
                    info["path"] = alt_path
                    break

# List what's actually in directories
print("\n" + "=" * 60)
print("Files in directories:")
print("=" * 60)

directories_to_check = {
    "checkpoints": f"{COMFYUI_ROOT}/models/checkpoints",
    "clip": f"{COMFYUI_ROOT}/models/clip",
    "text_encoders": f"{COMFYUI_ROOT}/models/text_encoders",
    "vae": f"{COMFYUI_ROOT}/models/vae",
}

for dir_name, dir_path in directories_to_check.items():
    if os.path.exists(dir_path):
        files = [f for f in os.listdir(dir_path) 
                 if os.path.isfile(os.path.join(dir_path, f)) 
                 and f.endswith(('.safetensors', '.ckpt', '.pt'))]
        if files:
            print(f"\n{dir_name}/ ({len(files)} file(s)):")
            for f in files[:10]:  # Show first 10
                size_gb = os.path.getsize(f"{dir_path}/{f}") / (1024**3)
                print(f"  - {f} ({size_gb:.2f} GB)")
        else:
            print(f"\n{dir_name}/: (empty)")
    else:
        print(f"\n{dir_name}/: (directory not found)")

print("\n" + "=" * 60)
print("Summary & Recommendations")
print("=" * 60)

all_found = all(info["found"] for info in files_to_check.values())

if all_found:
    print("\n✓ All files found!")
    print("\nFiles are in correct locations:")
    for file_type, info in files_to_check.items():
        print(f"  {file_type}: {info['path']}")
else:
    print("\n✗ Some files are missing!")
    print("\nMissing files:")
    for file_type, info in files_to_check.items():
        if not info["found"]:
            print(f"  - {file_type}: {info['path']}")
    
    print("\nTo download missing files:")
    print("1. CLIP (qwen_3_4b.safetensors):")
    print("   https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/text_encoders/qwen_3_4b.safetensors")
    print("   → Place in: models/clip/ or models/text_encoders/")
    print("\n2. VAE (ae.safetensors):")
    print("   https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/vae/ae.safetensors")
    print("   → Place in: models/vae/")

print("\n" + "=" * 60)

