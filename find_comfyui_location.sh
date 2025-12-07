#!/bin/bash
# Quick script to find ComfyUI location on RunPod

echo "=== Finding ComfyUI Location ==="
echo ""

# Check common locations
LOCATIONS=(
    "/workspace/runpod-slim/ComfyUI"
    "/workspace/ComfyUI"
    "/workspace/comfyui"
    "/ComfyUI"
    "/comfyui"
)

echo "Checking common locations..."
for loc in "${LOCATIONS[@]}"; do
    if [ -d "$loc" ]; then
        echo "✓ FOUND: $loc"
        echo "  Contents:"
        ls -la "$loc" | head -5
        echo ""
        
        # Check for main.py
        if [ -f "$loc/main.py" ]; then
            echo "  ✓ main.py found - this is ComfyUI!"
        fi
        
        # Check for models directory
        if [ -d "$loc/models" ]; then
            echo "  ✓ models/ directory found"
            echo "  Model subdirectories:"
            ls -d "$loc/models"/*/ 2>/dev/null | sed 's|.*/||' | sed 's|/$||' | sed 's/^/    - /'
        fi
        echo ""
    fi
done

echo "=== Searching entire /workspace ==="
echo "Searching for ComfyUI directories..."
find /workspace -type d -name "ComfyUI" -o -name "comfyui" 2>/dev/null | head -10

echo ""
echo "=== Searching for main.py (ComfyUI entry point) ==="
find /workspace -name "main.py" -path "*/ComfyUI/*" 2>/dev/null | head -5

echo ""
echo "=== Current directory structure ==="
echo "You are in: $(pwd)"
echo ""
echo "Contents of /workspace:"
ls -la /workspace/ | head -10
