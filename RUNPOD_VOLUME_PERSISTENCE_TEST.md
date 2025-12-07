# Network Volume Persistence Test - Step by Step

## Overview

This test verifies that your ComfyUI installation and z_image_turbo models persist on the network volume after Pod termination and can be reused in a new Pod.

---

## Pre-Test Checklist

Before starting, note these details:

**Current Pod Information:**
- Pod ID: (Note this from RunPod dashboard)
- Network Volume Name: (Note from Storage page)
- ComfyUI Location: `/workspace/runpod-slim/ComfyUI`
- Models Location: `/workspace/runpod-slim/ComfyUI/models/`

**Verify Files Are There:**
- [ ] UNet: `models/unet/z_image_turbo_bf16.safetensors` (~11.46 GB)
- [ ] CLIP: `models/clip/qwen_3_4b.safetensors` (~7.49 GB)
- [ ] VAE: `models/vae/ae.safetensors` (~0.31 GB)
- [ ] ComfyUI is working and you've generated an image

---

## Step 1: Note Your Network Volume Name

**In RunPod Dashboard:**

1. Go to: https://www.runpod.io/console/storage
2. Find your network volume
3. **Note the exact name** (e.g., `comfyui-models`, `my-comfyui-volume`)
4. **Note the size** (should be 50-100 GB or whatever you created)

**Or in JupyterLab Terminal:**
```bash
# Check what's mounted
df -h /workspace

# This will show your network volume details
```

---

## Step 2: Verify Files Are on Network Volume

**In JupyterLab Terminal (before terminating Pod):**

```bash
# Verify all files exist
cd /workspace/runpod-slim/ComfyUI

echo "=== File Verification ==="
echo ""
echo "UNet:"
ls -lh models/unet/z_image_turbo_bf16.safetensors

echo ""
echo "CLIP:"
ls -lh models/clip/qwen_3_4b.safetensors

echo ""
echo "VAE:"
ls -lh models/vae/ae.safetensors

echo ""
echo "Network Volume Status:"
df -h /workspace

echo ""
echo "Total Model Size:"
du -sh models/unet models/clip models/vae
```

**Expected Output:**
- All three files should exist
- Total size should be ~19.26 GB
- Files should be on `/workspace` (network volume)

---

## Step 3: Stop/Terminate Current Pod

**In RunPod Dashboard:**

1. Go to: https://www.runpod.io/console/pods
2. Find your current Pod
3. Click on the Pod
4. Click **"Stop"** or **"Terminate"** button
   - **Stop**: Pod stops but can be restarted (keeps Pod ID)
   - **Terminate**: Pod is deleted (frees resources, but data on network volume persists)

**For this test, either is fine** - the network volume persists regardless.

5. Wait for Pod to stop/terminate (10-30 seconds)

---

## Step 4: Deploy New Pod with Same Network Volume

**In RunPod Dashboard:**

1. Click **"Deploy"** button
2. **Select Network Volume**:
   - Find "Network Volume" section
   - Select your network volume from dropdown (the one you noted in Step 1)
   - **Important**: Must select the SAME volume!

3. **Select Template**:
   - Search for "ComfyUI" or use template ID: `cw3nka7d08`
   - Or direct link: https://console.runpod.io/hub/template/comfyui?id=cw3nka7d08
   - Select the same template you used before

4. **Select GPU Type**:
   - Choose your preferred GPU (same or different - doesn't matter)

5. **Environment Variables** (if needed):
   - Set `HF_API_KEY` if you want to download more models later
   - Or attach your `huggingface` secret

6. **Deploy**:
   - Click **"Deploy On-Demand"**
   - Wait for Pod to start (2-3 minutes)

---

## Step 5: Access New Pod

**Once Pod is Running:**

1. **Access JupyterLab**:
   - RunPod Dashboard → Your Pod → Connect → **JupyterLab**

2. **Open Terminal**:
   - In JupyterLab: File → New → Terminal

---

## Step 6: Verify Files Are Still There

**In JupyterLab Terminal:**

```bash
# Check network volume is mounted
df -h /workspace

# Find ComfyUI
find /workspace -name "ComfyUI" -type d

# Navigate to ComfyUI
cd /workspace/runpod-slim/ComfyUI

# Verify all model files exist
echo "=== Verifying Files ==="
echo ""

# Check UNet
if [ -f "models/unet/z_image_turbo_bf16.safetensors" ]; then
    size=$(du -h models/unet/z_image_turbo_bf16.safetensors | cut -f1)
    echo "✓ UNet: $size"
else
    echo "✗ UNet: NOT FOUND"
fi

# Check CLIP
if [ -f "models/clip/qwen_3_4b.safetensors" ]; then
    size=$(du -h models/clip/qwen_3_4b.safetensors | cut -f1)
    echo "✓ CLIP: $size"
else
    echo "✗ CLIP: NOT FOUND"
fi

# Check VAE
if [ -f "models/vae/ae.safetensors" ]; then
    size=$(du -h models/vae/ae.safetensors | cut -f1)
    echo "✓ VAE: $size"
else
    echo "✗ VAE: NOT FOUND"
fi

echo ""
echo "Total model directory size:"
du -sh models/unet models/clip models/vae
```

**Expected Result:**
- ✅ All three files should exist
- ✅ File sizes should match (~11.46 GB, ~7.49 GB, ~0.31 GB)
- ✅ Total should be ~19.26 GB

---

## Step 7: Start ComfyUI

**In Terminal:**

```bash
cd /workspace/runpod-slim/ComfyUI

# Start ComfyUI
python3 main.py --listen 0.0.0.0 --port 8188
```

**Keep terminal open** - ComfyUI needs to keep running.

---

## Step 8: Test ComfyUI in Browser

1. **Access ComfyUI**:
   - RunPod Dashboard → Your Pod → Connect → Port **8188**
   - Or use proxy URL: `https://xxxxx-8188.proxy.runpod.net`

2. **Verify Models Are Available**:
   - Add **UNETLoader** node → Should show `z_image_turbo_bf16.safetensors` in dropdown
   - Add **CLIPLoader** node → Should show `qwen_3_4b.safetensors` in dropdown
   - Add **VAELoader** node → Should show `ae.safetensors` in dropdown

3. **Test Generation**:
   - Load your workflow (or create a simple one)
   - Set CLIPLoader type to `qwen_image`
   - Queue a prompt
   - **Generate an image** to verify everything works

---

## Step 9: Verify Success

**If everything works:**

✅ **Network volume persistence confirmed!**

- Files persisted after Pod termination
- ComfyUI works with existing models
- No re-downloading needed
- Setup time: ~2-5 minutes (just start ComfyUI)

**What this means:**
- You can terminate Pods anytime
- Models stay on network volume
- Future deployments are fast
- Cost-effective (no repeated downloads)

---

## Troubleshooting

### Files Not Found

**Issue**: Models don't appear in new Pod

**Solutions**:
1. **Verify correct network volume** was selected during deployment
2. **Check volume name** matches what you noted
3. **Check file locations**:
   ```bash
   find /workspace -name "z_image_turbo_bf16.safetensors"
   find /workspace -name "qwen_3_4b.safetensors"
   find /workspace -name "ae.safetensors"
   ```

### ComfyUI Not Found

**Issue**: Can't find ComfyUI directory

**Solutions**:
```bash
# Search for ComfyUI
find /workspace -name "ComfyUI" -type d

# Check common locations
ls -la /workspace/ComfyUI
ls -la /workspace/runpod-slim/ComfyUI
```

### Models Not Appearing in ComfyUI

**Issue**: Files exist but don't show in dropdown

**Solutions**:
1. **Wait 30-60 seconds** for ComfyUI to rescan
2. **Restart ComfyUI**:
   ```bash
   pkill -f "python.*main.py"
   cd /workspace/runpod-slim/ComfyUI
   python3 main.py --listen 0.0.0.0 --port 8188
   ```
3. **Check file permissions**:
   ```bash
   chmod 644 /workspace/runpod-slim/ComfyUI/models/unet/*.safetensors
   chmod 644 /workspace/runpod-slim/ComfyUI/models/clip/*.safetensors
   chmod 644 /workspace/runpod-slim/ComfyUI/models/vae/*.safetensors
   ```

### Wrong Network Volume

**Issue**: Selected wrong volume during deployment

**Solution**:
- Terminate Pod
- Deploy again with **correct** network volume
- Make sure volume name matches

---

## Success Criteria

**Test is successful if:**

- [ ] New Pod deployed with same network volume
- [ ] All three model files exist (~19.26 GB total)
- [ ] ComfyUI starts successfully
- [ ] Models appear in ComfyUI dropdown menus
- [ ] Image generation works
- [ ] No re-downloading needed

---

## Next Steps After Successful Test

Once you've confirmed persistence:

1. **Document your setup**:
   - Network volume name
   - ComfyUI template ID
   - Model locations

2. **Future deployments**:
   - Always select same network volume
   - Models will be there automatically
   - Just start ComfyUI and generate

3. **Cost savings**:
   - No repeated downloads
   - Fast Pod startup
   - Efficient resource usage

---

## Summary

**This test proves:**
- ✅ Network volumes persist across Pod deployments
- ✅ Your ~20GB of models are safely stored
- ✅ Setup time is minimal for future Pods
- ✅ Cost-effective solution for frequent deployments

**If test succeeds**: You're all set! Your setup is persistent and reusable.

**If test fails**: Check troubleshooting section or verify network volume was selected correctly.

---

**Ready to test?** Follow the steps above to verify your network volume persistence!

