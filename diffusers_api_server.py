#!/usr/bin/env python3
"""
Simple FastAPI server for Stable Diffusion using Diffusers format models.
Supports models from Hugging Face in Diffusers format.

Usage:
    pip install diffusers transformers accelerate torch fastapi uvicorn pillow
    python diffusers_api_server.py

API endpoint: http://localhost:8000/generate
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import io
import base64
from typing import Optional

app = FastAPI(title="Stable Diffusion Diffusers API")

# Global model variable
pipe = None

class GenerateRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = ""
    num_inference_steps: Optional[int] = 20
    guidance_scale: Optional[float] = 7.5
    width: Optional[int] = 512
    height: Optional[int] = 512
    seed: Optional[int] = None
    model_id: Optional[str] = "stablediffusionapi/deliberate-3"  # Default model

@app.on_event("startup")
async def load_model():
    """Load the model on startup"""
    global pipe
    print("Loading model... This may take a few minutes.")
    # You can change the default model here
    model_id = "stablediffusionapi/deliberate-3"
    
    # Check if CUDA is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32
    
    try:
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=dtype,
            safety_checker=None,  # Disable safety checker if needed
            requires_safety_checker=False
        )
        pipe = pipe.to(device)
        if device == "cuda":
            pipe.enable_attention_slicing()  # Reduce memory usage
        print(f"Model loaded successfully on {device}")
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

@app.post("/generate")
async def generate_image(request: GenerateRequest):
    """Generate an image from a text prompt"""
    global pipe
    
    if pipe is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Set seed if provided
        generator = None
        if request.seed is not None:
            generator = torch.Generator(device=pipe.device).manual_seed(request.seed)
        
        # Generate image
        image = pipe(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            num_inference_steps=request.num_inference_steps,
            guidance_scale=request.guidance_scale,
            width=request.width,
            height=request.height,
            generator=generator
        ).images[0]
        
        # Convert to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        return {
            "image": f"data:image/png;base64,{img_base64}",
            "prompt": request.prompt,
            "parameters": {
                "negative_prompt": request.negative_prompt,
                "steps": request.num_inference_steps,
                "guidance_scale": request.guidance_scale,
                "width": request.width,
                "height": request.height,
                "seed": request.seed
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": pipe is not None,
        "device": str(pipe.device) if pipe else None
    }

@app.get("/")
async def root():
    """API documentation"""
    return {
        "message": "Stable Diffusion Diffusers API",
        "endpoints": {
            "POST /generate": "Generate an image from a text prompt",
            "GET /health": "Check API health status",
            "GET /docs": "Interactive API documentation"
        },
        "example_request": {
            "prompt": "a beautiful landscape",
            "negative_prompt": "blurry, low quality",
            "num_inference_steps": 20,
            "guidance_scale": 7.5,
            "width": 512,
            "height": 512
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

