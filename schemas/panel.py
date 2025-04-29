from pydantic import BaseModel
from typing import Optional

class PanelCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    user_id: int  # presupunem că e trimis din frontend momentan

class PanelResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    user_id: int

    class Config:
        orm_mode = True
