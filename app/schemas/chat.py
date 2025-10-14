from pydantic import BaseModel
from typing import Optional


class ChatQuery(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    image_url: Optional[str] = None
