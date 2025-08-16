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
            
            # Use AnimateDiff base model (more cost-effective)
            output = replicate.run(
                "lucataco/animate-diff:cdcd2c66589c8a990e4024b1dc6fedcec4f4c0a41b5c1c6f0d5c46a0c1c2f2c8",
                input={
                    "prompt": enhanced_prompt,
                    "negative_prompt": "blurry, low quality, distorted, ugly, bad anatomy, extra limbs, watermark, text",
                    "num_inference_steps": 15,  # Lower for faster generation
                    "guidance_scale": 7.5,
                    "width": 512,
                    "height": 512,
                    "num_frames": 16,
                    "num_videos": 1,
                    "fps": 8
                }
            )
            
            print(f"Replicate output: {output}")
            
            print(f"Raw output type: {type(output)}")
            print(f"Raw output content: {output}")
            
            # Handle different response formats
            if isinstance(output, list) and output:
                video_url = output[0]
            elif isinstance(output, dict) and 'output' in output:
                video_url = output['output']
            elif isinstance(output, str):
                video_url = output
            else:
                raise ValueError(f"Unexpected output format: {output}")
            
            if not video_url:
                raise ValueError("No video URL in the response")
            
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