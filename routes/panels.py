from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from database.database import async_session
from models.panel import SolarPanel
from schemas.panel import PanelCreate, PanelResponse
from typing import List

router = APIRouter(prefix="/panels", tags=["panels"])

async def get_session():
    async with async_session() as session:
        yield session

@router.post("/add", response_model=PanelResponse)
async def create_panel(panel_data: PanelCreate, session: AsyncSession = Depends(get_session)):
    panel = SolarPanel(**panel_data.dict())
    session.add(panel)
    await session.commit()
    await session.refresh(panel)
    return panel

@router.get("/get/{user_id}", response_model=List[PanelResponse])
async def get_panels_by_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(SolarPanel).where(SolarPanel.user_id == user_id).order_by(SolarPanel.id))
    panels = result.scalars().all()
    return panels

@router.put("/edit/{panel_id}", response_model=PanelResponse)
async def update_panel(panel_id: int, panel_data: PanelCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(SolarPanel).where(SolarPanel.id == panel_id))
    panel = result.scalar_one_or_none()
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")

    for key, value in panel_data.dict().items():
        setattr(panel, key, value)

    session.add(panel)
    await session.commit()
    await session.refresh(panel)
    return panel

@router.delete("/delete/{panel_id}", response_model=PanelResponse)
async def update_panel(panel_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(SolarPanel).where(SolarPanel.id == panel_id))
    panel = result.scalar_one_or_none()
    if not panel:
        raise HTTPException(status_code=404, detail="Panel not found")
    await session.delete(panel)
    await session.commit()
    return panel

