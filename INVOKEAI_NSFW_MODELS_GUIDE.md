# InvokeAI NSFW Models Guide

## Overview

This guide covers finding, downloading, and installing modern NSFW models for InvokeAI, including Flux models and SDXL models that aren't supported in Stable Diffusion WebUI.

---

## Table of Contents

1. [Where to Find NSFW Models](#where-to-find-nsfw-models)
2. [Flux NSFW Models](#flux-nsfw-models)
3. [SDXL NSFW Models](#sdxl-nsfw-models)
4. [Download Methods](#download-methods)
5. [Installation Steps](#installation-steps)
6. [Model Recommendations](#model-recommendations)
7. [Verification & Testing](#verification--testing)
8. [Troubleshooting](#troubleshooting)

---

## Where to Find NSFW Models

### 1. Hugging Face (Official Models)

**URL**: https://huggingface.co

**Official Flux Models**:
- **Flux.1-dev**: https://huggingface.co/black-forest-labs/FLUX.1-dev
- **Flux.1-schnell**: https://huggingface.co/black-forest-labs/FLUX.1-schnell
- **Flux.1-pro**: https://huggingface.co/black-forest-labs/FLUX.1-pro (if available)

**How to Search**:
1. Go to https://huggingface.co/models
2. Search for: `flux` or `flux-dev` or `flux-schnell`
3. Filter by: "Text-to-Image" or "Diffusion"
4. Look for fine-tuned models (check descriptions for NSFW capability)

**Fine-tuned Flux Models**:
- Search: `flux nsfw` or `flux adult` or `flux uncensored`
- Check model descriptions and tags
- Verify compatibility with InvokeAI

### 2. CivitAI (Community Models)

**URL**: https://civitai.com

**Search Strategies**:
1. **For Flux Models**:
   - Search: `flux`
   - Filter: "Checkpoint" or "Model"
   - Sort by: "Most Downloaded" or "Highest Rated"
   - Check tags: Look for NSFW-related tags

2. **For SDXL Models**:
   - Search: `sdxl nsfw` or `sdxl uncensored`
   - Filter: "Checkpoint"
   - Popular tags: `nsfw`, `adult`, `uncensored`, `explicit`

3. **Browse Categories**:
   - Go to Models → Browse
   - Filter by: Base Model (SDXL, Flux if available)
   - Filter by: Tags (NSFW-related)

**Popular NSFW Model Creators**:
- Check "Most Downloaded" section
- Look for verified creators
- Read reviews and comments

### 3. InvokeAI Model Library

**Built-in Access**:
- InvokeAI has a built-in model browser
- Access via: `invokeai --list-models` or web UI
- Some models can be downloaded directly

---

## Flux NSFW Models

### Official Flux Models (Base)

**Flux.1-dev** (Recommended for Quality)
- **URL**: https://huggingface.co/black-forest-labs/FLUX.1-dev
- **Size**: ~24 GB
- **Format**: Diffusers
- **NSFW Support**: ✅ Yes (no built-in filters)
- **Quality**: Highest
- **Speed**: Slower

**Flux.1-schnell** (Recommended for Speed)
- **URL**: https://huggingface.co/black-forest-labs/FLUX.1-schnell
- **Size**: ~24 GB
- **Format**: Diffusers
- **NSFW Support**: ✅ Yes
- **Quality**: High (slightly lower than dev)
- **Speed**: Much faster

**Flux.1-pro** (If Available)
- **URL**: Check Hugging Face
- **Size**: ~24+ GB
- **Format**: Diffusers
- **NSFW Support**: ✅ Yes
- **Quality**: Professional grade

### Fine-tuned Flux Models

**Finding Fine-tuned Flux Models**:

1. **Hugging Face**:
   - Search: `flux fine-tuned` or `flux nsfw`
   - Look for models with high download counts
   - Check model cards for NSFW capability

2. **CivitAI**:
   - Search: `flux`
   - Filter by: "Checkpoint" or "Model"
   - Check model descriptions

**Popular Fine-tuned Flux Models** (Examples - verify availability):
- Various community fine-tunes
- Check CivitAI "Most Downloaded" section
- Look for models with good reviews

---

## SDXL NSFW Models

### Popular SDXL NSFW Models

**Juggernaut XL** (Highly Recommended)
- **CivitAI**: Search "Juggernaut XL"
- **Format**: `.safetensors` or `.ckpt`
- **NSFW Support**: ✅ Excellent
- **Quality**: Very High
- **Size**: ~6-7 GB
- **Compatibility**: ✅ InvokeAI compatible

**RealVisXL** (Realistic)
- **CivitAI**: Search "RealVisXL"
- **Format**: `.safetensors`
- **NSFW Support**: ✅ Excellent
- **Quality**: Photorealistic
- **Size**: ~6-7 GB

**DreamShaper XL**
- **CivitAI**: Search "DreamShaper XL"
- **Format**: `.safetensors`
- **NSFW Support**: ✅ Good
- **Quality**: Artistic/Realistic blend
- **Size**: ~6-7 GB

**Other Popular SDXL NSFW Models**:
- Search CivitAI for: `sdxl nsfw`, `sdxl uncensored`
- Check "Most Downloaded" section
- Read model descriptions and reviews

---

## Download Methods

### Method 1: Via InvokeAI Configuration Wizard

**During Initial Setup**:
```bash
invokeai-configure
```

**Options**:
- Select models to download during configuration
- Choose Flux.1-dev or Flux.1-schnell
- Choose SDXL base models
- Models download automatically

**After Setup**:
```bash
# Download Flux.1-dev
invokeai --download-models flux-dev

# Download Flux.1-schnell
invokeai --download-models flux-schnell

# Download SDXL
invokeai --download-models sdxl
```

### Method 2: Hugging Face (Official Flux Models)

**Using Hugging Face CLI**:

```bash
# Install Hugging Face CLI (if not installed)
pip install huggingface_hub

# Login (optional, for gated models)
huggingface-cli login

# Download Flux.1-dev
huggingface-cli download black-forest-labs/FLUX.1-dev \
  --local-dir ~/invokeai/models/checkpoints/flux-dev

# Download Flux.1-schnell
huggingface-cli download black-forest-labs/FLUX.1-schnell \
  --local-dir ~/invokeai/models/checkpoints/flux-schnell
```

**Using Git LFS**:

```bash
# Install Git LFS (if not installed)
# macOS: brew install git-lfs
# Linux: sudo apt-get install git-lfs

git lfs install

# Clone Flux.1-dev repository
cd ~/invokeai/models/checkpoints
git clone https://huggingface.co/black-forest-labs/FLUX.1-dev
```

**Manual Download**:

1. Visit: https://huggingface.co/black-forest-labs/FLUX.1-dev
2. Click "Files and versions"
3. Download files manually (large, ~24 GB)
4. Place in: `~/invokeai/models/checkpoints/flux-dev/`

### Method 3: CivitAI (Community Models)

**Download Steps**:

1. **Find Model**:
   - Go to https://civitai.com
   - Search for model name
   - Click on model page

2. **Check Format**:
   - Look for "SafeTensor" or "PickleTensor" format
   - **Prefer SafeTensor** (safer, modern format)
   - Avoid PickleTensor if possible

3. **Download**:
   - Click "Download" button
   - Select format: SafeTensor (if available)
   - Select size: Full (recommended) or fp16 (smaller)
   - Wait for download (may require login)

4. **Save Location**:
   - Save to: `~/invokeai/models/checkpoints/`
   - Or custom path configured in InvokeAI

**Direct Download Link** (if available):
```bash
# Example (replace with actual model URL)
wget "https://civitai.com/api/download/models/[MODEL_ID]?type=Model&format=SafeTensor" \
  -O ~/invokeai/models/checkpoints/model-name.safetensors
```

**Note**: CivitAI API may require authentication. Check CivitAI documentation.

### Method 4: Using InvokeAI Web UI

1. Launch InvokeAI: `invokeai --web`
2. Open browser: http://localhost:9090
3. Navigate to Models section
4. Browse available models
5. Click "Download" for desired models
6. Models download automatically

---

## Installation Steps

### Step 1: Locate InvokeAI Models Directory

**Default Location**:
```bash
~/invokeai/models/checkpoints/
```

**Custom Location**:
- Check configuration: `~/.invokeai/invokeai.yaml`
- Look for `paths.models_dir` setting

**Find Current Location**:
```bash
invokeai --list-models
# Shows model paths
```

### Step 2: Install Flux Models

**For Diffusers Format (Flux)**:

```bash
# Create directory for Flux model
mkdir -p ~/invokeai/models/checkpoints/flux-dev

# Download using Hugging Face CLI
huggingface-cli download black-forest-labs/FLUX.1-dev \
  --local-dir ~/invokeai/models/checkpoints/flux-dev

# Or use git clone
cd ~/invokeai/models/checkpoints
git clone https://huggingface.co/black-forest-labs/FLUX.1-dev
```

**Verify Installation**:
```bash
ls -lh ~/invokeai/models/checkpoints/flux-dev/
# Should show model files
```

### Step 3: Install SDXL Models

**For Safetensors Format (SDXL)**:

```bash
# Download model file
# (from CivitAI or other source)
# Save to:
~/invokeai/models/checkpoints/model-name.safetensors

# Or place in subdirectory:
mkdir -p ~/invokeai/models/checkpoints/sdxl-models
# Place .safetensors file there
```

**Example: Downloading Juggernaut XL**:

```bash
# 1. Download from CivitAI (manual or via API)
# 2. Save file as: juggernaut-xl.safetensors
# 3. Move to InvokeAI directory:
mv juggernaut-xl.safetensors ~/invokeai/models/checkpoints/
```

### Step 4: Refresh Model List

**After Installing Models**:

```bash
# Restart InvokeAI to detect new models
# Or use command:
invokeai --list-models

# Should show newly installed models
```

**Via Web UI**:
1. Launch InvokeAI: `invokeai --web`
2. Go to Models section
3. Click "Refresh" or restart InvokeAI
4. New models should appear

### Step 5: Set Default Model (Optional)

**Edit Configuration**:
```bash
# Edit config file
nano ~/.invokeai/invokeai.yaml

# Or use InvokeAI command:
invokeai --configure
```

**Set Default Model**:
```yaml
InvokeAI:
  model: flux-dev  # or your preferred model name
```

---

## Model Recommendations

### For Maximum Quality (Flux)

**Recommended**: Flux.1-dev
- **Quality**: Highest
- **NSFW**: ✅ Excellent support
- **Speed**: Slower (but worth it)
- **VRAM**: 12GB+ recommended
- **Use Case**: Final production images

**Alternative**: Flux.1-schnell
- **Quality**: Very High (slightly lower)
- **NSFW**: ✅ Excellent support
- **Speed**: Much faster
- **VRAM**: 12GB+ recommended
- **Use Case**: Quick generation, testing

### For Best Compatibility (SDXL)

**Recommended**: Juggernaut XL
- **Quality**: Very High
- **NSFW**: ✅ Excellent support
- **Compatibility**: ✅ Works in both WebUI and InvokeAI
- **VRAM**: 8GB+ recommended
- **Use Case**: Versatile, widely supported

**Alternative**: RealVisXL
- **Quality**: Photorealistic
- **NSFW**: ✅ Excellent support
- **Compatibility**: ✅ Good
- **VRAM**: 8GB+ recommended
- **Use Case**: Realistic portraits

### For Lower VRAM (SDXL)

**Recommended**: SDXL Base + Fine-tunes
- **Quality**: High
- **NSFW**: ✅ Good (model-dependent)
- **VRAM**: 6-8GB
- **Use Case**: Limited VRAM systems

---

## Verification & Testing

### Check Installed Models

```bash
# List all models
invokeai --list-models

# Should show:
# - flux-dev (if installed)
# - flux-schnell (if installed)
# - sdxl models (if installed)
# - Custom models
```

### Test Model Loading

**Via Command Line**:
```bash
# Test Flux model
invokeai "test prompt" --model flux-dev

# Test SDXL model
invokeai "test prompt" --model juggernaut-xl
```

**Via Web UI**:
1. Launch: `invokeai --web`
2. Select model from dropdown
3. Enter test prompt
4. Generate image
5. Verify model loads and generates

### Test NSFW Generation

**Test Prompt** (adjust as needed):
```
masterpiece, best quality, highly detailed, 8k, [your NSFW description]
```

**Verify**:
- Model loads without errors
- Generation completes successfully
- Output matches expected quality
- No safety filters blocking content

---

## Troubleshooting

### Model Not Appearing

**Problem**: Model doesn't show in list

**Solutions**:
```bash
# 1. Check file location
ls -lh ~/invokeai/models/checkpoints/

# 2. Verify file format
# Flux: Should be Diffusers format (directory with files)
# SDXL: Should be .safetensors or .ckpt file

# 3. Check file permissions
chmod 644 ~/invokeai/models/checkpoints/*

# 4. Refresh model list
invokeai --list-models

# 5. Restart InvokeAI
```

### Model Won't Load

**Problem**: Error loading model

**Solutions**:
```bash
# 1. Check VRAM
# Flux models need 12GB+ VRAM
# SDXL models need 8GB+ VRAM

# 2. Check file integrity
# Re-download if corrupted

# 3. Check format compatibility
# Flux: Must be Diffusers format
# SDXL: Must be .safetensors or .ckpt

# 4. Check InvokeAI version
invokeai --version
# Update if needed: pip install --upgrade invokeai
```

### Out of Memory Errors

**Problem**: OOM (Out of Memory) errors

**Solutions**:
```bash
# 1. Use smaller model
# Try flux-schnell instead of flux-dev
# Or SDXL instead of Flux

# 2. Reduce resolution
invokeai "prompt" --width 512 --height 512

# 3. Use lower precision
# Some models support fp16 or int8

# 4. Close other applications
# Free up VRAM
```

### NSFW Content Filtered

**Problem**: Safety filters blocking content

**Solutions**:
```bash
# 1. Check model
# Some models have built-in filters
# Try different model

# 2. Check InvokeAI settings
# Look for safety/safety_checker settings
# Disable if available

# 3. Use uncensored models
# Look for "uncensored" or "nsfw" in model name
# Check model descriptions
```

### Download Fails

**Problem**: Can't download model

**Solutions**:
```bash
# 1. Check internet connection
ping huggingface.co

# 2. Use different method
# Try git clone instead of huggingface-cli
# Or manual download

# 3. Check authentication
# Some models require Hugging Face login
huggingface-cli login

# 4. Check disk space
df -h
# Need ~25GB for Flux models
# Need ~7GB for SDXL models
```

---

## Quick Reference

### Model Directories

```bash
# Default locations
~/invokeai/models/checkpoints/     # Main models
~/invokeai/models/loras/           # LoRA models
~/invokeai/models/vae/             # VAE models
```

### Download Commands

```bash
# Flux via Hugging Face CLI
huggingface-cli download black-forest-labs/FLUX.1-dev \
  --local-dir ~/invokeai/models/checkpoints/flux-dev

# Flux via Git
cd ~/invokeai/models/checkpoints
git clone https://huggingface.co/black-forest-labs/FLUX.1-dev

# Via InvokeAI
invokeai --download-models flux-dev
```

### Verification Commands

```bash
# List models
invokeai --list-models

# Test model
invokeai "test prompt" --model flux-dev

# Check version
invokeai --version
```

---

## Resources

### Official Sources

- **Hugging Face**: https://huggingface.co
- **Flux Official**: https://huggingface.co/black-forest-labs
- **InvokeAI Docs**: https://invoke-ai.github.io/InvokeAI/

### Community Sources

- **CivitAI**: https://civitai.com
- **InvokeAI GitHub**: https://github.com/invoke-ai/InvokeAI
- **Community Forums**: Check InvokeAI Discord/Forums

### Search Terms

**For Flux Models**:
- `flux nsfw`
- `flux uncensored`
- `flux fine-tuned`
- `flux adult`

**For SDXL Models**:
- `sdxl nsfw`
- `sdxl uncensored`
- `sdxl explicit`
- `sdxl adult`

---

## Summary Checklist

- [ ] Set up InvokeAI workspace
- [ ] Identify desired models (Flux vs SDXL)
- [ ] Check VRAM requirements
- [ ] Download Flux base model (if using Flux)
- [ ] Download SDXL models (if using SDXL)
- [ ] Place models in correct directory
- [ ] Verify models appear in list
- [ ] Test model loading
- [ ] Test NSFW generation
- [ ] Configure default model (optional)

---

**Remember**: Always verify model compatibility with InvokeAI before downloading large files. Check model descriptions and community reviews for NSFW capability and quality.

