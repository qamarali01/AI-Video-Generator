import os
from typing import Dict
import requests
import replicate
from dotenv import load_dotenv

load_dotenv()

class VideoService:
    def __init__(self):
        # Initialize API keys
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.replicate_key = os.getenv("REPLICATE_API_TOKEN")
        
        if not self.openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is not set")
        if not self.replicate_key:
            raise ValueError("REPLICATE_API_TOKEN environment variable is not set")
        
        # Set Replicate API key
        os.environ["REPLICATE_API_TOKEN"] = self.replicate_key

    async def enhance_prompt(self, prompt: str) -> str:
        """Use Qwen to enhance the video generation prompt"""
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": os.getenv("APP_URL", "http://localhost:5173"),
                    "X-Title": "AI Video Generator"
                },
                json={
                    "model": "qwen/qwen-2.5-72b-instruct",
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are a professional video director specializing in AI video generation. Convert user prompts into detailed, cinematic prompts that will result in high-quality videos. Focus on:
1. Visual style (cinematic, dramatic, artistic)
2. Lighting conditions (golden hour, dramatic shadows, etc.)
3. Camera movements (slow pan, aerial view, etc.)
4. Color palette and mood
5. Specific details that make the scene unique

Format your response as a single, detailed paragraph without any prefixes or explanations. Focus purely on the visual description."""
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 200
                }
            )
            
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Prompt enhancement failed: {str(e)}")
            return prompt

    async def generate_video(self, prompt: str) -> Dict[str, str]:
        try:
            # Enhance the prompt using Qwen 2.5
            enhanced_prompt = await self.enhance_prompt(prompt)
            print(f"Using enhanced prompt: {enhanced_prompt}")
            
            # Use Stable Video Diffusion for better quality
            output = replicate.run(
                "stability-ai/stable-video-diffusion:3d00aa9e6d38f25af51c53b0a7d0b5e137c2224a0c8db0d8e8d320040bbbc5df",
                input={
                    "cond_aug": 0.02,
                    "decoding_t": 7,
                    "frames": 25,
                    "height": 576,
                    "width": 1024,
                    "input_image": None,
                    "motion_bucket_id": 127,
                    "negative_prompt": "blurry, low quality, distorted, ugly, bad anatomy, extra limbs, watermark, text, timestamp, duplicate, double image, pixelated",
                    "num_inference_steps": 50,
                    "prompt": enhanced_prompt,
                    "seed": 42,
                    "sizing_strategy": "maintain_aspect_ratio",
                    "video_length": "25_frames_with_svd_xt"
                }
            )
            
            print(f"Replicate output: {output}")
            
            # The output is usually a list with the video URL as the first element
            video_url = output[0] if isinstance(output, list) and output else output
            
            return {
                "status": "success",
                "message": "Video generated successfully",
                "videoUrl": video_url,
                "generationDetails": f"Enhanced prompt: {enhanced_prompt}"
            }

        except Exception as e:
            print(f"Video generation error: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "videoUrl": None,
                "generationDetails": None
            }