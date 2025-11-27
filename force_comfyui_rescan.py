#!/usr/bin/env python3
"""
Force ComfyUI to rescan models and verify file system
Run this in your RunPod notebook
"""

import os
import requests
import json

BASE_URL = "https://h2gpcwjzl8iavs-8188.proxy.runpod.net"
COMFYUI_ROOT = "/workspace/ComfyUI"

print("=" * 60)
print("ComfyUI Model Rescan & Verification")
print("=" * 60)

# Step 1: Verify file exists on disk
print("\n1. Verifying model file on disk...")
print("-" * 60)

model_file = f"{COMFYUI_ROOT}/models/checkpoints/z_image_turbo_bf16.safetensors"

if os.path.exists(model_file):
    size_gb = os.path.getsize(model_file) / (1024**3)
    print(f"✓ Model file exists: {model_file}")
    print(f"  Size: {size_gb:.2f} GB")
    
    # Check permissions
    import stat
    file_stat = os.stat(model_file)
    perms = oct(file_stat.st_mode)[-3:]
    print(f"  Permissions: {perms}")
    
    if perms != "644":
        print("  Fixing permissions...")
        os.chmod(model_file, 0o644)
        print("  ✓ Permissions fixed")
else:
    print(f"✗ Model file NOT found: {model_file}")
    print("\nChecking what's in checkpoints directory:")
    checkpoints_dir = f"{COMFYUI_ROOT}/models/checkpoints"
    if os.path.exists(checkpoints_dir):
        files = os.listdir(checkpoints_dir)
        print(f"  Found {len(files)} items:")
        for f in files:
            item_path = f"{checkpoints_dir}/{f}"
            if os.path.isfile(item_path):
                size_gb = os.path.getsize(item_path) / (1024**3)
                print(f"    File: {f} ({size_gb:.2f} GB)")
            else:
                print(f"    Directory: {f}/")

# Step 2: Check what ComfyUI API currently sees
print("\n2. Checking what ComfyUI API sees...")
print("-" * 60)

try:
    response = requests.get(f"{BASE_URL}/api/object_info", timeout=10)
    if response.status_code == 200:
        data = response.json()
        
        if 'CheckpointLoaderSimple' in data:
            ckpt_info = data['CheckpointLoaderSimple']['input']['required']['ckpt_name']
            print(f"  API structure type: {type(ckpt_info)}")
            
            if isinstance(ckpt_info, list):
                print(f"  List length: {len(ckpt_info)}")
                for i, item in enumerate(ckpt_info):
                    print(f"    Item {i}: {type(item)}")
                    if isinstance(item, list):
                        print(f"      Length: {len(item)}")
                        if len(item) == 0:
                            print("      ⚠ Empty list - ComfyUI hasn't scanned models yet!")
                        else:
                            print(f"      Models: {item[:5]}")
                            
                            # Check for turbo
                            turbo = [m for m in item if isinstance(m, str) and 'turbo' in m.lower()]
                            if turbo:
                                print(f"      ✓ Found turbo models: {turbo}")
                            else:
                                print(f"      ✗ No turbo models found")
                    elif isinstance(item, dict):
                        print(f"      Dictionary keys: {list(item.keys())}")
            
            # The empty list suggests ComfyUI needs to rescan
            if isinstance(ckpt_info, list) and len(ckpt_info) > 0:
                if isinstance(ckpt_info[0], list) and len(ckpt_info[0]) == 0:
                    print("\n  ⚠ ComfyUI model list is EMPTY")
                    print("  → ComfyUI needs to scan the models directory")
except Exception as e:
    print(f"  Error checking API: {e}")

# Step 3: List all files in checkpoints directory
print("\n3. Files in checkpoints directory:")
print("-" * 60)

checkpoints_dir = f"{COMFYUI_ROOT}/models/checkpoints"
if os.path.exists(checkpoints_dir):
    all_files = []
    for root, dirs, files in os.walk(checkpoints_dir):
        for file in files:
            if file.endswith(('.safetensors', '.ckpt', '.pt')):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, checkpoints_dir)
                size_gb = os.path.getsize(file_path) / (1024**3)
                all_files.append((rel_path, size_gb))
    
    if all_files:
        print(f"  Found {len(all_files)} model file(s):")
        for rel_path, size_gb in all_files:
            print(f"    - {rel_path} ({size_gb:.2f} GB)")
            
            # Check if turbo model
            if 'turbo' in rel_path.lower():
                print(f"      ✓ This is the turbo model!")
    else:
        print("  ✗ No model files found")
else:
    print(f"  ✗ Checkpoints directory not found: {checkpoints_dir}")

# Step 4: Recommendations
print("\n" + "=" * 60)
print("Recommendations")
print("=" * 60)

if os.path.exists(model_file):
    print("\n✓ Model file exists on disk")
    print("\nSince ComfyUI API shows empty model list, try:")
    print("\n1. FULLY restart ComfyUI:")
    print("   - Stop ComfyUI completely")
    print("   - Wait 10-15 seconds")
    print("   - Start ComfyUI again")
    print("   - ComfyUI should scan models directory on startup")
    print("\n2. Check ComfyUI startup logs for:")
    print("   - 'Loading checkpoint list'")
    print("   - Any errors reading model files")
    print("\n3. If restart doesn't work, check:")
    print("   - ComfyUI config files for model paths")
    print("   - File permissions (should be 644)")
    print("   - ComfyUI version compatibility")
else:
    print("\n✗ Model file not found at expected location")
    print("   Run the model location fix script first")

print("\n" + "=" * 60)

