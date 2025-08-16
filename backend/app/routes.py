from fastapi import APIRouter, HTTPException
from .models import PromptRequest, VideoResponse
from .services.video_service import VideoService

router = APIRouter()
video_service = VideoService()

@router.get("/")
async def read_root():
    return {"status": "healthy", "message": "Video Generation API is running"}

@router.post("/api/generate-video", response_model=VideoResponse)
async def generate_video(request: PromptRequest) -> VideoResponse:
    try:
        result = await video_service.generate_video(request.prompt)
        return VideoResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))