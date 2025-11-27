# InvokeAI Setup Guide - New Workspace

## Overview

This guide helps you set up InvokeAI in a new workspace, separate from your Stable Diffusion WebUI installation. InvokeAI supports Flux models and other modern formats that WebUI doesn't support.

---

## Strategy Overview

1. **Create new workspace directory**
2. **Set up Python virtual environment** (recommended)
3. **Install InvokeAI**
4. **Configure InvokeAI**
5. **Download models** (Flux, SDXL, etc.)
6. **Launch and test**

---

## Step-by-Step Setup

### Step 1: Create New Workspace

```bash
# Navigate to your AI dev directory
cd /Volumes/5bits/current/ai-dev

# Create new workspace for InvokeAI
mkdir invokeai-workspace
cd invokeai-workspace

# Verify you're in the right place
pwd
# Should show: /Volumes/5bits/current/ai-dev/invokeai-workspace
```

### Step 2: Set Up Python Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# Verify Python version (InvokeAI requires Python 3.10+)
python --version
# Should show Python 3.10 or higher

# Upgrade pip
pip install --upgrade pip
```

### Step 3: Install InvokeAI

```bash
# Install InvokeAI
pip install invokeai

# Verify installation
invokeai --version
```

**Note**: Installation may take several minutes as it downloads dependencies.

### Step 4: Configure InvokeAI

```bash
# Run configuration wizard
invokeai-configure
```

**Configuration Options:**

1. **Model Storage Location**:
   - Default: `~/invokeai/models` (in your home directory)
   - Recommended: Use default or specify custom path
   - Example: `/Volumes/5bits/current/ai-dev/invokeai-workspace/models`

2. **Download Base Models**:
   - **SD 1.5**: Optional (you already have SD 1.5 models)
   - **SDXL**: Recommended if you have 8GB+ VRAM
   - **Flux.1-dev**: Recommended for modern high-quality generation
   - **Flux.1-schnell**: Fast version, good for testing

3. **VAE Selection**:
   - Default VAE is usually fine
   - Can add custom VAEs later

4. **Output Directory**:
   - Default: `~/invokeai/outputs`
   - Can customize if desired

**Configuration File Location**:
- After configuration, settings are saved to: `~/.invokeai/invokeai.yaml`
- Or custom location if specified during setup

### Step 5: Launch InvokeAI

```bash
# Launch InvokeAI Web Interface
invokeai --web

# Or launch with specific host/port
invokeai --web --host 0.0.0.0 --port 9090

# Or launch in headless mode (API only)
invokeai --web --host 0.0.0.0 --port 9090 --no-frontend
```

**Default Access**:
- Web UI: http://localhost:9090
- API: http://localhost:9090/api/v1

---

## Quick Start Script

Create a script to automate setup:

```bash
# Create setup script
cat > setup_invokeai.sh << 'EOF'
#!/bin/bash

# InvokeAI Setup Script
set -e

echo "=========================================="
echo "InvokeAI Setup Script"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install InvokeAI
echo "Installing InvokeAI (this may take a while)..."
pip install invokeai

# Verify installation
echo "Verifying installation..."
invokeai --version

echo "=========================================="
echo "Installation complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Run configuration: invokeai-configure"
echo "3. Launch InvokeAI: invokeai --web"
echo ""
EOF

chmod +x setup_invokeai.sh
```

**Run the script**:
```bash
./setup_invokeai.sh
```

---

## Configuration Details

### Manual Configuration

If you want to configure manually or edit settings:

**Configuration File**: `~/.invokeai/invokeai.yaml`

**Key Settings**:
```yaml
# Model paths
paths:
  models_dir: /path/to/models
  output_dir: /path/to/outputs

# Default model
InvokeAI:
  model: flux-dev  # or sdxl, sd15, etc.
  
# API settings
InvokeAI:
  host: 0.0.0.0
  port: 9090
```

### Environment Variables

You can also set environment variables:

```bash
# Set model directory
export INVOKEAI_ROOT=/Volumes/5bits/current/ai-dev/invokeai-workspace

# Set output directory
export INVOKEAI_OUTPUT_DIR=/Volumes/5bits/current/ai-dev/invokeai-workspace/outputs
```

---

## Downloading Models

### Via Configuration Wizard

During `invokeai-configure`, you can download:
- SD 1.5 models
- SDXL models
- Flux models

### Via Command Line

```bash
# Download Flux.1-dev
invokeai --download-models flux-dev

# Download Flux.1-schnell (fast version)
invokeai --download-models flux-schnell

# Download SDXL
invokeai --download-models sdxl

# List available models
invokeai --list-models
```

### Manual Download

Models are stored in: `~/invokeai/models` (or your configured path)

You can manually place models there:
- **Flux models**: Place in `checkpoints/` subdirectory
- **SDXL models**: Place in `checkpoints/` subdirectory
- **LoRA**: Place in `loras/` subdirectory

---

## Usage Examples

### Web Interface

1. Launch: `invokeai --web`
2. Open browser: http://localhost:9090
3. Use the web interface to generate images

### Command Line

```bash
# Generate image from prompt
invokeai "a beautiful landscape, masterpiece, 8k"

# Generate with specific model
invokeai "a beautiful portrait" --model flux-dev

# Generate with custom settings
invokeai "your prompt" \
  --steps 30 \
  --cfg-scale 7.5 \
  --width 1024 \
  --height 1024 \
  --model flux-dev
```

### API Usage

```bash
# Generate via API
curl -X POST http://localhost:9090/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "masterpiece, best quality, a beautiful portrait",
    "model": "flux-dev",
    "steps": 30,
    "cfg_scale": 7.5,
    "width": 1024,
    "height": 1024
  }'
```

---

## Integration with Existing Setup

### Share Models (Optional)

If you want to use models from your WebUI installation:

```bash
# Create symlink to share models (optional)
# Note: Format compatibility may vary
ln -s /Volumes/5bits/current/ai-dev/stable-diffusion-webui/models/Stable-diffusion \
  ~/invokeai/models/checkpoints/webui-models
```

**Warning**: Not all WebUI models work in InvokeAI due to format differences.

### Run Both Simultaneously

You can run both WebUI and InvokeAI:

```bash
# Terminal 1: WebUI
cd /Volumes/5bits/current/ai-dev/stable-diffusion-webui
python launch.py --api --port 7860

# Terminal 2: InvokeAI
cd /Volumes/5bits/current/ai-dev/invokeai-workspace
source venv/bin/activate
invokeai --web --port 9090
```

**Ports**:
- WebUI: http://localhost:7860
- InvokeAI: http://localhost:9090

---

## Troubleshooting

### Installation Issues

**Problem**: `pip install invokeai` fails
```bash
# Solution: Upgrade pip and try again
pip install --upgrade pip setuptools wheel
pip install invokeai
```

**Problem**: Python version too old
```bash
# Check version
python3 --version

# Need Python 3.10+
# Install Python 3.10+ if needed (macOS: brew install python@3.11)
```

### Configuration Issues

**Problem**: `invokeai-configure` fails
```bash
# Try running with verbose output
invokeai-configure --verbose

# Or configure manually by editing:
# ~/.invokeai/invokeai.yaml
```

### Model Loading Issues

**Problem**: Models won't load
```bash
# Check model format
# InvokeAI prefers Diffusers format for Flux
# Check model location: ~/invokeai/models/checkpoints/

# Verify model files
ls -lh ~/invokeai/models/checkpoints/
```

### VRAM Issues

**Problem**: Out of memory errors
```bash
# Use smaller models
invokeai --model flux-schnell  # Instead of flux-dev

# Or use SDXL instead of Flux
invokeai --model sdxl

# Reduce resolution
invokeai "prompt" --width 512 --height 512
```

---

## Recommended Models for NSFW

### Flux Models (High Quality)
- **Flux.1-dev** - Best quality, slower
- **Flux.1-schnell** - Fast, good quality
- **Flux fine-tunes** - Various NSFW fine-tunes available

### SDXL Models (Good Compatibility)
- **SDXL Base** - Works well
- **Juggernaut XL** - Popular NSFW SDXL
- **RealVisXL** - Realistic NSFW SDXL

### Where to Find Models
- **Hugging Face**: https://huggingface.co (official Flux models)
- **CivitAI**: https://civitai.com (fine-tuned models)
- **InvokeAI Model Library**: Built into InvokeAI

**📖 For detailed NSFW model download guide, see**: `INVOKEAI_NSFW_MODELS_GUIDE.md`

---

## File Structure

After setup, your workspace will look like:

```
invokeai-workspace/
├── venv/                    # Virtual environment
├── setup_invokeai.sh       # Setup script (if created)
└── (other files)

~/.invokeai/                 # Configuration directory
├── invokeai.yaml           # Main config file
└── (other config files)

~/invokeai/                  # Default model/output directory
├── models/
│   ├── checkpoints/        # Model checkpoints
│   ├── loras/             # LoRA models
│   └── vae/               # VAE models
└── outputs/               # Generated images
```

---

## Quick Reference Commands

```bash
# Activate environment
source venv/bin/activate

# Launch Web UI
invokeai --web

# Launch API only
invokeai --web --no-frontend

# Generate from command line
invokeai "your prompt"

# List models
invokeai --list-models

# Download model
invokeai --download-models flux-dev

# Check version
invokeai --version

# Get help
invokeai --help
```

---

## Next Steps

1. **Complete Setup**: Run through all steps above
2. **Download Models**: Get Flux or SDXL models
3. **Test Generation**: Try generating some images
4. **Explore Features**: Check out InvokeAI's unique features
5. **Compare**: Test same prompts in both WebUI and InvokeAI

---

## Comparison: WebUI vs InvokeAI

| Feature | WebUI | InvokeAI |
|---------|-------|----------|
| SD 1.5 Support | ✅ Excellent | ✅ Good |
| SDXL Support | ✅ Good | ✅ Excellent |
| SD 3 Support | ✅ Good | ✅ Good |
| Flux Support | ❌ No | ✅ Yes |
| NSFW Support | ✅ Excellent | ✅ Excellent |
| API | ✅ Yes | ✅ Yes |
| Ease of Use | ✅ Very Easy | ✅ Easy |
| Model Selection | ✅ Wide | ✅ Wide |

**Best Use Cases**:
- **WebUI**: SD 1.5 models, wide extension ecosystem
- **InvokeAI**: Flux models, modern formats, different workflow

---

## Resources

- **InvokeAI GitHub**: https://github.com/invoke-ai/InvokeAI
- **InvokeAI Documentation**: https://invoke-ai.github.io/InvokeAI/
- **Flux Models**: https://huggingface.co/black-forest-labs
- **Community**: InvokeAI Discord/Forums

---

**Ready to start?** Follow the steps above to set up InvokeAI in your new workspace!

