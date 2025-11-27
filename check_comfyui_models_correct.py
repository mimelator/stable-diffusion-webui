#!/usr/bin/env python3
"""
Check ComfyUI models - exploring actual API structure
Run this in your RunPod notebook
"""

import requests
import json

BASE_URL = "https://h2gpcwjzl8iavs-8188.proxy.runpod.net"
endpoint = "/api/object_info"
url = f"{BASE_URL}{endpoint}"

print("=" * 60)
print("Exploring ComfyUI API Structure...")
print("=" * 60)

try:
    response = requests.get(url, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        
        # Explore CheckpointLoaderSimple structure
        if 'CheckpointLoaderSimple' in data:
            print("\nFound CheckpointLoaderSimple node")
            checkpoint_info = data['CheckpointLoaderSimple']
            
            print("\nFull structure:")
            print(json.dumps(checkpoint_info, indent=2)[:1000])  # First 1000 chars
            
            print("\n" + "=" * 60)
            print("Exploring input structure...")
            print("=" * 60)
            
            if 'input' in checkpoint_info:
                input_info = checkpoint_info['input']
                print("\n'input' keys:", list(input_info.keys()))
                
                if 'required' in input_info:
                    required = input_info['required']
                    print("\n'required' keys:", list(required.keys()))
                    
                    if 'ckpt_name' in required:
                        ckpt_name_info = required['ckpt_name']
                        print(f"\n'ckpt_name' type: {type(ckpt_name_info)}")
                        print(f"'ckpt_name' content:")
                        print(json.dumps(ckpt_name_info, indent=2))
                        
                        # Try different ways to extract models
                        print("\n" + "=" * 60)
                        print("Trying to extract model list...")
                        print("=" * 60)
                        
                        # Method 1: If it's a list, check each item
                        if isinstance(ckpt_name_info, list):
                            print(f"\nIt's a list with {len(ckpt_name_info)} items")
                            for i, item in enumerate(ckpt_name_info):
                                print(f"\nItem {i}:")
                                print(f"  Type: {type(item)}")
                                if isinstance(item, list):
                                    print(f"  Length: {len(item)}")
                                    if len(item) > 0:
                                        print(f"  First few items: {item[:10]}")
                                        
                                        # This might be the actual model list!
                                        models = item
                                        print(f"\n✓ Found {len(models)} model(s):")
                                        print("-" * 60)
                                        for m in models:
                                            print(f"  - {m}")
                                        
                                        # Check for turbo
                                        turbo_models = [m for m in models if isinstance(m, str) and 'turbo' in m.lower()]
                                        
                                        print("\n" + "=" * 60)
                                        if turbo_models:
                                            print("✓ z_image_turbo FOUND!")
                                            for m in turbo_models:
                                                print(f"  - {m}")
                                        else:
                                            print("✗ z_image_turbo NOT found")
                                        break
                                elif isinstance(item, dict):
                                    print(f"  Keys: {list(item.keys())}")
                                    # Check if there's a models key
                                    if 'models' in item or 'options' in item:
                                        print(f"  Found models/options key!")
                                else:
                                    print(f"  Value: {str(item)[:100]}")
                        
                        # Method 2: Check if there's a hidden key
                        if 'optional' in input_info:
                            optional = input_info['optional']
                            print(f"\n'optional' keys: {list(optional.keys())}")
                            if 'ckpt_name' in optional:
                                print("Found ckpt_name in optional!")
                                print(optional['ckpt_name'])
                
                # Check if there's a different structure
                if 'optional' in input_info:
                    optional = input_info['optional']
                    print(f"\n'optional' section found")
                    print(f"Keys: {list(optional.keys())}")
            
            # Also check other checkpoint loaders
            print("\n" + "=" * 60)
            print("Checking other checkpoint loaders...")
            print("=" * 60)
            
            checkpoint_loaders = [k for k in data.keys() if 'checkpoint' in k.lower() or 'ckpt' in k.lower()]
            if checkpoint_loaders:
                print(f"Found {len(checkpoint_loaders)} checkpoint-related nodes:")
                for loader in checkpoint_loaders:
                    print(f"  - {loader}")
                    loader_info = data[loader]
                    if 'input' in loader_info and 'required' in loader_info['input']:
                        if 'ckpt_name' in loader_info['input']['required']:
                            ckpt = loader_info['input']['required']['ckpt_name']
                            if isinstance(ckpt, list) and len(ckpt) > 0:
                                if isinstance(ckpt[0], list) and len(ckpt[0]) > 0:
                                    models = ckpt[0]
                                    print(f"    Found {len(models)} models!")
                                    for m in models[:5]:
                                        print(f"      - {m}")
        else:
            print("✗ CheckpointLoaderSimple not found")
            print("Available nodes:", list(data.keys())[:20])
            
    else:
        print(f"✗ Error: {response.status_code}")
        print(response.text[:500])
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)

