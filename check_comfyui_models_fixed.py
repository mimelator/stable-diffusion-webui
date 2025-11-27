#!/usr/bin/env python3
"""
Check ComfyUI models using the correct endpoint
Run this in your RunPod notebook
"""

import requests

BASE_URL = "https://h2gpcwjzl8iavs-8188.proxy.runpod.net"

print("=" * 60)
print("Checking ComfyUI Models (using correct endpoint)...")
print("=" * 60)

# Use the working endpoint
endpoint = "/api/object_info"
url = f"{BASE_URL}{endpoint}"

try:
    response = requests.get(url, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ API endpoint working: {endpoint}\n")
        
        # Check for CheckpointLoaderSimple node (contains model list)
        if 'CheckpointLoaderSimple' in data:
            print("Found CheckpointLoaderSimple node")
            checkpoint_info = data['CheckpointLoaderSimple']
            
            if 'input' in checkpoint_info and 'required' in checkpoint_info['input']:
                required = checkpoint_info['input']['required']
                
                if 'ckpt_name' in required:
                    models = required['ckpt_name']
                    
                    if isinstance(models, list):
                        print(f"\nComfyUI sees {len(models)} checkpoint(s):")
                        print("-" * 60)
                        
                        for m in models:
                            print(f"  - {m}")
                        
                        # Check for turbo
                        turbo_models = [m for m in models if 'turbo' in m.lower()]
                        
                        print("\n" + "=" * 60)
                        if turbo_models:
                            print("✓ z_image_turbo FOUND in ComfyUI!")
                            print("\nModels found:")
                            for m in turbo_models:
                                print(f"  - {m}")
                            print("\n" + "=" * 60)
                            print("If ComfyUI Manager doesn't show it:")
                            print("  1. Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)")
                            print("  2. Look for 'Refresh' or 'Rescan' button in Manager")
                            print("  3. Check Manager settings for model paths")
                        else:
                            print("✗ z_image_turbo NOT found in ComfyUI")
                            print("\n" + "=" * 60)
                            print("ComfyUI hasn't detected the model file.")
                            print("\nTry these fixes:")
                            print("  1. FULLY restart ComfyUI (stop completely, wait 10s, start)")
                            print("  2. Check file permissions:")
                            print("     import os, stat")
                            print("     os.chmod('/workspace/ComfyUI/models/checkpoints/z_image_turbo_bf16.safetensors', 0o644)")
                            print("  3. Verify file location:")
                            print("     ls -lh /workspace/ComfyUI/models/checkpoints/ | grep turbo")
                    else:
                        print(f"\n⚠ Model list is not a list, it's: {type(models)}")
                        print(f"Content preview: {str(models)[:200]}")
                else:
                    print("\n✗ 'ckpt_name' not found in CheckpointLoaderSimple")
                    print("Available keys in 'required':", list(required.keys())[:10])
            else:
                print("\n✗ 'input.required' not found in CheckpointLoaderSimple")
                print("Available keys:", list(checkpoint_info.keys())[:10])
        else:
            print("\n✗ CheckpointLoaderSimple node not found")
            print(f"Available nodes ({len(data)} total):")
            for node_name in list(data.keys())[:15]:
                print(f"  - {node_name}")
            
    else:
        print(f"✗ API Error: {response.status_code}")
        print(f"  Response: {response.text[:200]}")
        
except requests.exceptions.ConnectionError:
    print("✗ Connection Error: Cannot reach ComfyUI")
    print("  - Check if ComfyUI is running")
    print("  - Verify URL is correct")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print(f"  Type: {type(e).__name__}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)

