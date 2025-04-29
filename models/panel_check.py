from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from .panel import SolarPanel

class PanelCheck(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    panel_id: int = Field(foreign_key="solarpanel.id")
    timestamp: datetime
    status: str
    image_path: Optional[str] = None

    panel: Optional["SolarPanel"] = Relationship(back_populates="checks")
