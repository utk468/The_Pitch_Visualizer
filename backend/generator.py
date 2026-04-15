import os
import asyncio
import uuid
import base64
import io
from PIL import Image
from huggingface_hub import InferenceClient
from .state import PitchState
from fastapi.concurrency import run_in_threadpool

async def generate_single_image(prompt: str, style: str):
    """
    Helper to generate a single image via HF InferenceClient and return as Base64.
    """
    api_key = os.getenv("HF_API_KEY")
    client = InferenceClient(
        model="stabilityai/stable-diffusion-xl-base-1.0",
        token=api_key
    )
    
    def call_client():
        try:
            image = client.text_to_image(
                prompt,
                negative_prompt="blurry, text, watermark, low quality, distorted",
                num_inference_steps=35,
                guidance_scale=7.5
            )
            return image
        except Exception as e:
            print(f"InferenceClient Error for prompt '{prompt[:30]}...': {e}")
            return None

    image = await run_in_threadpool(call_client)
    
    if image:
        # Convert PIL Image to Base64 String 
        def encode_image():
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG", quality=85)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            return f"data:image/jpeg;base64,{img_str}"
        
        base64_data = await run_in_threadpool(encode_image)
        return base64_data
    
    return "/static/placeholder.png"

async def image_generator(state: PitchState):
    """
    Node to generate all images IN PARALLEL and return as Base64.
    """
    prompts = state["prompts"]
    style = state.get("style", "digital art")
    
    # Schedule all generation tasks concurrently
    tasks = [generate_single_image(prompt, style) for prompt in prompts]
    b64_images = await asyncio.gather(*tasks)
    
    storyboard = []
    for i, b64 in enumerate(b64_images):
        storyboard.append({
            "text": state["segments"][i],
            "prompt": prompts[i],
            "image_url": b64 # stores the full base64 data
        })
        
    return {"image_urls": b64_images, "storyboard": storyboard}
