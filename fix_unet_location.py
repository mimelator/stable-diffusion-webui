#!/usr/bin/env python3
"""
Move z_image_turbo UNet to correct location
Run this in your RunPod notebook
"""

import os
import shutil

COMFYUI_ROOT = "/workspace/runpod-slim/ComfyUI"

# Current and target locations
current_location = f"{COMFYUI_ROOT}/models/checkpoints/z_image_turbo_bf16.safetensors"
unet_dir = f"{COMFYUI_ROOT}/models/unet"
target_location = f"{unet_dir}/z_image_turbo_bf16.safetensors"

print("=" * 60)
print("Moving UNet to Correct Location")
print("=" * 60)

# Create unet directory if needed
os.makedirs(unet_dir, exist_ok=True)
print(f"✓ UNet directory ready: {unet_dir}")

# Check current location
if os.path.exists(current_location):
    size_gb = os.path.getsize(current_location) / (1024**3)
    print(f"\n✓ Found model at: {current_location} ({size_gb:.2f} GB)")
    
    # Check if already in target location
    if os.path.exists(target_location):
        target_size = os.path.getsize(target_location) / (1024**3)
        print(f"\n⚠ Model already exists at target location: {target_location} ({target_size:.2f} GB)")
        
        if abs(size_gb - target_size) < 0.01:
            print("  Sizes match - keeping target location, removing duplicate")
            os.remove(current_location)
            print("  ✓ Removed duplicate from checkpoints/")
        else:
            print("  Sizes differ - replacing with current file")
            os.remove(target_location)
            shutil.move(current_location, target_location)
            print(f"  ✓ Moved to: {target_location}")
    else:
        # Move to target location
        print(f"\nMoving model to UNet directory...")
        shutil.move(current_location, target_location)
        print(f"  ✓ Moved to: {target_location}")
        
        # Verify
        if os.path.exists(target_location):
            verify_size = os.path.getsize(target_location) / (1024**3)
            print(f"  ✓ Verified: {verify_size:.2f} GB")
else:
    print(f"\n✗ Model not found at: {current_location}")
    
    # Check if already in target location
    if os.path.exists(target_location):
        size_gb = os.path.getsize(target_location) / (1024**3)
        print(f"✓ Model already at correct location: {target_location} ({size_gb:.2f} GB)")
    else:
        print(f"✗ Model not found at target location either: {target_location}")

# List files in unet directory
print("\n" + "=" * 60)
print("Files in unet/ directory:")
print("=" * 60)

if os.path.exists(unet_dir):
    files = [f for f in os.listdir(unet_dir) 
             if os.path.isfile(f"{unet_dir}/{f}") 
             and f.endswith(('.safetensors', '.ckpt', '.pt'))]
    if files:
        for f in files:
            size_gb = os.path.getsize(f"{unet_dir}/{f}") / (1024**3)
            print(f"  ✓ {f} ({size_gb:.2f} GB)")
    else:
        print("  (no files found)")

print("\n" + "=" * 60)
print("Summary")
print("=" * 60)

if os.path.exists(target_location):
    print("\n✓ UNet file is in correct location")
    print(f"  {target_location}")
    print("\nNext steps:")
    print("1. Restart ComfyUI or wait for rescan")
    print("2. The workflow should now work!")
else:
    print("\n✗ UNet file not found")
    print("  Check file locations manually")

print("=" * 60)

