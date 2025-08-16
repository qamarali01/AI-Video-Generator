from fastapi import APIRouter, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from .models import PromptRequest, VideoResponse
from .services.video_service import VideoService

router = APIRouter()
video_service = VideoService()

@router.get("/")
async def read_root(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return {"status": "healthy", "message": "Video Generation API is running"}

@router.options("/api/generate-video")
async def options_generate_video(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return {}

@router.post("/api/generate-video", response_model=VideoResponse)
async def generate_video(request: PromptRequest, response: Response) -> VideoResponse:
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    try:
        result = await video_service.generate_video(request.prompt)
        return VideoResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))