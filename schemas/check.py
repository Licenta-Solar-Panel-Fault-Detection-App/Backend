from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CheckCreate(BaseModel):
    panel_id: int
    status: str
    image_path: Optional[str] = None  # path-ul imaginii
    timestamp: Optional[datetime] = None  # poate fi auto-generat dacă e None

class CheckResponse(BaseModel):
    id: int
    panel_id: int
    status: str
    image_path: Optional[str]
    timestamp: datetime

    class Config:
        orm_mode = True
