# Modern Model Compatibility Guide

## Overview

This document covers modern NSFW and general AI image generation models and their compatibility with Stable Diffusion WebUI.

---

## ✅ Supported Model Formats

Your current WebUI installation supports:

### 1. **Stable Diffusion 1.x (SD1)**
- **Format**: `.safetensors` or `.ckpt`
- **Status**: ✅ Fully Supported
- **Examples**: Real-Dreams, DreamShaper, Deliberate v3, Realistic Vision
- **NSFW Support**: ✅ Yes (model-dependent)
- **Resolution**: 512x512 base, up to 1024x1024

### 2. **Stable Diffusion 2.x (SD2)**
- **Format**: `.safetensors` or `.ckpt`
- **Status**: ✅ Fully Supported
- **NSFW Support**: ⚠️ Limited (SD 2.0+ has NSFW filters)
- **Resolution**: 512x512, 768x768 base
- **Note**: SD 2.0+ intentionally restricts NSFW content generation

### 3. **Stable Diffusion XL (SDXL)**
- **Format**: `.safetensors` or `.ckpt`
- **Status**: ✅ Fully Supported
- **NSFW Support**: ✅ Yes (model-dependent)
- **Resolution**: 1024x1024 base, up to 2048x2048
- **Examples**: SDXL Base, SDXL Turbo, various fine-tuned SDXL models
- **Note**: Requires more VRAM (8GB+ recommended)

### 4. **Stable Diffusion 3 (SD3)**
- **Format**: `.safetensors`
- **Status**: ✅ Supported (newer WebUI versions)
- **NSFW Support**: ⚠️ Limited (has safety filters)
- **Resolution**: Various, typically 1024x1024+
- **Note**: Requires significant VRAM (12GB+ recommended)
- **Architecture**: Different from SD1/SD2/SDXL

### 5. **SSD (Stable Diffusion XL variant)**
- **Format**: `.safetensors` or `.ckpt`
- **Status**: ✅ Supported
- **NSFW Support**: ✅ Yes (model-dependent)
- **Note**: SDXL variant with different architecture

---

## ❌ NOT Supported Model Formats

### 1. **Flux Models** (Black Forest Labs)
- **Status**: ❌ NOT Supported
- **Reason**: Completely different architecture
- **Format**: Diffusers format (not compatible with WebUI checkpoints)
- **NSFW Support**: Model-dependent (some Flux models support NSFW)
- **Alternatives**:
  - Use **ComfyUI** (has Flux support)
  - Use **InvokeAI** (has Flux support)
  - Use **Diffusers library directly** (Python)
  - Use **Flux WebUI** (separate application)

**Popular Flux Models:**
- Flux.1-dev (base)
- Flux.1-schnell (fast)
- Flux.1-pro (professional)
- Various fine-tuned Flux models

**Why Not Supported:**
- Flux uses a different transformer architecture
- Different latent space dimensions
- Different conditioning mechanisms
- Requires different inference pipeline

### 2. **SD 3.5 / SD 3.5 Medium**
- **Status**: ⚠️ Limited Support (may work but not officially supported)
- **Reason**: Very new, compatibility varies
- **Note**: May require WebUI updates

### 3. **Other Proprietary Formats**
- **Status**: ❌ Not Supported
- **Examples**: Some proprietary model formats from various vendors

---

## Modern NSFW Models by Format

### SDXL NSFW Models (✅ Supported)
- **Juggernaut XL** - Popular NSFW SDXL model
- **RealVisXL** - Realistic NSFW SDXL
- **DreamShaper XL** - Artistic NSFW SDXL
- **Various fine-tuned SDXL models** on CivitAI

**Download**: Search CivitAI for "SDXL NSFW" or specific model names

### SD 1.5 NSFW Models (✅ Supported)
- **Real-Dreams** - Currently installed ✅
- **Realistic Vision** - Currently installed ✅
- **DreamShaper** - Currently installed ✅
- **Deliberate v3** - Versatile NSFW ✅
- **AbyssOrangeMix2** - Anime-style NSFW ✅
- **Many others** on CivitAI

### SD 3 NSFW Models (⚠️ Limited)
- **Status**: SD 3 has built-in safety filters
- **Workaround**: Some fine-tuned SD 3 models may bypass filters
- **Note**: Limited availability due to safety restrictions

### Flux NSFW Models (❌ Not Supported in WebUI)
- **Flux.1-dev fine-tuned models** - Various NSFW fine-tunes exist
- **Status**: Must use ComfyUI, InvokeAI, or Flux WebUI
- **Note**: Flux models generally produce high-quality results

---

## Compatibility Matrix

| Model Format | WebUI Support | NSFW Support | VRAM Required | Notes |
|-------------|---------------|--------------|---------------|-------|
| SD 1.x | ✅ Yes | ✅ Yes | 4-6 GB | Best compatibility |
| SD 2.x | ✅ Yes | ⚠️ Limited | 4-6 GB | Has NSFW filters |
| SDXL | ✅ Yes | ✅ Yes | 8-12 GB | High quality |
| SD 3 | ✅ Yes | ⚠️ Limited | 12+ GB | Safety filters |
| SSD | ✅ Yes | ✅ Yes | 8-12 GB | SDXL variant |
| Flux | ❌ No | ✅ Yes* | 12+ GB | Different architecture |

*NSFW support depends on specific Flux model

---

## How to Use Flux Models (Alternative Methods)

### Option 1: ComfyUI
```bash
# Install ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip install -r requirements.txt

# Download Flux models
# Place in: models/checkpoints/
# Use ComfyUI's node-based interface
```

### Option 2: InvokeAI
```bash
# Install InvokeAI
pip install invokeai
invokeai-configure

# Download Flux models via InvokeAI interface
```

### Option 3: Flux WebUI
```bash
# Separate WebUI specifically for Flux
# Search GitHub for "flux-webui" or similar projects
```

### Option 4: Diffusers Library (Python)
```python
from diffusers import DiffusionPipeline
import torch

pipe = DiffusionPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.float16
)
pipe = pipe.to("cuda")

image = pipe("your prompt").images[0]
```

---

## Recommendations

### For NSFW Content Generation

**Best Options (WebUI Compatible):**
1. **SDXL Models** - Highest quality, good NSFW support
   - Examples: Juggernaut XL, RealVisXL
   - Requires: 8GB+ VRAM

2. **SD 1.5 Models** - Best compatibility, wide selection
   - Examples: Real-Dreams (current), Realistic Vision, DreamShaper
   - Requires: 4-6GB VRAM
   - **Current setup is optimal for this**

3. **Fine-tuned SDXL** - Best of both worlds
   - Many NSFW fine-tunes available
   - High quality with good compatibility

**Not Recommended:**
- SD 2.x for NSFW (has filters)
- SD 3 for NSFW (has safety filters)
- Flux in WebUI (not supported)

### For Maximum Quality (Outside WebUI)

If you need Flux-level quality:
- Use **ComfyUI** with Flux models
- Use **InvokeAI** with Flux models
- Use **Diffusers library** directly

---

## Checking Model Compatibility

### Before Downloading a Model:

1. **Check Format**:
   - ✅ `.safetensors` - Safe and recommended
   - ✅ `.ckpt` - Works but less secure
   - ❌ `.pt` (PickleTensor) - Deprecated, avoid
   - ❌ Diffusers-only - Won't work in WebUI

2. **Check Base Model**:
   - SD 1.5 ✅
   - SD 2.x ✅ (but limited NSFW)
   - SDXL ✅
   - SD 3 ✅ (but limited NSFW)
   - Flux ❌

3. **Check File Size**:
   - SD 1.5: ~2-4 GB
   - SDXL: ~6-7 GB
   - SD 3: ~10+ GB
   - Flux: ~24+ GB (different format)

### Verify in WebUI:

1. Place model in `models/Stable-diffusion/`
2. Restart WebUI
3. Check model appears in dropdown
4. Try loading - if it loads, it's compatible

---

## Future-Proofing

### Models Likely to Gain Support:
- **SD 3.5** - May get better support in future WebUI updates
- **SD 4** (if released) - Will likely be supported

### Models Unlikely to Gain Support:
- **Flux** - Different architecture, would require major rewrite
- **Proprietary formats** - Licensing/technical barriers

### Recommendations:
- Stick with SD 1.5 and SDXL for best compatibility
- Use ComfyUI/InvokeAI for Flux if needed
- Keep WebUI updated for latest SD 3 support

---

## Troubleshooting

### Model Won't Load:
1. **Check format**: Must be `.safetensors` or `.ckpt`
2. **Check base model**: Must be SD 1.5, SD 2.x, SDXL, or SD 3
3. **Check file size**: Should match expected size for model type
4. **Check VRAM**: May need more VRAM for larger models
5. **Check WebUI version**: Update if using SD 3 models

### Model Loads But Produces Errors:
1. **Check config file**: WebUI should auto-detect, but may need manual config
2. **Check VAE**: Some models need specific VAE
3. **Check resolution**: Use recommended resolution for model
4. **Check sampler**: Some models work better with specific samplers

### NSFW Content Not Generating:
1. **Check model**: Some models have built-in filters
2. **Check prompt**: May need specific prompt engineering
3. **Check WebUI settings**: Some settings may filter content
4. **Try different model**: Use known NSFW-friendly models

---

## Resources

### Model Repositories:
- **CivitAI**: https://civitai.com (largest collection)
- **Hugging Face**: https://huggingface.co (official models)
- **Stability AI**: https://stability.ai (official SD models)

### Alternative Tools:
- **ComfyUI**: https://github.com/comfyanonymous/ComfyUI
- **InvokeAI**: https://github.com/invoke-ai/InvokeAI
- **Flux WebUI**: Search GitHub for flux-webui projects

### Documentation:
- **WebUI GitHub**: https://github.com/AUTOMATIC1111/stable-diffusion-webui
- **Flux Documentation**: https://github.com/black-forest-labs/flux-dev

---

## Summary

**Your Current Setup:**
- ✅ SD 1.5 models (Real-Dreams, Realistic Vision, DreamShaper)
- ✅ Good NSFW support
- ✅ Optimal VRAM usage
- ✅ Best compatibility

**For Modern High-Quality NSFW:**
- Use SDXL models (require more VRAM)
- Use ComfyUI/InvokeAI for Flux models
- Stick with SD 1.5 for best compatibility

**Not Supported:**
- Flux models (use ComfyUI/InvokeAI instead)
- Some proprietary formats
- Very new experimental formats

---

**Last Updated**: Based on current WebUI capabilities and model availability

