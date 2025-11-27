#!/usr/bin/env python3
"""
Verify model file location and check ComfyUI configuration
Run this in your RunPod notebook
"""

import os
import stat

COMFYUI_ROOT = "/workspace/ComfyUI"
checkpoints_dir = f"{COMFYUI_ROOT}/models/checkpoints"

print("=" * 60)
print("Verifying Model File Location")
print("=" * 60)

# Check if checkpoints directory exists
print(f"\n1. Checking checkpoints directory...")
if os.path.exists(checkpoints_dir):
    print(f"   ✓ Directory exists: {checkpoints_dir}")
    
    # List all files in checkpoints directory
    print(f"\n2. Files in checkpoints directory:")
    print("-" * 60)
    
    all_items = os.listdir(checkpoints_dir)
    model_files = []
    subdirs = []
    
    for item in all_items:
        item_path = os.path.join(checkpoints_dir, item)
        if os.path.isfile(item_path):
            if item.endswith(('.safetensors', '.ckpt', '.pt')):
                size_gb = os.path.getsize(item_path) / (1024**3)
                model_files.append((item, size_gb))
        elif os.path.isdir(item_path):
            subdirs.append(item)
    
    if model_files:
        print(f"   Found {len(model_files)} model file(s) directly in checkpoints/:")
        for filename, size_gb in model_files:
            print(f"     ✓ {filename} ({size_gb:.2f} GB)")
            if 'turbo' in filename.lower():
                print(f"       → This is the z_image_turbo model!")
    else:
        print("   ✗ No model files found directly in checkpoints/")
    
    if subdirs:
        print(f"\n   Found {len(subdirs)} subdirectory(ies):")
        for subdir in subdirs:
            print(f"     - {subdir}/")
            # Check if there are models in subdirectories
            subdir_path = os.path.join(checkpoints_dir, subdir)
            subdir_files = [f for f in os.listdir(subdir_path) 
                           if os.path.isfile(os.path.join(subdir_path, f)) 
                           and f.endswith(('.safetensors', '.ckpt', '.pt'))]
            if subdir_files:
                print(f"       → Contains {len(subdir_files)} model file(s)")
                for f in subdir_files[:3]:
                    print(f"         - {f}")
    
    # Check for z_image_turbo specifically
    print(f"\n3. Searching for z_image_turbo model...")
    print("-" * 60)
    
    turbo_found = False
    for root, dirs, files in os.walk(checkpoints_dir):
        for file in files:
            if 'turbo' in file.lower() and file.endswith(('.safetensors', '.ckpt', '.pt')):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, checkpoints_dir)
                size_gb = os.path.getsize(file_path) / (1024**3)
                print(f"   ✓ Found: {rel_path} ({size_gb:.2f} GB)")
                turbo_found = True
                
                # Check if it's in the root or subdirectory
                if rel_path == file:
                    print(f"     → Location: ✓ CORRECT (directly in checkpoints/)")
                else:
                    print(f"     → Location: ⚠ WRONG (in subdirectory)")
                    print(f"     → Should be moved to: {file}")
    
    if not turbo_found:
        print("   ✗ z_image_turbo model not found")
    
    # Check permissions
    print(f"\n4. Checking file permissions...")
    print("-" * 60)
    
    for root, dirs, files in os.walk(checkpoints_dir):
        for file in files:
            if file.endswith(('.safetensors', '.ckpt', '.pt')):
                file_path = os.path.join(root, file)
                file_stat = os.stat(file_path)
                perms = oct(file_stat.st_mode)[-3:]
                print(f"   {os.path.basename(file_path)}: {perms}")
                
                if perms != "644":
                    print(f"     ⚠ Should be 644, fixing...")
                    try:
                        os.chmod(file_path, 0o644)
                        print(f"     ✓ Fixed")
                    except Exception as e:
                        print(f"     ✗ Error: {e}")
                break  # Just check first file
    
    # Check directory permissions
    dir_stat = os.stat(checkpoints_dir)
    dir_perms = oct(dir_stat.st_mode)[-3:]
    print(f"\n   Directory permissions: {dir_perms}")
    if dir_perms != "755":
        print(f"     ⚠ Should be 755, fixing...")
        try:
            os.chmod(checkpoints_dir, 0o755)
            print(f"     ✓ Fixed")
        except Exception as e:
            print(f"     ✗ Error: {e}")
    
else:
    print(f"   ✗ Directory not found: {checkpoints_dir}")

# Check ComfyUI config
print(f"\n5. Checking ComfyUI configuration...")
print("-" * 60)

config_files = [
    f"{COMFYUI_ROOT}/config.yaml",
    f"{COMFYUI_ROOT}/extra_model_paths.yaml",
    f"{COMFYUI_ROOT}/.config.yaml",
]

for config_file in config_files:
    if os.path.exists(config_file):
        print(f"   Found config: {config_file}")
        try:
            with open(config_file, 'r') as f:
                content = f.read()
                if 'checkpoints' in content.lower() or 'models' in content.lower():
                    print(f"     → Contains model path configuration")
        except:
            pass

print("\n" + "=" * 60)
print("Summary & Recommendations")
print("=" * 60)

if turbo_found:
    print("\n✓ z_image_turbo model file exists")
    print("\nIf ComfyUI still doesn't show it:")
    print("  1. Ensure model is directly in checkpoints/ (not subdirectory)")
    print("  2. Check ComfyUI logs for scanning errors")
    print("  3. Try manually typing the filename in CheckpointLoaderSimple node")
    print("  4. Some ComfyUI versions need explicit model list refresh")
else:
    print("\n✗ z_image_turbo model file not found")
    print("  Run the model download script again")

print("\n" + "=" * 60)

