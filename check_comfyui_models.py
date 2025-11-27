#!/usr/bin/env python3
"""
Check what models ComfyUI API detects
Run this in your RunPod notebook
"""

import requests

BASE_URL = "https://h2gpcwjzl8iavs-8188.proxy.runpod.net"

print("=" * 60)
print("Checking ComfyUI API for models...")
print("=" * 60)

try:
    response = requests.get(f"{BASE_URL}/api/v1/models", timeout=10)
    
    if response.status_code == 200:
        models = response.json()
        checkpoints = models.get('checkpoints', [])
        
        print(f"\nComfyUI sees {len(checkpoints)} checkpoint(s):")
        print("-" * 60)
        
        if checkpoints:
            for m in checkpoints:
                print(f"  - {m}")
        else:
            print("  (no checkpoints found)")
        
        # Check for turbo
        turbo_models = [m for m in checkpoints if 'turbo' in m.lower()]
        
        print("\n" + "=" * 60)
        if turbo_models:
            print("✓ z_image_turbo FOUND in API!")
            print("  Models found:")
            for m in turbo_models:
                print(f"    - {m}")
            print("\nIf Manager doesn't show it, try:")
            print("  1. Hard refresh browser (Ctrl+Shift+R)")
            print("  2. Check ComfyUI Manager settings")
        else:
            print("✗ z_image_turbo NOT in API response")
            print("\nThis means ComfyUI hasn't detected the model file yet.")
            print("Try:")
            print("  1. FULLY restart ComfyUI (stop completely, wait, start)")
            print("  2. Check file permissions")
            print("  3. Verify file is at correct location")
        
        # Also show other model types
        print("\n" + "=" * 60)
        print("Other model types:")
        print("-" * 60)
        for key in models.keys():
            if key != 'checkpoints':
                count = len(models.get(key, []))
                if count > 0:
                    print(f"  {key}: {count} model(s)")
        
    else:
        print(f"✗ API Error: {response.status_code}")
        print(f"  Response: {response.text}")
        print("\nPossible issues:")
        print("  - ComfyUI not running")
        print("  - Wrong URL")
        print("  - API endpoint changed")
        
except requests.exceptions.ConnectionError:
    print("✗ Connection Error: Cannot reach ComfyUI")
    print("\nPossible issues:")
    print("  - ComfyUI not running")
    print("  - Wrong URL")
    print("  - Network/firewall issue")
    
except requests.exceptions.Timeout:
    print("✗ Timeout: ComfyUI didn't respond in time")
    print("  Try again or check if ComfyUI is running")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print(f"  Type: {type(e).__name__}")

print("\n" + "=" * 60)

