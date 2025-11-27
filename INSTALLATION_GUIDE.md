# Stable Diffusion WebUI - Installation & Configuration Guide

## Current Configuration Overview

### ✅ Installed Models
- **Real-Dreams.safetensors** (2.0 GB) - **CURRENTLY ACTIVE**
- Realistic_Vision_V6.0_NV_B1_fp16.safetensors (2.0 GB)
- dreamshaper_8.safetensors (2.0 GB)
- v1-5-pruned-emaonly.safetensors (4.0 GB)

### ✅ Installed VAE
- **vae-ft-mse-840000-ema-pruned.ckpt** (319 MB) - Currently Active

### ✅ Installed Extensions
- **ADetailer** - Face and hand enhancement extension

### ✅ Launch Configuration
- API Mode: Enabled (`--api`)
- Torch CUDA Test: Skipped (`--skip-torch-cuda-test`)

---

## Quick Start Guide

### 1. Verify Installation

Check that all files are in place:

```bash
# Models should be in:
ls models/Stable-diffusion/

# VAE should be in:
ls models/VAE/

# Extensions should be in:
ls extensions/
```

### 2. Launch WebUI

```bash
# From the stable-diffusion-webui directory:
python launch.py

# Or use the shell script:
./webui.sh

# Or on macOS:
source webui-macos-env.sh
```

The WebUI will be available at: **http://localhost:7860**

### 3. Verify Current Model

In the WebUI:
1. Check the model dropdown at the top - should show "Real-Dreams.safetensors"
2. Go to Settings → Stable Diffusion → SD Model Checkpoint
3. Verify: `Real-Dreams.safetensors [ab51aab984]`
4. Verify VAE: `vae-ft-mse-840000-ema-pruned.ckpt`

---

## Real-Dreams Model Configuration

### Recommended Settings

#### Basic Generation Settings
- **Sampler**: `Euler a` or `DPM++ 2M Karras` (recommended)
- **Sampling Steps**: 20-30 steps
  - Quick tests: 20 steps
  - Quality: 25-30 steps
  - High quality: 30-40 steps
- **CFG Scale**: 7.0-9.0
  - Default: 7.5-8.0
  - More creative: 6.0-7.0
  - Stronger adherence: 8.0-9.0

#### Resolution Settings
- **Base Resolution**: 512x512 or 768x768
- **Portrait**: 512x768 or 768x1024
- **Landscape**: 768x512 or 1024x768
- **Square**: 512x512, 768x768, 1024x1024

#### High-Resolution Fix (Hires.Fix)
- **Enable**: Yes (recommended for final outputs)
- **Upscale by**: 1.5-2.0x
- **Denoising strength**: 0.3-0.5
- **Upscaler**: 
  - `4x-UltraSharp` (best detail)
  - `R-ESRGAN 4x+` (good general purpose)
  - `Latent` (fastest)
- **Hires steps**: 10-20 steps

#### Prompt Engineering

**Positive Prompt Structure:**
```
masterpiece, best quality, highly detailed, 8k, uhd, 
[your detailed description], 
photorealistic, sharp focus, professional photography
```

**Recommended Negative Prompt:**
```
lowres, bad anatomy, bad hands, text, error, missing fingers, 
extra digit, fewer digits, cropped, worst quality, low quality, 
normal quality, jpeg artifacts, signature, watermark, username, 
blurry, bad feet, bad proportions, gross proportions, 
deformed, ugly, mutilated, disfigured, extra limbs, 
cloned face, bad eyes, bad face, mutation
```

### ADetailer Configuration (Face Enhancement)

ADetailer is already installed. To configure:

1. Scroll down in txt2img/img2img tabs
2. Find "ADetailer" section
3. Enable ADetailer checkbox

**Recommended ADetailer Settings:**
- **Model**: `face_yolov8n.pt` (auto-downloads on first use)
- **Detection confidence**: 0.3
- **Denoising strength**: 0.35-0.4
- **Steps**: 25-30
- **CFG Scale**: 7.0-8.0
- **Sampler**: `DPM++ SDE Karras` or match main sampler
- **Prompt**: (leave empty to use main prompt)
- **Negative prompt**: `blurry face, deformed face, bad eyes, bad anatomy`

---

## Switching Between Models

### Via WebUI Interface

1. Click the model dropdown at the top (next to "Generate" button)
2. Select desired model:
   - `Real-Dreams.safetensors` (current)
   - `Realistic_Vision_V6.0_NV_B1_fp16.safetensors`
   - `dreamshaper_8.safetensors`
   - `v1-5-pruned-emaonly.safetensors`
3. Wait for model to load (check console for progress)

### Via Settings (Persistent)

1. Go to Settings tab → Stable Diffusion
2. Under "SD Model Checkpoint", select your model
3. Click "Apply settings"
4. Click "Reload UI" (optional)

### Via API

```bash
# Set Real-Dreams model
curl -X POST http://localhost:7860/sdapi/v1/options \
  -H "Content-Type: application/json" \
  -d '{"sd_model_checkpoint": "Real-Dreams.safetensors"}'

# Set Realistic Vision model
curl -X POST http://localhost:7860/sdapi/v1/options \
  -H "Content-Type: application/json" \
  -d '{"sd_model_checkpoint": "Realistic_Vision_V6.0_NV_B1_fp16.safetensors"}'
```

### Via Config File (Persistent)

Edit `config.json`:
```json
{
  "sd_model_checkpoint": "Real-Dreams.safetensors",
  "sd_vae": "vae-ft-mse-840000-ema-pruned.ckpt"
}
```

---

## Enhanced API Wrapper (Recommended)

For easier API usage with model selection and ADetailer control, use the Enhanced API Wrapper:

### Setup Enhanced API Wrapper

1. **Install dependencies**:
   ```bash
   pip install requests fastapi uvicorn
   ```

2. **Start the wrapper** (in a separate terminal):
   ```bash
   python enhanced_api_wrapper.py
   ```
   Wrapper runs on: `http://localhost:8080`

3. **Use simplified API**:
   ```bash
   curl -X POST http://localhost:8080/generate \
     -H "Content-Type: application/json" \
     -d '{
       "prompt": "masterpiece, best quality, a beautiful portrait",
       "model": "real-dreams",
       "adetailer": {"enabled": true}
     }'
   ```

### Benefits of Enhanced API Wrapper

- **Easy Model Selection**: Just specify `"model": "real-dreams"` instead of full filename
- **Simple ADetailer Control**: `"adetailer": {"enabled": true}` instead of complex args array
- **Preset Configurations**: Optimal settings automatically applied per model
- **Cleaner API**: Simplified request format
- **Type Safety**: Automatic validation

See `ENHANCED_API_GUIDE.md` for full documentation and examples.

---

## Direct WebUI API Usage

### Check Current Configuration

```bash
# Check current model
curl http://localhost:7860/sdapi/v1/options | grep sd_model_checkpoint

# Check current VAE
curl http://localhost:7860/sdapi/v1/options | grep sd_vae

# Full options
curl http://localhost:7860/sdapi/v1/options
```

### Generate Image via API

```bash
curl -X POST http://localhost:7860/sdapi/v1/txt2img \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "masterpiece, best quality, highly detailed, 8k, a beautiful portrait, photorealistic",
    "negative_prompt": "lowres, bad anatomy, bad hands, text, error, worst quality, low quality",
    "steps": 25,
    "sampler_name": "Euler a",
    "cfg_scale": 7.5,
    "width": 512,
    "height": 768,
    "enable_hr": true,
    "hr_scale": 1.5,
    "hr_upscaler": "4x-UltraSharp",
    "hr_second_pass_steps": 15,
    "denoising_strength": 0.4
  }'
```

### API with ADetailer

```bash
curl -X POST http://localhost:7860/sdapi/v1/txt2img \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "masterpiece, best quality, highly detailed, 8k, a beautiful portrait, photorealistic",
    "negative_prompt": "lowres, bad anatomy, bad hands, text, error, worst quality, low quality",
    "steps": 25,
    "sampler_name": "Euler a",
    "cfg_scale": 7.5,
    "width": 512,
    "height": 768,
    "alwayson_scripts": {
      "ADetailer": {
        "args": [
          true,
          "face_yolov8n.pt",
          0.3,
          4,
          4,
          true,
          32,
          0.4,
          7.5,
          28,
          "DPM++ SDE Karras",
          "",
          "blurry face, deformed",
          1,
          null
        ]
      }
    }
  }'
```

---

## Model-Specific Recommendations

### Real-Dreams (Current)
- **Best for**: Photorealistic portraits, artistic images
- **CFG Scale**: 7.5-8.0
- **Sampler**: Euler a or DPM++ 2M Karras
- **VAE**: vae-ft-mse-840000-ema-pruned.ckpt (current)

### Realistic Vision V6.0
- **Best for**: Ultra-realistic portraits, photography-style
- **CFG Scale**: 6.5-7.5
- **Sampler**: DPM++ SDE Karras (25+ steps) or DPM++ 2M SDE (50+ steps)
- **VAE**: vae-ft-mse-840000-ema-pruned.ckpt (current)
- **Resolution**: 896x896, 768x1024

### DreamShaper 8
- **Best for**: Artistic, creative, versatile
- **CFG Scale**: 7.0-8.0
- **Sampler**: Euler a or DPM++ 2M Karras
- **VAE**: vae-ft-mse-840000-ema-pruned.ckpt (current)

---

## Workflow Recommendations

### Quick Test Workflow
1. Set resolution: 512x768
2. Steps: 25, CFG: 7.5, Sampler: Euler a
3. Generate test image
4. If composition good, enable Hires.Fix (1.5x, denoising 0.4)
5. Enable ADetailer if face needs work

### Production Workflow
1. Generate base at 768x1024, 30 steps, CFG 7.5-8.0, DPM++ 2M Karras
2. Enable Hires.Fix: 2.0x, 4x-UltraSharp, denoising 0.4, 20 steps
3. Enable ADetailer: Face enhancement (face_yolov8n.pt)
4. Generate batch of 4-8 variations
5. Pick best and refine if needed

---

## Troubleshooting

### Model Not Loading
- **Check file location**: `models/Stable-diffusion/Real-Dreams.safetensors`
- **Check file size**: Should be ~2.0 GB
- **Check console**: Look for error messages
- **Try reloading**: Settings → Reload UI

### Out of Memory (OOM)
- Reduce resolution: Use 512x512 instead of 768x768
- Enable attention slicing: Settings → Optimizations
- Reduce batch size: Set to 1
- Use `--medvram` flag: Edit `webui-user.sh`:
  ```bash
  export COMMANDLINE_ARGS="--api --skip-torch-cuda-test --medvram"
  ```

### ADetailer Not Working
- Check extension is installed: `extensions/adetailer/`
- Restart WebUI after installation
- Check console for error messages
- Verify model downloads: `extensions/adetailer/models/`

### API Not Responding
- Verify WebUI is running: Check `http://localhost:7860`
- Check API is enabled: `--api` flag in launch args
- Check firewall settings
- Verify port 7860 is not in use

### Poor Quality Results
- Increase steps: Try 30-40 steps
- Use better sampler: DPM++ 2M Karras or DPM++ SDE Karras
- Enable Hires.Fix: 1.5-2.0x upscale
- Improve prompts: Add quality tags, be more specific
- Use ADetailer: For face/hand enhancement
- Check VAE: Ensure correct VAE is loaded

### Wrong Colors
- Check VAE: Ensure `vae-ft-mse-840000-ema-pruned.ckpt` is loaded
- Try different VAE: Settings → Stable Diffusion → SD VAE
- Adjust prompt: Add color-specific terms

---

## File Structure

```
stable-diffusion-webui/
├── models/
│   ├── Stable-diffusion/          # Model checkpoints (.safetensors)
│   │   ├── Real-Dreams.safetensors
│   │   ├── Realistic_Vision_V6.0_NV_B1_fp16.safetensors
│   │   ├── dreamshaper_8.safetensors
│   │   └── v1-5-pruned-emaonly.safetensors
│   └── VAE/                      # VAE files
│       └── vae-ft-mse-840000-ema-pruned.ckpt
├── extensions/                   # Extensions
│   └── adetailer/               # ADetailer extension
├── config.json                   # Main configuration file
├── webui-user.sh                 # Launch configuration
└── launch.py                     # Launch script
```

---

## Launch Arguments Reference

Current launch arguments (in `webui-user.sh`):
```bash
export COMMANDLINE_ARGS="--api --skip-torch-cuda-test"
```

### Common Launch Arguments

- `--api` - Enable API mode
- `--listen` - Listen on all network interfaces (not just localhost)
- `--port 7860` - Set port (default: 7860)
- `--medvram` - Optimize for medium VRAM (4-6GB)
- `--lowvram` - Optimize for low VRAM (<4GB)
- `--xformers` - Use xformers for memory optimization
- `--skip-torch-cuda-test` - Skip CUDA test on startup
- `--no-half` - Disable half precision (if having issues)
- `--precision full` - Use full precision

### Example: Full Launch Arguments

```bash
export COMMANDLINE_ARGS="--api --listen --port 7860 --medvram --xformers"
```

---

## Verification Checklist

- [ ] Real-Dreams.safetensors is in `models/Stable-diffusion/`
- [ ] VAE file is in `models/VAE/`
- [ ] ADetailer extension is in `extensions/adetailer/`
- [ ] WebUI launches successfully
- [ ] Model loads in WebUI dropdown
- [ ] VAE is selected in Settings
- [ ] API responds at `http://localhost:7860`
- [ ] Can generate images successfully
- [ ] ADetailer works (if tested)

---

## Additional Resources

- **WebUI Documentation**: Check `README.md` in repository
- **Model Notes**: See `notes.txt` for detailed model configurations
- **API Documentation**: Visit `http://localhost:7860/docs` when WebUI is running
- **Community**: AUTOMATIC1111 WebUI GitHub Issues

---

## Quick Reference Commands

```bash
# Launch WebUI
python launch.py

# Check current model via API
curl http://localhost:7860/sdapi/v1/options | grep sd_model_checkpoint

# Set model via API
curl -X POST http://localhost:7860/sdapi/v1/options \
  -H "Content-Type: application/json" \
  -d '{"sd_model_checkpoint": "Real-Dreams.safetensors"}'

# Generate image
curl -X POST http://localhost:7860/sdapi/v1/txt2img \
  -H "Content-Type: application/json" \
  -d '{"prompt": "your prompt", "steps": 25, "cfg_scale": 7.5}'
```

---

**Last Updated**: Based on current configuration as of installation
**Current Active Model**: Real-Dreams.safetensors
**Current Active VAE**: vae-ft-mse-840000-ema-pruned.ckpt

