from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReportCreate(BaseModel):
    panel_check_id: int
    user_id: Optional[int]
    description: Optional[str] = None



class ReportResponse(BaseModel):
    id: int
    panel_check_id: int
    user_id: Optional[int]
    description: Optional[str]
    timestamp: datetime

    class Config:
        orm_mode = True

class ReportUpdate(BaseModel):
    description: str

class ReportDelete(BaseModel):
    id: int