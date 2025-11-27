#!/usr/bin/env python3
"""
Find the correct ComfyUI API endpoints
Run this in your RunPod notebook
"""

import requests

BASE_URL = "https://h2gpcwjzl8iavs-8188.proxy.runpod.net"

print("=" * 60)
print("Finding ComfyUI API Endpoints...")
print("=" * 60)

# Common ComfyUI API endpoints to try
endpoints_to_try = [
    "/api/v1/models",
    "/api/models",
    "/api/v1/system_stats",
    "/api/system_stats",
    "/api/v1/object_info",
    "/api/object_info",
    "/api/v1/prompt",
    "/api/prompt",
    "/",
    "/api",
    "/api/v1",
]

print("\nTrying different API endpoints...")
print("-" * 60)

working_endpoints = []
failed_endpoints = []

for endpoint in endpoints_to_try:
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, timeout=5)
        status = response.status_code
        
        if status == 200:
            print(f"✓ {endpoint} → {status} OK")
            working_endpoints.append((endpoint, response))
            
            # Try to parse JSON
            try:
                data = response.json()
                if isinstance(data, dict):
                    print(f"    Keys: {list(data.keys())[:5]}")
            except:
                pass
        elif status == 404:
            print(f"✗ {endpoint} → 404 Not Found")
            failed_endpoints.append(endpoint)
        else:
            print(f"⚠ {endpoint} → {status}")
            
    except requests.exceptions.ConnectionError:
        print(f"✗ {endpoint} → Connection Error")
    except requests.exceptions.Timeout:
        print(f"✗ {endpoint} → Timeout")
    except Exception as e:
        print(f"✗ {endpoint} → Error: {e}")

print("\n" + "=" * 60)
print("Summary")
print("=" * 60)

if working_endpoints:
    print(f"\n✓ Found {len(working_endpoints)} working endpoint(s):")
    for endpoint, response in working_endpoints:
        print(f"  - {endpoint}")
        
        # Try to get models from working endpoints
        if 'models' in endpoint or 'object_info' in endpoint:
            try:
                data = response.json()
                if isinstance(data, dict):
                    if 'checkpoints' in data:
                        checkpoints = data['checkpoints']
                        print(f"    Found {len(checkpoints)} checkpoint(s)")
                        for m in checkpoints[:5]:
                            print(f"      - {m}")
                    elif 'CheckpointLoaderSimple' in str(data):
                        print(f"    This endpoint has model info")
            except:
                pass
else:
    print("\n✗ No working API endpoints found")
    print("\nPossible issues:")
    print("  1. ComfyUI API might not be enabled")
    print("  2. ComfyUI Manager might use different endpoints")
    print("  3. Need to check ComfyUI directly (not via API)")

# Try to get object_info which usually has model list
print("\n" + "=" * 60)
print("Checking object_info endpoint (most likely to have models)...")
print("=" * 60)

object_info_endpoints = [
    "/api/v1/object_info",
    "/api/object_info",
    "/object_info",
]

for endpoint in object_info_endpoints:
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Found object_info at: {endpoint}")
            
            # Look for checkpoint loader info
            if 'CheckpointLoaderSimple' in data:
                checkpoint_info = data['CheckpointLoaderSimple']
                if 'input' in checkpoint_info and 'required' in checkpoint_info['input']:
                    ckpt_input = checkpoint_info['input']['required']
                    if 'ckpt_name' in ckpt_input:
                        ckpt_options = ckpt_input['ckpt_name']
                        if isinstance(ckpt_options, list):
                            print(f"\nFound {len(ckpt_options)} checkpoint(s):")
                            for m in ckpt_options:
                                print(f"  - {m}")
                            
                            # Check for turbo
                            turbo_models = [m for m in ckpt_options if 'turbo' in m.lower()]
                            if turbo_models:
                                print(f"\n✓ z_image_turbo FOUND!")
                                for m in turbo_models:
                                    print(f"  - {m}")
                            else:
                                print(f"\n✗ z_image_turbo NOT found in list")
            break
    except Exception as e:
        pass

print("\n" + "=" * 60)

