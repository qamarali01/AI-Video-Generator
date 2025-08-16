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
                            "content": """You are a professional cinematographer specializing in creating stunning visual sequences. Transform user prompts into highly detailed, cinematic descriptions that will generate beautiful videos. Your prompts should include:

1. Cinematography:
   - Camera angle and movement (e.g., "slow aerial pan", "dynamic tracking shot", "gentle dolly zoom")
   - Shot composition and framing
   - Depth of field and focus

2. Lighting & Atmosphere:
   - Time of day and lighting conditions
   - Weather and atmospheric effects
   - Color grading and mood

3. Scene Details:
   - Specific visual elements and their placement
   - Textures and materials
   - Environmental details

4. Motion & Flow:
   - Movement patterns and dynamics
   - Transitions and progression
   - Temporal elements

Format your response as a single, flowing paragraph that reads like a professional shot description. Focus purely on the visual elements, avoiding any technical jargon or non-visual descriptions. Make it vivid and specific, but keep the language natural and cinematic.

Example: For "sunset beach", don't just say "A beautiful beach at sunset". Instead, craft something like "A sweeping aerial view gliding over crystalline waters as they reflect the rich golden light of a setting sun, waves gently rolling onto pristine white sand, wispy clouds painted in vibrant oranges and purples stretching across the horizon, palm fronds swaying gently in the warm evening breeze..."
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
            
            # Use Zeroscope v2 XL (known working version)
            output = replicate.run(
                "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
                input={
                    "prompt": enhanced_prompt,
                    "negative_prompt": "blurry, low quality, distorted, ugly, bad anatomy, extra limbs, watermark, text, timestamp, duplicate, double image, pixelated",
                    "width": 768,
                    "height": 432,
                    "fps": 16,
                    "num_frames": 120,  # 7.5 seconds at 16 fps
                    "guidance_scale": 15.0,  # Stronger adherence to prompt
                    "num_inference_steps": 60  # More detail
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
            error_msg = f"Video generation error: {str(e)}"
            print(error_msg)
            print(f"Error type: {type(e)}")
            print(f"Error details: {repr(e)}")
            
            if hasattr(e, 'response'):
                print(f"Response status: {e.response.status_code}")
                print(f"Response body: {e.response.text}")
            
            return {
                "status": "error",
                "message": error_msg,
                "videoUrl": None,
                "generationDetails": None
            }