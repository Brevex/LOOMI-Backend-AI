from pydantic import BaseModel
from typing import Optional


class PaintBase(BaseModel):
    name: str
    color: str
    surface_type: Optional[str] = None
    environment: Optional[str] = None
    finish_type: Optional[str] = None
    features: Optional[str] = None
    line: Optional[str] = None


class PaintCreate(PaintBase):
    pass


class PaintUpdate(PaintBase):
    name: Optional[str] = None
    color: Optional[str] = None


class Paint(PaintBase):
    id: int

    class Config:
        from_attributes = True
