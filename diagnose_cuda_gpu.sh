#!/bin/bash
# Diagnose CUDA/GPU issues on RunPod

echo "=== CUDA/GPU Diagnosis ==="
echo ""

# Check if nvidia-smi works
echo "1. Checking nvidia-smi..."
if command -v nvidia-smi >/dev/null 2>&1; then
    nvidia-smi
    echo ""
else
    echo "✗ nvidia-smi not found or not accessible"
    echo ""
fi

# Check CUDA_VISIBLE_DEVICES
echo "2. Checking CUDA_VISIBLE_DEVICES..."
if [ -n "$CUDA_VISIBLE_DEVICES" ]; then
    echo "  CUDA_VISIBLE_DEVICES=$CUDA_VISIBLE_DEVICES"
else
    echo "  CUDA_VISIBLE_DEVICES is not set"
fi
echo ""

# Check if /dev/nvidia* devices exist
echo "3. Checking for NVIDIA devices..."
if ls /dev/nvidia* >/dev/null 2>&1; then
    echo "  ✓ NVIDIA devices found:"
    ls -la /dev/nvidia* | head -5
else
    echo "  ✗ No NVIDIA devices found in /dev/"
fi
echo ""

# Check Python torch CUDA availability
echo "4. Checking PyTorch CUDA..."
python3 << EOF
import sys
try:
    import torch
    print(f"  PyTorch version: {torch.__version__}")
    print(f"  CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"  CUDA version: {torch.version.cuda}")
        print(f"  Number of GPUs: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
    else:
        print("  ✗ CUDA is not available in PyTorch")
        print("  Trying to get more info...")
        try:
            torch.cuda.current_device()
        except Exception as e:
            print(f"  Error: {e}")
except ImportError:
    print("  ✗ PyTorch not installed")
except Exception as e:
    print(f"  ✗ Error: {e}")
EOF

echo ""

# Check if we're in a container with GPU access
echo "5. Checking container/GPU access..."
if [ -f /.dockerenv ]; then
    echo "  Running in Docker container"
fi

# Check for GPU in /proc/driver
if [ -d /proc/driver/nvidia ]; then
    echo "  ✓ NVIDIA driver directory exists"
    if [ -f /proc/driver/nvidia/version ]; then
        echo "  Driver version:"
        cat /proc/driver/nvidia/version
    fi
else
    echo "  ✗ No NVIDIA driver found in /proc/driver/"
fi

echo ""
echo "=== Summary ==="
echo "If nvidia-smi works: GPU is accessible"
echo "If nvidia-smi fails: GPU is not accessible to this container/Pod"
echo ""
echo "Common fixes:"
echo "1. Ensure Pod has GPU attached in RunPod dashboard"
echo "2. Check Pod template has GPU support enabled"
echo "3. Try restarting the Pod"
echo "4. Check RunPod GPU availability in your region"
