from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from .panel_check import PanelCheck
    from .user import User

class Report(SQLModel, table=True):
    id: Optional[int]= Field(default=None, primary_key=True)
    panel_check_id: int = Field(foreign_key="panelcheck.id", unique=True)
    user_id: Optional[int] = Field(foreign_key="user.id")
    description: Optional[str]= None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    panel_check: Optional["PanelCheck"] = Relationship(back_populates="report")
    user: Optional["User"] = Relationship()


