# Enhanced API Wrapper Guide

## Overview

The Enhanced API Wrapper provides a simplified interface to the Stable Diffusion WebUI API with:
- **Model Selection**: Choose from available models (Real-Dreams, Realistic Vision, DreamShaper, etc.)
- **ADetailer Control**: Easy enable/disable with customizable settings
- **Preset Configurations**: Optimal settings for each model
- **Simplified API**: Cleaner request format

## Setup

### Prerequisites

1. **WebUI must be running** with API enabled:
   ```bash
   python launch.py --api
   ```
   WebUI should be accessible at: `http://localhost:7860`

2. **Install dependencies**:
   ```bash
   pip install requests fastapi uvicorn
   ```

### Start the Enhanced API Wrapper

```bash
python enhanced_api_wrapper.py
```

The wrapper will run on: `http://localhost:8080`

---

## API Endpoints

### `GET /` - API Documentation
Returns API information and available models.

### `GET /models` - List Available Models
Get list of all available models.

### `GET /presets` - Get Model Presets
Get recommended settings for each model.

### `GET /health` - Health Check
Verify WebUI is accessible and get current configuration.

### `POST /generate` - Generate Image
Main endpoint for image generation with enhanced options.

---

## Usage Examples

### Basic Generation (Using Presets)

```bash
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "masterpiece, best quality, highly detailed, 8k, a beautiful portrait, photorealistic",
    "model": "real-dreams"
  }'
```

### With ADetailer Enabled

```bash
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "masterpiece, best quality, highly detailed, 8k, a beautiful portrait, photorealistic",
    "model": "real-dreams",
    "adetailer": {
      "enabled": true,
      "model": "face_yolov8n.pt"
    }
  }'
```

### With Hires.Fix and ADetailer

```bash
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "masterpiece, best quality, highly detailed, 8k, a beautiful portrait, photorealistic",
    "model": "real-dreams",
    "adetailer": {
      "enabled": true,
      "model": "face_yolov8n.pt",
      "denoising_strength": 0.4,
      "steps": 28
    },
    "hires_fix": {
      "enabled": true,
      "scale": 1.5,
      "upscaler": "4x-UltraSharp"
    }
  }'
```

### Custom Settings (Override Presets)

```bash
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "masterpiece, best quality, highly detailed, 8k, a beautiful portrait",
    "model": "real-dreams",
    "steps": 30,
    "cfg_scale": 8.0,
    "sampler": "DPM++ 2M Karras",
    "width": 768,
    "height": 1024,
    "seed": 42
  }'
```

### Switch to Realistic Vision Model

```bash
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "ultra realistic portrait, professional photography",
    "model": "realistic-vision",
    "adetailer": {
      "enabled": true
    }
  }'
```

### Full Custom ADetailer Configuration

```bash
curl -X POST http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "masterpiece, best quality, highly detailed, 8k, a beautiful portrait",
    "model": "real-dreams",
    "adetailer": {
      "enabled": true,
      "model": "face_yolov8n.pt",
      "detection_confidence": 0.3,
      "denoising_strength": 0.4,
      "steps": 28,
      "cfg_scale": 7.0,
      "sampler": "DPM++ SDE Karras",
      "prompt": "beautiful face, detailed eyes, perfect skin",
      "negative_prompt": "blurry face, deformed face, bad eyes",
      "mask_only_top_k": 1
    }
  }'
```

---

## Python Examples

### Basic Usage

```python
import requests

url = "http://localhost:8080/generate"

payload = {
    "prompt": "masterpiece, best quality, highly detailed, 8k, a beautiful portrait",
    "model": "real-dreams",
    "adetailer": {
        "enabled": True,
        "model": "face_yolov8n.pt"
    }
}

response = requests.post(url, json=payload)
result = response.json()

if result["status"] == "success":
    # Images are base64 encoded in result["images"]
    print(f"Generated {len(result['images'])} image(s)")
    print(f"Model used: {result['model_used']}")
    print(f"Parameters: {result['parameters']}")
```

### With Error Handling

```python
import requests

def generate_image(prompt, model="real-dreams", use_adetailer=True):
    url = "http://localhost:8080/generate"
    
    payload = {
        "prompt": prompt,
        "model": model,
        "adetailer": {
            "enabled": use_adetailer,
            "model": "face_yolov8n.pt"
        } if use_adetailer else None
    }
    
    try:
        response = requests.post(url, json=payload, timeout=300)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to API wrapper. Is it running?")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        print(f"Response: {response.text}")
        return None

# Usage
result = generate_image(
    "masterpiece, best quality, highly detailed, 8k, a beautiful portrait",
    model="real-dreams",
    use_adetailer=True
)

if result:
    print(f"Success! Generated {len(result['images'])} image(s)")
```

### Batch Generation

```python
import requests
import time

def generate_batch(prompts, model="real-dreams", use_adetailer=True):
    url = "http://localhost:8080/generate"
    results = []
    
    for prompt in prompts:
        payload = {
            "prompt": prompt,
            "model": model,
            "adetailer": {
                "enabled": use_adetailer,
                "model": "face_yolov8n.pt"
            } if use_adetailer else None
        }
        
        response = requests.post(url, json=payload, timeout=300)
        if response.status_code == 200:
            results.append(response.json())
        else:
            print(f"Error generating for prompt: {prompt}")
        
        time.sleep(1)  # Rate limiting
    
    return results

# Usage
prompts = [
    "masterpiece, best quality, a beautiful portrait of a woman",
    "masterpiece, best quality, a handsome portrait of a man",
    "masterpiece, best quality, a cute portrait of a child"
]

results = generate_batch(prompts, model="real-dreams", use_adetailer=True)
print(f"Generated {len(results)} images")
```

---

## Request Parameters

### Main Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | **required** | Main prompt |
| `negative_prompt` | string | (default) | Negative prompt |
| `model` | string | `"real-dreams"` | Model to use: `real-dreams`, `realistic-vision`, `dreamshaper`, `deliberate`, `sd-v1.5` |
| `steps` | integer | (preset) | Sampling steps (None = use preset) |
| `cfg_scale` | float | (preset) | CFG scale (None = use preset) |
| `sampler` | string | (preset) | Sampler name (None = use preset) |
| `width` | integer | (preset) | Image width (None = use preset) |
| `height` | integer | (preset) | Image height (None = use preset) |
| `seed` | integer | `null` | Seed (-1 for random) |
| `batch_size` | integer | `1` | Number of images to generate |

### ADetailer Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | boolean | `false` | Enable ADetailer |
| `model` | string | `"face_yolov8n.pt"` | Detection model |
| `detection_confidence` | float | `0.3` | Detection confidence (0.0-1.0) |
| `denoising_strength` | float | `0.4` | Denoising strength (0.0-1.0) |
| `steps` | integer | `28` | ADetailer steps |
| `cfg_scale` | float | `7.0` | ADetailer CFG scale |
| `sampler` | string | `null` | ADetailer sampler (null = use main) |
| `prompt` | string | `""` | ADetailer prompt (empty = use main) |
| `negative_prompt` | string | (default) | ADetailer negative prompt |
| `mask_only_top_k` | integer | `1` | Process only top K detections |

### Hires.Fix Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `enabled` | boolean | `false` | Enable Hires.Fix |
| `scale` | float | `1.5` | Upscale factor (1.0-4.0) |
| `denoising_strength` | float | `0.4` | Denoising strength (0.0-1.0) |
| `upscaler` | string | `"4x-UltraSharp"` | Upscaler name |
| `steps` | integer | `15` | Hires.Fix steps |

---

## Model Presets

### Real-Dreams (Default)
- **Sampler**: Euler a
- **Steps**: 25
- **CFG Scale**: 7.5
- **Resolution**: 512x768

### Realistic Vision
- **Sampler**: DPM++ SDE Karras
- **Steps**: 30
- **CFG Scale**: 7.0
- **Resolution**: 768x1024

### DreamShaper
- **Sampler**: Euler a
- **Steps**: 25
- **CFG Scale**: 7.5
- **Resolution**: 512x768

### Deliberate v3
- **Sampler**: Euler a or DPM++ 2M Karras
- **Steps**: 20-30
- **CFG Scale**: 7.0-8.0
- **Resolution**: 512x512, 768x768, 512x768
- **Note**: Versatile model for people, landscapes, architecture, various styles

### SD v1.5
- **Sampler**: Euler a
- **Steps**: 20
- **CFG Scale**: 7.5
- **Resolution**: 512x512

---

## Response Format

```json
{
  "status": "success",
  "model_used": "real-dreams",
  "model_file": "Real-Dreams.safetensors",
  "images": [
    "base64_encoded_image_data..."
  ],
  "parameters": {
    "prompt": "...",
    "steps": 25,
    "cfg_scale": 7.5,
    "sampler": "Euler a",
    "width": 512,
    "height": 768,
    "adetailer_enabled": true,
    "hires_fix_enabled": false
  },
  "info": "generation_info_string",
  "webui_request": { ... }
}
```

---

## Troubleshooting

### "Cannot connect to WebUI"
- Make sure WebUI is running: `python launch.py --api`
- Check WebUI is accessible: `curl http://localhost:7860/sdapi/v1/options`
- Verify port 7860 is not blocked

### "Model not found"
- Check model file exists in `models/Stable-diffusion/`
- Verify model name in `AVAILABLE_MODELS` dictionary
- Check WebUI can see the model: `curl http://localhost:7860/sdapi/v1/sd-models`

### ADetailer not working
- Verify ADetailer extension is installed
- Check ADetailer models are downloaded
- Look at WebUI console for error messages

### Timeout errors
- Increase timeout in your client (default: 300 seconds)
- Reduce resolution or steps
- Check WebUI console for errors

---

## Comparison: Direct WebUI API vs Enhanced Wrapper

### Direct WebUI API (Complex)

```json
{
  "prompt": "...",
  "steps": 25,
  "cfg_scale": 7.5,
  "sampler_name": "Euler a",
  "width": 512,
  "height": 768,
  "override_settings": {
    "sd_model_checkpoint": "Real-Dreams.safetensors"
  },
  "alwayson_scripts": {
    "ADetailer": {
      "args": [true, "face_yolov8n.pt", 0.3, 4, 4, true, 32, 0.4, 7.0, 28, "Euler a", "", "blurry face", 1, null]
    }
  }
}
```

### Enhanced Wrapper (Simple)

```json
{
  "prompt": "...",
  "model": "real-dreams",
  "adetailer": {
    "enabled": true,
    "model": "face_yolov8n.pt"
  }
}
```

---

## Benefits

1. **Simpler API**: Cleaner request format
2. **Model Presets**: Optimal settings automatically applied
3. **Easy Model Switching**: Just change `model` parameter
4. **ADetailer Control**: Simple enable/disable with sensible defaults
5. **Type Safety**: Pydantic models for validation
6. **Error Handling**: Better error messages
7. **Documentation**: Auto-generated API docs at `/docs`

---

## Interactive API Documentation

Visit `http://localhost:8080/docs` for interactive Swagger documentation where you can test the API directly in your browser.

