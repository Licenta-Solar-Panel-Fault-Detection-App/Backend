from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from .report import Report
from .models_enum import ModelEnum

if TYPE_CHECKING:
    from .panel import SolarPanel



class PanelCheck(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    panel_id: Optional[int] = Field(default=None, foreign_key="solarpanel.id")
    timestamp: datetime
    model: ModelEnum
    status: str
    image_path: Optional[str] = None

    panel: Optional["SolarPanel"] = Relationship(back_populates="checks")
    report: Optional["Report"] = Relationship(back_populates="panel_check")
