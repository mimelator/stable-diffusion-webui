#!/usr/bin/env python3
"""
Enhanced API Wrapper for Stable Diffusion WebUI
Provides convenient model selection and ADetailer control

This wrapper connects to the WebUI API (port 7860) and provides:
- Model selection (Real-Dreams, Realistic Vision, DreamShaper, etc.)
- ADetailer control (enable/disable with custom settings)
- Preset configurations
- Simplified API interface

Usage:
    pip install requests fastapi uvicorn
    python enhanced_api_wrapper.py

API endpoint: http://localhost:8080/generate
WebUI must be running on: http://localhost:7860
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal
import requests
import json
from enum import Enum

app = FastAPI(title="Enhanced Stable Diffusion API Wrapper")

# WebUI API base URL
WEBUI_API_URL = "http://localhost:7860"

# Available models mapping
AVAILABLE_MODELS = {
    "real-dreams": "Real-Dreams.safetensors",
    "realistic-vision": "Realistic_Vision_V6.0_NV_B1_fp16.safetensors",
    "dreamshaper": "dreamshaper_8.safetensors",
    "deliberate": "Deliberate_v3.safetensors",  # Add after downloading
    "sd-v1.5": "v1-5-pruned-emaonly.safetensors",
}

# Model presets
MODEL_PRESETS = {
    "real-dreams": {
        "sampler": "Euler a",
        "steps": 25,
        "cfg_scale": 7.5,
        "recommended_resolution": {"width": 512, "height": 768},
    },
    "realistic-vision": {
        "sampler": "DPM++ SDE Karras",
        "steps": 30,
        "cfg_scale": 7.0,
        "recommended_resolution": {"width": 768, "height": 1024},
    },
    "dreamshaper": {
        "sampler": "Euler a",
        "steps": 25,
        "cfg_scale": 7.5,
        "recommended_resolution": {"width": 512, "height": 768},
    },
    "deliberate": {
        "sampler": "Euler a",
        "steps": 25,
        "cfg_scale": 7.5,
        "recommended_resolution": {"width": 512, "height": 768},
    },
    "sd-v1.5": {
        "sampler": "Euler a",
        "steps": 20,
        "cfg_scale": 7.5,
        "recommended_resolution": {"width": 512, "height": 512},
    },
}


class ADetailerConfig(BaseModel):
    """ADetailer configuration"""
    enabled: bool = Field(default=False, description="Enable ADetailer")
    model: str = Field(
        default="face_yolov8n.pt",
        description="ADetailer model (face_yolov8n.pt, face_yolov8s.pt, hand_yolov8n.pt)"
    )
    detection_confidence: float = Field(default=0.3, ge=0.0, le=1.0, description="Detection confidence threshold")
    denoising_strength: float = Field(default=0.4, ge=0.0, le=1.0, description="Denoising strength")
    steps: int = Field(default=28, ge=1, le=100, description="ADetailer steps")
    cfg_scale: float = Field(default=7.0, ge=1.0, le=30.0, description="ADetailer CFG scale")
    sampler: Optional[str] = Field(default=None, description="ADetailer sampler (None = use main sampler)")
    prompt: Optional[str] = Field(default="", description="ADetailer prompt (empty = use main prompt)")
    negative_prompt: Optional[str] = Field(
        default="blurry face, deformed face, bad eyes, bad anatomy",
        description="ADetailer negative prompt"
    )
    mask_only_top_k: int = Field(default=1, ge=1, description="Process only top K largest detections")


class HiresFixConfig(BaseModel):
    """High-Resolution Fix configuration"""
    enabled: bool = Field(default=False, description="Enable Hires.Fix")
    scale: float = Field(default=1.5, ge=1.0, le=4.0, description="Upscale factor")
    denoising_strength: float = Field(default=0.4, ge=0.0, le=1.0, description="Denoising strength")
    upscaler: str = Field(
        default="4x-UltraSharp",
        description="Upscaler name (4x-UltraSharp, R-ESRGAN 4x+, Latent, etc.)"
    )
    steps: int = Field(default=15, ge=1, le=100, description="Hires.Fix steps")


class GenerateRequest(BaseModel):
    """Enhanced generation request"""
    prompt: str = Field(..., description="Main prompt")
    negative_prompt: Optional[str] = Field(
        default="lowres, bad anatomy, bad hands, text, error, missing fingers, worst quality, low quality",
        description="Negative prompt"
    )
    
    # Model selection
    model: Literal["real-dreams", "realistic-vision", "dreamshaper", "deliberate", "sd-v1.5"] = Field(
        default="real-dreams",
        description="Model to use"
    )
    
    # Generation parameters
    steps: Optional[int] = Field(default=None, ge=1, le=150, description="Sampling steps (None = use preset)")
    cfg_scale: Optional[float] = Field(default=None, ge=1.0, le=30.0, description="CFG scale (None = use preset)")
    sampler: Optional[str] = Field(default=None, description="Sampler name (None = use preset)")
    width: Optional[int] = Field(default=None, ge=64, le=2048, description="Width (None = use preset)")
    height: Optional[int] = Field(default=None, ge=64, le=2048, description="Height (None = use preset)")
    seed: Optional[int] = Field(default=None, description="Seed (-1 for random)")
    batch_size: int = Field(default=1, ge=1, le=8, description="Batch size")
    
    # ADetailer configuration
    adetailer: Optional[ADetailerConfig] = Field(default=None, description="ADetailer settings")
    
    # Hires.Fix configuration
    hires_fix: Optional[HiresFixConfig] = Field(default=None, description="Hires.Fix settings")
    
    # Advanced: Override settings directly
    override_settings: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Override WebUI settings directly (advanced)"
    )


def get_webui_models() -> list:
    """Get list of available models from WebUI"""
    try:
        response = requests.get(f"{WEBUI_API_URL}/sdapi/v1/sd-models", timeout=5)
        if response.status_code == 200:
            models = response.json()
            return [model.get("title", model.get("model_name", "")) for model in models]
    except Exception as e:
        print(f"Warning: Could not fetch models from WebUI: {e}")
    return []


def build_webui_request(req: GenerateRequest) -> Dict[str, Any]:
    """Build WebUI API request from enhanced request"""
    
    # Get model preset
    preset = MODEL_PRESETS.get(req.model, MODEL_PRESETS["real-dreams"])
    model_name = AVAILABLE_MODELS.get(req.model, AVAILABLE_MODELS["real-dreams"])
    
    # Use preset values if not specified
    steps = req.steps if req.steps is not None else preset["steps"]
    cfg_scale = req.cfg_scale if req.cfg_scale is not None else preset["cfg_scale"]
    sampler = req.sampler if req.sampler is not None else preset["sampler"]
    
    # Resolution
    if req.width is None or req.height is None:
        rec_res = preset["recommended_resolution"]
        width = req.width if req.width is not None else rec_res["width"]
        height = req.height if req.height is not None else rec_res["height"]
    else:
        width = req.width
        height = req.height
    
    # Build base request
    webui_request = {
        "prompt": req.prompt,
        "negative_prompt": req.negative_prompt,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "sampler_name": sampler,
        "width": width,
        "height": height,
        "batch_size": req.batch_size,
        "override_settings": {
            "sd_model_checkpoint": model_name,
        }
    }
    
    # Add seed
    if req.seed is not None:
        webui_request["seed"] = req.seed
    
    # Add Hires.Fix
    if req.hires_fix and req.hires_fix.enabled:
        webui_request["enable_hr"] = True
        webui_request["hr_scale"] = req.hires_fix.scale
        webui_request["denoising_strength"] = req.hires_fix.denoising_strength
        webui_request["hr_upscaler"] = req.hires_fix.upscaler
        webui_request["hr_second_pass_steps"] = req.hires_fix.steps
    
    # Add ADetailer
    if req.adetailer and req.adetailer.enabled:
        adetailer_sampler = req.adetailer.sampler if req.adetailer.sampler else sampler
        
        webui_request["alwayson_scripts"] = {
            "ADetailer": {
                "args": [
                    True,  # Enable
                    req.adetailer.model,  # Model
                    req.adetailer.detection_confidence,  # Detection confidence
                    4,  # Mask dilation
                    4,  # Mask blur
                    True,  # Inpaint only masked
                    32,  # Inpaint padding
                    req.adetailer.denoising_strength,  # Denoising strength
                    req.adetailer.cfg_scale,  # CFG scale
                    req.adetailer.steps,  # Steps
                    adetailer_sampler,  # Sampler
                    req.adetailer.prompt or "",  # Prompt
                    req.adetailer.negative_prompt or "",  # Negative prompt
                    req.adetailer.mask_only_top_k,  # Mask only top-k largest
                    None  # ControlNet (disabled)
                ]
            }
        }
    
    # Add override settings if provided
    if req.override_settings:
        webui_request["override_settings"].update(req.override_settings)
    
    return webui_request


@app.get("/")
async def root():
    """API documentation"""
    return {
        "message": "Enhanced Stable Diffusion API Wrapper",
        "version": "1.0",
        "webui_url": WEBUI_API_URL,
        "endpoints": {
            "POST /generate": "Generate image with enhanced options",
            "GET /models": "List available models",
            "GET /presets": "Get model presets",
            "GET /health": "Health check"
        },
        "available_models": list(AVAILABLE_MODELS.keys()),
        "example_request": {
            "prompt": "masterpiece, best quality, highly detailed, 8k, a beautiful portrait",
            "model": "real-dreams",
            "adetailer": {
                "enabled": True,
                "model": "face_yolov8n.pt"
            },
            "hires_fix": {
                "enabled": True,
                "scale": 1.5
            }
        }
    }


@app.get("/models")
async def list_models():
    """List available models"""
    webui_models = get_webui_models()
    return {
        "available_models": AVAILABLE_MODELS,
        "webui_models": webui_models,
        "current_default": "real-dreams"
    }


@app.get("/presets")
async def get_presets():
    """Get model presets"""
    return {
        "presets": MODEL_PRESETS,
        "available_models": list(AVAILABLE_MODELS.keys())
    }


@app.get("/health")
async def health_check():
    """Health check - verify WebUI is accessible"""
    try:
        response = requests.get(f"{WEBUI_API_URL}/sdapi/v1/options", timeout=5)
        if response.status_code == 200:
            options = response.json()
            current_model = options.get("sd_model_checkpoint", "Unknown")
            return {
                "status": "healthy",
                "webui_accessible": True,
                "current_webui_model": current_model,
                "wrapper_url": "http://localhost:8080"
            }
        else:
            return {
                "status": "unhealthy",
                "webui_accessible": False,
                "error": f"WebUI returned status {response.status_code}"
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "webui_accessible": False,
            "error": str(e),
            "message": "Make sure WebUI is running on http://localhost:7860"
        }


@app.post("/generate")
async def generate_image(request: GenerateRequest):
    """Generate image with enhanced options"""
    
    # Build WebUI request
    webui_request = build_webui_request(request)
    
    # Call WebUI API
    try:
        response = requests.post(
            f"{WEBUI_API_URL}/sdapi/v1/txt2img",
            json=webui_request,
            timeout=300  # 5 minute timeout
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"WebUI API error: {response.text}"
            )
        
        result = response.json()
        
        # Return enhanced response
        return {
            "status": "success",
            "model_used": request.model,
            "model_file": AVAILABLE_MODELS.get(request.model),
            "images": result.get("images", []),
            "parameters": {
                "prompt": request.prompt,
                "negative_prompt": request.negative_prompt,
                "steps": webui_request["steps"],
                "cfg_scale": webui_request["cfg_scale"],
                "sampler": webui_request["sampler_name"],
                "width": webui_request["width"],
                "height": webui_request["height"],
                "seed": webui_request.get("seed"),
                "adetailer_enabled": request.adetailer.enabled if request.adetailer else False,
                "hires_fix_enabled": request.hires_fix.enabled if request.hires_fix else False,
            },
            "info": result.get("info", ""),
            "webui_request": webui_request  # For debugging
        }
        
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to WebUI. Make sure it's running on http://localhost:7860"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating image: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    print("=" * 60)
    print("Enhanced Stable Diffusion API Wrapper")
    print("=" * 60)
    print(f"Wrapper API: http://localhost:8080")
    print(f"WebUI API: {WEBUI_API_URL}")
    print(f"Available models: {', '.join(AVAILABLE_MODELS.keys())}")
    print("=" * 60)
    print("\nMake sure WebUI is running before making requests!")
    print("Launch WebUI with: python launch.py --api\n")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8080)

