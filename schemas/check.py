from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.models_enum import ModelEnum


class CheckCreate(BaseModel):
    panel_id: Optional[int] = None
    status: str
    model: ModelEnum
    image_path: Optional[str] = None
    timestamp: Optional[datetime] = None

class CheckResponse(BaseModel):
    id: int
    panel_id: Optional[int] = None
    model: ModelEnum
    status: str
    image_path: Optional[str]
    timestamp: datetime

    class Config:
        orm_mode = True
