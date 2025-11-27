#!/usr/bin/env python3
"""
Quick test script to invoke ComfyUI workflow endpoint.
Submits a workflow JSON file and waits for completion.
"""

import json
import requests
import time
import sys
from pathlib import Path


# Configuration
BASE_URL = "https://h2gpcwjzl8iavs-8188.proxy.runpod.net"
WORKFLOW_FILE = "wavelength-md-campsite.json"


def load_workflow(file_path):
    """Load workflow JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: Workflow file not found: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in workflow file: {e}")
        sys.exit(1)


def submit_workflow(base_url, workflow):
    """Submit workflow to ComfyUI and return prompt_id."""
    print("=" * 60)
    print("Submitting workflow to ComfyUI...")
    print("=" * 60)
    
    try:
        response = requests.post(
            f"{base_url}/prompt",
            json={"prompt": workflow},
            timeout=30
        )
        response.raise_for_status()
        
        result = response.json()
        prompt_id = result.get("prompt_id")
        
        if prompt_id:
            print(f"✓ Workflow submitted successfully!")
            print(f"  Prompt ID: {prompt_id}")
            return prompt_id
        else:
            print(f"❌ Error: No prompt_id in response")
            print(f"  Response: {result}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error submitting workflow: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"  Response: {e.response.text}")
        return None


def check_queue(base_url, prompt_id):
    """Check if workflow is still in queue."""
    try:
        response = requests.get(f"{base_url}/queue", timeout=10)
        response.raise_for_status()
        queue_data = response.json()
        
        # Check running queue
        running = queue_data.get("queue_running", [])
        pending = queue_data.get("queue_pending", [])
        
        for item in running + pending:
            if item[1] == prompt_id:
                return True
        return False
        
    except Exception as e:
        print(f"⚠ Warning: Could not check queue: {e}")
        return True  # Assume still running if we can't check


def wait_for_completion(base_url, prompt_id, max_wait=300):
    """Wait for workflow to complete."""
    print("\n" + "=" * 60)
    print("Waiting for workflow to complete...")
    print("=" * 60)
    
    start_time = time.time()
    check_interval = 2  # Check every 2 seconds
    
    while time.time() - start_time < max_wait:
        # Check if still in queue
        if not check_queue(base_url, prompt_id):
            print(f"\n✓ Workflow completed!")
            return True
        
        elapsed = int(time.time() - start_time)
        print(f"  Waiting... ({elapsed}s elapsed)", end='\r')
        time.sleep(check_interval)
    
    print(f"\n⚠ Timeout: Workflow did not complete within {max_wait} seconds")
    return False


def get_history(base_url, prompt_id):
    """Get workflow history and find output images."""
    try:
        response = requests.get(f"{base_url}/history/{prompt_id}", timeout=10)
        response.raise_for_status()
        history = response.json()
        
        if prompt_id in history:
            workflow_data = history[prompt_id]
            outputs = workflow_data.get("outputs", {})
            
            images = []
            for node_id, node_output in outputs.items():
                if "images" in node_output:
                    for img_info in node_output["images"]:
                        images.append({
                            "filename": img_info.get("filename"),
                            "subfolder": img_info.get("subfolder", ""),
                            "type": img_info.get("type", "output")
                        })
            
            return images
        return []
        
    except Exception as e:
        print(f"⚠ Warning: Could not get history: {e}")
        return []


def download_image(base_url, filename, subfolder="", output_dir="outputs"):
    """Download generated image."""
    try:
        # ComfyUI image URL format
        url = f"{base_url}/view"
        params = {
            "filename": filename,
            "subfolder": subfolder,
            "type": "output"
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        # Create output directory
        Path(output_dir).mkdir(exist_ok=True)
        
        # Save image
        output_path = Path(output_dir) / filename
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ Downloaded: {output_path}")
        return str(output_path)
        
    except Exception as e:
        print(f"❌ Error downloading image: {e}")
        return None


def main():
    """Main execution."""
    print("\n" + "=" * 60)
    print("ComfyUI Workflow Test Script")
    print("=" * 60)
    
    # Load workflow
    workflow_path = Path(__file__).parent / WORKFLOW_FILE
    print(f"\n📄 Loading workflow: {workflow_path}")
    workflow = load_workflow(workflow_path)
    print(f"✓ Workflow loaded ({len(workflow)} nodes)")
    
    # Submit workflow
    prompt_id = submit_workflow(BASE_URL, workflow)
    if not prompt_id:
        print("\n❌ Failed to submit workflow")
        sys.exit(1)
    
    # Wait for completion
    if wait_for_completion(BASE_URL, prompt_id):
        # Get history and download images
        print("\n" + "=" * 60)
        print("Retrieving results...")
        print("=" * 60)
        
        images = get_history(BASE_URL, prompt_id)
        
        if images:
            print(f"\n✓ Found {len(images)} generated image(s):")
            for img in images:
                print(f"  - {img['filename']} (subfolder: {img['subfolder']})")
                download_image(BASE_URL, img['filename'], img['subfolder'])
        else:
            print("\n⚠ No images found in history")
            print("  Check ComfyUI web interface for results")
    else:
        print("\n⚠ Workflow may still be processing")
        print(f"  Check status at: {BASE_URL}")
        print(f"  Prompt ID: {prompt_id}")
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()

