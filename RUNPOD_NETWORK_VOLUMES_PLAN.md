# RunPod Network Volumes - Reuse Plan for ComfyUI + z_image

## Overview

Network volumes provide persistent storage that survives Pod termination, making them perfect for storing your ComfyUI installation and z_image_turbo models (~20GB). This eliminates the need to re-download models every time you deploy a new Pod.

**Reference**: [RunPod Network Volumes Documentation](https://docs.runpod.io/storage/network-volumes)

---

## Benefits for Your Setup

### Why Use Network Volumes?

1. **Persistent Model Storage** (~20GB saved)
   - z_image_turbo models stay on the volume
   - No re-downloading when deploying new Pods
   - Saves time (20-30 minutes) and bandwidth

2. **Cost Efficiency**
   - Network volume: ~$1.40/month for 20GB ($0.07/GB)
   - Re-downloading 20GB repeatedly: More expensive in bandwidth/time
   - Share models across multiple Pods

3. **Faster Pod Deployment**
   - Models already available
   - No waiting for downloads
   - Start generating immediately

4. **Share Between Pods**
   - Use same models on different Pods
   - Test different GPU types without re-downloading
   - Maintain consistent model versions

---

## Cost Analysis

### Network Volume Pricing

- **First 1TB**: $0.07 per GB per month
- **Beyond 1TB**: $0.05 per GB per month

### Your Use Case

**Storage Needed**:
- ComfyUI installation: ~2-5 GB
- z_image_turbo models: ~20 GB
- Additional models: Variable
- Outputs/workflows: Variable

**Recommended Volume Size**: **50-100 GB** (allows room for growth)

**Monthly Cost**:
- 50 GB: $3.50/month
- 100 GB: $7.00/month

**Cost vs. Re-downloading**:
- Downloading 20GB repeatedly: Time cost + bandwidth
- Network volume: One-time setup, persistent storage
- **Break-even**: If you deploy Pods more than 2-3 times per month, network volume is cheaper

---

## Implementation Plan

### Phase 1: Create Network Volume

1. **Go to RunPod Console**
   - Navigate to: https://www.runpod.io/console/storage
   - Click **"New Network Volume"**

2. **Configure Volume**
   - **Name**: `comfyui-zimage-models` (or descriptive name)
   - **Size**: 50-100 GB (recommended)
   - **Datacenter**: Choose based on:
     - GPU availability in that region
     - Your preferred location
     - Note: S3 API available in: `EUR-IS-1`, `EU-RO-1`, `EU-CZ-1`, `US-KS-2`, `US-CA-2`

3. **Create Volume**
   - Click **"Create Network Volume"**
   - Note the volume ID/name for later use

### Phase 2: Initial Setup (One-Time)

#### Access Methods

You have **three options** to access your Pod and run commands:

**Option 1: JupyterLab (Recommended - Easiest)**
- RunPod Dashboard → Your Pod → Connect → **JupyterLab**
- Opens web-based interface with terminal and file browser
- **Best for**: Running scripts, uploading files, viewing outputs
- **No SSH setup needed**

**Option 2: Web Terminal**
- RunPod Dashboard → Your Pod → Connect → **Web Terminal**
- Simple terminal in browser
- **Best for**: Quick commands, simple tasks
- **No SSH setup needed**

**Option 3: SSH (Advanced)**
- RunPod Dashboard → Your Pod → Connect → **SSH**
- Copy SSH command (e.g., `ssh root@xxxxx.runpod.io -p xxxxx`)
- Run in your local terminal
- **Best for**: Advanced users, local terminal preferences
- **Requires**: SSH client on your machine

**Recommendation**: Use **JupyterLab** for Phase 2 - it's the easiest and most user-friendly.

---

#### Setup Steps

1. **Deploy Pod with Network Volume**
   - Go to Pods → Deploy
   - **Select Network Volume**: Choose your existing volume (or create new one)
   - **Select GPU type**: (e.g., RTX 3090, RTX 4090, A100)
   - **Select Pod Template**: 
     - Search for "ComfyUI" or use template ID: `cw3nka7d08`
     - Or use direct link: https://console.runpod.io/hub/template/comfyui?id=cw3nka7d08
   - **Important**: 
     - Network volume mounts at `/workspace` by default
     - This replaces the Pod's default disk
     - ComfyUI will be installed on the network volume
   - Configure other settings (environment variables, etc.)
   - Click **Deploy On-Demand**
   - Wait for pod to start (2-3 minutes)

2. **Access Your Pod**
   - **Recommended**: Click "Connect" → "JupyterLab"
   - **Alternative**: Click "Connect" → "Web Terminal"
   - **Advanced**: Click "Connect" → "SSH" (copy command to local terminal)

3. **Install ComfyUI (if not using template)**
   
   **In JupyterLab/Web Terminal/SSH:**
   ```bash
   cd /workspace
   git clone https://github.com/comfyanonymous/ComfyUI.git
   cd ComfyUI
   pip install -r requirements.txt
   ```

4. **Install z_image_turbo Models**
   
   **Method A: Using the Setup Script (Recommended)**
   
   **In JupyterLab:**
   - Upload `setup_comfyui_zimage_runpod.py` to `/workspace/`
   - Open terminal in JupyterLab
   - Run:
   ```bash
   export HF_API_KEY="your_token_here"
   cd /workspace
   python3 setup_comfyui_zimage_runpod.py
   ```
   
   **Method B: Using Inline Script (Alternative)**
   
   **In JupyterLab:**
   - Create new Python notebook
   - Paste and run:
   ```python
   !pip install huggingface_hub -q
   import os
   from huggingface_hub import hf_hub_download, login
   
   HF_API_KEY = os.getenv("HF_API_KEY", "YOUR_TOKEN_HERE")
   COMFYUI_ROOT = "/workspace/ComfyUI"
   
   login(token=HF_API_KEY)
   
   # Create directories
   for d in ["unet", "clip", "vae"]:
       os.makedirs(f"{COMFYUI_ROOT}/models/{d}", exist_ok=True)
   
   # Download files
   hf_hub_download("Comfy-Org/z_image_turbo", "z_image_turbo_bf16.safetensors", 
                   local_dir=f"{COMFYUI_ROOT}/models/unet")
   hf_hub_download("Comfy-Org/z_image_turbo", "split_files/text_encoders/qwen_3_4b.safetensors", 
                   local_dir=f"{COMFYUI_ROOT}/models/clip")
   hf_hub_download("Comfy-Org/z_image_turbo", "split_files/vae/ae.safetensors", 
                   local_dir=f"{COMFYUI_ROOT}/models/vae")
   
   print("✓ Installation complete!")
   ```

5. **Verify Installation**
   
   **In terminal (any method):**
   ```bash
   # Check model files
   ls -lh /workspace/ComfyUI/models/unet/
   ls -lh /workspace/ComfyUI/models/clip/
   ls -lh /workspace/ComfyUI/models/vae/
   
   # Should show:
   # - z_image_turbo_bf16.safetensors (~11.46 GB)
   # - qwen_3_4b.safetensors (~7.49 GB)
   # - ae.safetensors (~0.31 GB)
   ```

6. **Test ComfyUI**
   
   **In terminal (any method):**
   ```bash
   cd /workspace/ComfyUI
   python main.py --listen 0.0.0.0 --port 8188
   ```
   
   - Keep terminal open (ComfyUI needs to keep running)
   - Access via RunPod proxy URL (Dashboard → Pod → Connect → Port 8188)
   - Load workflow and test generation
   - Verify everything works

7. **Save Workflow Files**
   
   **In JupyterLab:**
   - Use file browser to upload `z-image-workflow.json` to `/workspace/ComfyUI/`
   
   **Via SSH:**
   ```bash
   # From your local machine
   scp z-image-workflow.json root@xxxxx.runpod.io:/workspace/ComfyUI/
   ```
   
   **Via Web Terminal:**
   - Use RunPod's file upload feature (if available)
   - Or use `wget`/`curl` to download from URL

### Phase 3: Reusing the Volume (Future Deployments)

**Every time you deploy a new Pod:**

1. **Deploy Pod with Same Network Volume**
   - Pods → Deploy
   - Select **Network Volume** → Choose your existing volume
   - Select GPU type
   - Select template (or use same template)
   - Deploy

2. **Verify Files Are There**
   ```bash
   # Check ComfyUI exists
   ls -la /workspace/ComfyUI
   
   # Check models exist
   ls -lh /workspace/ComfyUI/models/unet/
   ls -lh /workspace/ComfyUI/models/clip/
   ls -lh /workspace/ComfyUI/models/vae/
   ```

3. **Start ComfyUI**
   ```bash
   cd /workspace/ComfyUI
   python main.py --listen 0.0.0.0 --port 8188
   ```

4. **That's It!**
   - Models are already there
   - No re-downloading needed
   - Start generating immediately

---

## Advanced Usage

### Sharing Between Multiple Pods

You can attach the same network volume to multiple Pods simultaneously:

**Use Cases**:
- Test different GPU types with same models
- Run multiple ComfyUI instances
- Share workflows between team members

**Important**: 
- Multiple Pods can **read** from the same volume
- Avoid **writing** to the same files simultaneously (data corruption risk)
- Use separate output directories per Pod if needed

**Example**:
```bash
# Pod 1: Use default output directory
cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8188 --output-directory /workspace/ComfyUI/output/pod1

# Pod 2: Use different output directory
cd /workspace/ComfyUI
python main.py --listen 0.0.0.0 --port 8189 --output-directory /workspace/ComfyUI/output/pod2
```

### Pre-populating Volume (S3 API)

If your volume is in a supported datacenter, you can upload files via S3 API **before** deploying Pods:

**Supported Datacenters**:
- `EUR-IS-1`
- `EU-RO-1`
- `EU-CZ-1`
- `US-KS-2`
- `US-CA-2`

**Benefits**:
- Upload models before launching Pods
- Reduce Pod initialization time
- Manage files without running compute

**Setup** (using AWS CLI):
```bash
# Configure S3 endpoint for your volume
aws configure set s3.endpoint_url https://api.runpod.io/s3

# Upload files
aws s3 cp z_image_turbo_bf16.safetensors s3://your-volume-name/models/unet/
```

### Migrating Between Volumes

If you need to move data to a different volume or datacenter:

**Method 1: Using runpodctl** (Simplest)
```bash
# On source Pod
cd /workspace
runpodctl send *

# Copy the receive command from output
# On destination Pod
cd /workspace
runpodctl receive <command-from-output>
```

**Method 2: Using rsync** (Faster for large transfers)
```bash
# On source Pod
rsync -avzP --inplace -e "ssh -p DEST_PORT" /workspace/ root@DEST_IP:/workspace
```

See [RunPod Migration Guide](https://docs.runpod.io/storage/network-volumes#migrate-files) for detailed steps.

---

## Best Practices

### Directory Structure

Organize your network volume for easy management:

```
/workspace/
├── ComfyUI/                    # ComfyUI installation
│   ├── models/
│   │   ├── unet/              # UNet models
│   │   ├── clip/              # CLIP models
│   │   ├── vae/               # VAE models
│   │   └── checkpoints/       # Other models
│   ├── workflows/             # Saved workflows
│   └── output/                # Generated images
├── scripts/                    # Setup scripts
└── configs/                    # Configuration files
```

### Version Control

- Keep setup scripts on the volume
- Document model versions
- Save workflow files
- Keep notes on configurations

### Backup Strategy

**Important**: Network volumes can be terminated if account lacks funds!

**Backup Options**:
1. **Regular Downloads**: Periodically download important files
2. **Duplicate Volume**: Create backup volume in different datacenter
3. **S3 Backup**: Export to external S3 storage
4. **Git**: Version control for workflows/scripts

### Cost Management

1. **Monitor Usage**: Check volume size regularly
2. **Clean Up**: Remove unused models/outputs
3. **Right-Size**: Don't create volumes larger than needed (can increase, not decrease)
4. **Account Balance**: Keep account funded to prevent termination

---

## Troubleshooting

### Volume Not Attaching

**Issue**: Can't see volume in dropdown during Pod deployment

**Solutions**:
- Verify volume is in same datacenter as Pod
- Check volume exists in Storage page
- Ensure you're using Secure Cloud (required for Pods)

### Files Missing After Deployment

**Issue**: Files not visible in `/workspace`

**Solutions**:
- Verify correct volume was selected
- Check volume mount path (default: `/workspace`)
- Verify files exist: Check Storage page → Volume details
- Try restarting Pod

### Permission Issues

**Issue**: Can't write to volume

**Solutions**:
```bash
# Fix permissions
chmod -R 755 /workspace
chown -R root:root /workspace
```

### Out of Space

**Issue**: Volume full

**Solutions**:
- Increase volume size (can't decrease)
- Clean up unused files
- Move outputs to different location
- Delete old models

---

## Migration from Existing Setup

If you already have ComfyUI running on a Pod **without** a network volume:

### Option 1: Copy to New Volume

1. **Create new network volume** (50-100 GB)
2. **Deploy new Pod** with volume attached
3. **On old Pod**: Create archive
   ```bash
   cd /workspace
   tar -czf comfyui_backup.tar.gz ComfyUI/
   ```
4. **Download archive** from old Pod
5. **Upload to new Pod** (via JupyterLab or SCP)
6. **Extract on new Pod**:
   ```bash
   cd /workspace
   tar -xzf comfyui_backup.tar.gz
   ```

### Option 2: Use runpodctl

1. **Deploy two Pods**:
   - Old Pod (source, no volume)
   - New Pod (destination, with volume)
2. **On source Pod**:
   ```bash
   cd /workspace
   runpodctl send ComfyUI/*
   ```
3. **On destination Pod**:
   ```bash
   cd /workspace
   runpodctl receive <command-from-source>
   ```

---

## Quick Reference

### Create Volume
- **Location**: RunPod Console → Storage → New Network Volume
- **Size**: 50-100 GB recommended
- **Cost**: ~$3.50-7.00/month

### Attach to Pod
- **When**: During Pod deployment (cannot attach later)
- **Mount Point**: `/workspace` (default)
- **Can Share**: Yes, multiple Pods can use same volume

### File Locations
- **ComfyUI**: `/workspace/ComfyUI/`
- **Models**: `/workspace/ComfyUI/models/`
- **Outputs**: `/workspace/ComfyUI/output/`

### Key Commands
```bash
# Check volume usage
du -sh /workspace

# List files
ls -lh /workspace/ComfyUI/models/

# Start ComfyUI
cd /workspace/ComfyUI && python main.py --listen 0.0.0.0 --port 8188
```

---

## Cost-Benefit Analysis

### Without Network Volume
- **Time per deployment**: 30-45 minutes (download models)
- **Bandwidth cost**: Variable
- **Setup effort**: High (repeat each time)

### With Network Volume
- **Time per deployment**: 2-5 minutes (just start ComfyUI)
- **Storage cost**: ~$3.50-7.00/month
- **Setup effort**: Low (one-time setup)

### Break-Even Point
- **If deploying Pods 2-3+ times per month**: Network volume is cost-effective
- **If keeping Pods running long-term**: Network volume saves time
- **If sharing between team**: Network volume is essential

---

## Recommended Workflow

1. **Create 50-100 GB network volume** in preferred datacenter
2. **Deploy initial Pod** with volume attached
3. **Install ComfyUI + z_image_turbo** (one-time setup)
4. **Test and verify** everything works
5. **Terminate Pod** (data persists on volume)
6. **Future deployments**: Just attach same volume and start ComfyUI

---

## Resources

- **RunPod Network Volumes Docs**: https://docs.runpod.io/storage/network-volumes
- **S3-Compatible API**: Available in select datacenters
- **Migration Guide**: See RunPod docs for runpodctl and rsync methods
- **Storage Console**: https://www.runpod.io/console/storage

---

## Summary

**Network volumes are ideal for your ComfyUI + z_image setup because**:

✅ **Persistent**: Models survive Pod termination  
✅ **Cost-Effective**: ~$3.50/month vs. repeated downloads  
✅ **Time-Saving**: No 30-minute download wait  
✅ **Shareable**: Use across multiple Pods  
✅ **Scalable**: Easy to add more models  

**Recommended Action**: Create a 50-100 GB network volume and migrate your ComfyUI setup to it for persistent, reusable storage.

---

**Next Steps**:
1. Create network volume in RunPod console
2. Deploy Pod with volume attached
3. Run setup script to install ComfyUI + z_image
4. Test and verify
5. Use volume for all future Pod deployments

