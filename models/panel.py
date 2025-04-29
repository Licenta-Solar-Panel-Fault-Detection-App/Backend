from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User
    from .panel_check import PanelCheck

class SolarPanel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    latitude: float
    longitude: float
    user_id: int = Field(foreign_key="user.id")

    user: Optional["User"] = Relationship(back_populates="panels")
    checks: List["PanelCheck"] = Relationship(back_populates="panel")
