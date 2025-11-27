#!/usr/bin/env python3
"""
Fix model path - Move model to correct ComfyUI location
Run this in your RunPod notebook
"""

import os
import shutil

# ComfyUI paths
WRONG_PATH = "/workspace/ComfyUI/models/checkpoints"
CORRECT_PATH = "/workspace/runpod-slim/ComfyUI/models/checkpoints"

MODEL_FILE = "z_image_turbo_bf16.safetensors"

print("=" * 60)
print("Fixing Model Path")
print("=" * 60)

print(f"\nComfyUI expects models at: {CORRECT_PATH}")
print(f"Model currently at: {WRONG_PATH}")

# Check if correct directory exists
if not os.path.exists(CORRECT_PATH):
    print(f"\nCreating directory: {CORRECT_PATH}")
    os.makedirs(CORRECT_PATH, exist_ok=True)
    print("✓ Directory created")

# Check if model exists in wrong location
wrong_location = f"{WRONG_PATH}/{MODEL_FILE}"
correct_location = f"{CORRECT_PATH}/{MODEL_FILE}"

if os.path.exists(wrong_location):
    print(f"\n✓ Found model at wrong location: {wrong_location}")
    size_gb = os.path.getsize(wrong_location) / (1024**3)
    print(f"  Size: {size_gb:.2f} GB")
    
    # Check if already exists in correct location
    if os.path.exists(correct_location):
        print(f"\n⚠ Model already exists at correct location!")
        print(f"  {correct_location}")
        
        # Compare sizes
        correct_size = os.path.getsize(correct_location) / (1024**3)
        if abs(size_gb - correct_size) < 0.01:
            print("  Sizes match - model is already in correct location")
            print("  Removing duplicate from wrong location...")
            os.remove(wrong_location)
            print("  ✓ Removed duplicate")
        else:
            print(f"  Sizes differ: {size_gb:.2f} GB vs {correct_size:.2f} GB")
            response = input("  Replace existing file? (y/n): ")
            if response.lower() == 'y':
                os.remove(correct_location)
                shutil.move(wrong_location, correct_location)
                print("  ✓ Moved model to correct location")
            else:
                print("  Keeping existing file")
    else:
        # Move model to correct location
        print(f"\nMoving model to correct location...")
        print(f"  From: {wrong_location}")
        print(f"  To:   {correct_location}")
        
        shutil.move(wrong_location, correct_location)
        print("  ✓ Model moved successfully!")
        
        # Verify
        if os.path.exists(correct_location):
            verify_size = os.path.getsize(correct_location) / (1024**3)
            print(f"  ✓ Verified: {verify_size:.2f} GB at correct location")
        
elif os.path.exists(correct_location):
    print(f"\n✓ Model already at correct location!")
    print(f"  {correct_location}")
    size_gb = os.path.getsize(correct_location) / (1024**3)
    print(f"  Size: {size_gb:.2f} GB")
else:
    print(f"\n✗ Model not found at either location!")
    print(f"  Checked: {wrong_location}")
    print(f"  Checked: {correct_location}")

# List files in correct location
print(f"\n" + "=" * 60)
print("Files in correct checkpoints directory:")
print("=" * 60)

if os.path.exists(CORRECT_PATH):
    files = [f for f in os.listdir(CORRECT_PATH) 
             if os.path.isfile(f"{CORRECT_PATH}/{f}") 
             and f.endswith(('.safetensors', '.ckpt', '.pt'))]
    
    if files:
        for f in files:
            size_gb = os.path.getsize(f"{CORRECT_PATH}/{f}") / (1024**3)
            print(f"  ✓ {f} ({size_gb:.2f} GB)")
            if 'turbo' in f.lower():
                print(f"    → This is z_image_turbo!")
    else:
        print("  (no model files found)")

print("\n" + "=" * 60)
print("Next Steps:")
print("=" * 60)
print("1. Restart ComfyUI (or wait for it to rescan)")
print("2. Check ComfyUI Manager - model should appear")
print("3. Or verify via API:")
print("   import requests")
print(f"   response = requests.get('https://h2gpcwjzl8iavs-8188.proxy.runpod.net/api/object_info')")
print("   models = response.json()['CheckpointLoaderSimple']['input']['required']['ckpt_name'][0]")
print("   print(models)")
print("=" * 60)

