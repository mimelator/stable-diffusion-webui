#!/usr/bin/env python3
"""
Example usage of the Enhanced API Wrapper
Demonstrates various use cases and configurations
"""

import requests
import json
import base64
from pathlib import Path

API_URL = "http://localhost:8080/generate"


def save_image(base64_data, filename):
    """Save base64 image to file"""
    image_data = base64.b64decode(base64_data)
    with open(filename, 'wb') as f:
        f.write(image_data)
    print(f"Saved: {filename}")


def example_1_basic():
    """Example 1: Basic generation with preset"""
    print("\n=== Example 1: Basic Generation ===")
    
    payload = {
        "prompt": "masterpiece, best quality, highly detailed, 8k, a beautiful portrait, photorealistic",
        "model": "real-dreams"
    }
    
    response = requests.post(API_URL, json=payload)
    result = response.json()
    
    if result["status"] == "success":
        print(f"✓ Generated successfully")
        print(f"  Model: {result['model_used']}")
        print(f"  Steps: {result['parameters']['steps']}")
        print(f"  CFG: {result['parameters']['cfg_scale']}")
        save_image(result["images"][0], "example_1_basic.png")
    else:
        print(f"✗ Error: {result}")


def example_2_with_adetailer():
    """Example 2: With ADetailer enabled"""
    print("\n=== Example 2: With ADetailer ===")
    
    payload = {
        "prompt": "masterpiece, best quality, highly detailed, 8k, a beautiful portrait, photorealistic",
        "model": "real-dreams",
        "adetailer": {
            "enabled": True,
            "model": "face_yolov8n.pt"
        }
    }
    
    response = requests.post(API_URL, json=payload)
    result = response.json()
    
    if result["status"] == "success":
        print(f"✓ Generated with ADetailer")
        print(f"  ADetailer enabled: {result['parameters']['adetailer_enabled']}")
        save_image(result["images"][0], "example_2_adetailer.png")
    else:
        print(f"✗ Error: {result}")


def example_3_with_hires_fix():
    """Example 3: With Hires.Fix"""
    print("\n=== Example 3: With Hires.Fix ===")
    
    payload = {
        "prompt": "masterpiece, best quality, highly detailed, 8k, a beautiful portrait, photorealistic",
        "model": "real-dreams",
        "hires_fix": {
            "enabled": True,
            "scale": 1.5,
            "upscaler": "4x-UltraSharp"
        }
    }
    
    response = requests.post(API_URL, json=payload)
    result = response.json()
    
    if result["status"] == "success":
        print(f"✓ Generated with Hires.Fix")
        print(f"  Hires.Fix enabled: {result['parameters']['hires_fix_enabled']}")
        save_image(result["images"][0], "example_3_hires_fix.png")
    else:
        print(f"✗ Error: {result}")


def example_4_full_configuration():
    """Example 4: Full configuration with ADetailer and Hires.Fix"""
    print("\n=== Example 4: Full Configuration ===")
    
    payload = {
        "prompt": "masterpiece, best quality, highly detailed, 8k, a beautiful portrait, photorealistic",
        "negative_prompt": "lowres, bad anatomy, bad hands, text, error, worst quality, low quality",
        "model": "real-dreams",
        "steps": 30,
        "cfg_scale": 8.0,
        "sampler": "DPM++ 2M Karras",
        "width": 768,
        "height": 1024,
        "seed": 42,
        "adetailer": {
            "enabled": True,
            "model": "face_yolov8n.pt",
            "denoising_strength": 0.4,
            "steps": 28,
            "cfg_scale": 7.0
        },
        "hires_fix": {
            "enabled": True,
            "scale": 1.5,
            "upscaler": "4x-UltraSharp",
            "denoising_strength": 0.4
        }
    }
    
    response = requests.post(API_URL, json=payload)
    result = response.json()
    
    if result["status"] == "success":
        print(f"✓ Generated with full configuration")
        print(f"  Model: {result['model_used']}")
        print(f"  Resolution: {result['parameters']['width']}x{result['parameters']['height']}")
        print(f"  Steps: {result['parameters']['steps']}")
        print(f"  ADetailer: {result['parameters']['adetailer_enabled']}")
        print(f"  Hires.Fix: {result['parameters']['hires_fix_enabled']}")
        save_image(result["images"][0], "example_4_full_config.png")
    else:
        print(f"✗ Error: {result}")


def example_5_switch_model():
    """Example 5: Switch to Realistic Vision model"""
    print("\n=== Example 5: Switch Model ===")
    
    payload = {
        "prompt": "ultra realistic portrait, professional photography, sharp focus",
        "model": "realistic-vision",
        "adetailer": {
            "enabled": True
        }
    }
    
    response = requests.post(API_URL, json=payload)
    result = response.json()
    
    if result["status"] == "success":
        print(f"✓ Generated with Realistic Vision")
        print(f"  Model: {result['model_used']}")
        print(f"  Model file: {result['model_file']}")
        save_image(result["images"][0], "example_5_realistic_vision.png")
    else:
        print(f"✗ Error: {result}")


def example_6_custom_adetailer():
    """Example 6: Custom ADetailer configuration"""
    print("\n=== Example 6: Custom ADetailer ===")
    
    payload = {
        "prompt": "masterpiece, best quality, highly detailed, 8k, a beautiful portrait",
        "model": "real-dreams",
        "adetailer": {
            "enabled": True,
            "model": "face_yolov8n.pt",
            "detection_confidence": 0.3,
            "denoising_strength": 0.4,
            "steps": 28,
            "cfg_scale": 7.0,
            "sampler": "DPM++ SDE Karras",
            "prompt": "beautiful face, detailed eyes, perfect skin, photorealistic",
            "negative_prompt": "blurry face, deformed face, bad eyes, bad anatomy",
            "mask_only_top_k": 1
        }
    }
    
    response = requests.post(API_URL, json=payload)
    result = response.json()
    
    if result["status"] == "success":
        print(f"✓ Generated with custom ADetailer")
        save_image(result["images"][0], "example_6_custom_adetailer.png")
    else:
        print(f"✗ Error: {result}")


def example_7_batch_generation():
    """Example 7: Batch generation"""
    print("\n=== Example 7: Batch Generation ===")
    
    prompts = [
        "masterpiece, best quality, a beautiful portrait of a woman",
        "masterpiece, best quality, a handsome portrait of a man",
        "masterpiece, best quality, a cute portrait of a child"
    ]
    
    results = []
    for i, prompt in enumerate(prompts):
        payload = {
            "prompt": prompt,
            "model": "real-dreams",
            "adetailer": {
                "enabled": True
            }
        }
        
        response = requests.post(API_URL, json=payload)
        result = response.json()
        
        if result["status"] == "success":
            filename = f"example_7_batch_{i+1}.png"
            save_image(result["images"][0], filename)
            results.append(result)
    
    print(f"✓ Generated {len(results)} images in batch")


def check_api_health():
    """Check if API wrapper is running"""
    try:
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            if health["status"] == "healthy":
                print("✓ API Wrapper is running")
                print(f"  WebUI accessible: {health['webui_accessible']}")
                print(f"  Current WebUI model: {health.get('current_webui_model', 'Unknown')}")
                return True
            else:
                print(f"✗ API Wrapper unhealthy: {health.get('error', 'Unknown error')}")
                return False
        else:
            print(f"✗ API Wrapper returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to API Wrapper")
        print("  Make sure it's running: python enhanced_api_wrapper.py")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Enhanced API Wrapper - Example Usage")
    print("=" * 60)
    
    # Check API health
    if not check_api_health():
        print("\nPlease start the API wrapper first:")
        print("  python enhanced_api_wrapper.py")
        exit(1)
    
    print("\nRunning examples...")
    print("=" * 60)
    
    # Run examples (comment out ones you don't want to run)
    try:
        example_1_basic()
        # example_2_with_adetailer()
        # example_3_with_hires_fix()
        # example_4_full_configuration()
        # example_5_switch_model()
        # example_6_custom_adetailer()
        # example_7_batch_generation()
        
        print("\n" + "=" * 60)
        print("Examples completed!")
        print("=" * 60)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

