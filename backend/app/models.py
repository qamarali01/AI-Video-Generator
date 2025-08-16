from pydantic import BaseModel
from typing import Optional

class PromptRequest(BaseModel):
    prompt: str

class VideoResponse(BaseModel):
    status: str
    message: str
    videoUrl: Optional[str] = None
    generationDetails: Optional[str] = None