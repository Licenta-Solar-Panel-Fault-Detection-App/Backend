from http.client import HTTPException

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from database.database import async_session
from models.panel_check import PanelCheck
from models.report import Report
from schemas.check import CheckCreate, CheckResponse
from typing import List, Dict, Any, Optional
from datetime import datetime
from models.panel import SolarPanel

router = APIRouter(prefix="/checks", tags=["checks"])

async def get_session():
    async with async_session() as session:
        yield session

@router.post("/", response_model=CheckResponse)
async def create_check(check: CheckCreate, session: AsyncSession = Depends(get_session)):
    check_data = check.dict()
    if not check_data["timestamp"]:
        check_data["timestamp"] = datetime.utcnow()
    check_record = PanelCheck(**check_data)
    session.add(check_record)
    await session.commit()
    await session.refresh(check_record)
    return check_record

@router.get("/panel/{panel_id}", response_model=List[CheckResponse])
async def get_checks_for_panel(panel_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(PanelCheck).where(PanelCheck.panel_id == panel_id))
    return result.scalars().all()

@router.delete("/delete/{check_id}")
async def delete_check(check_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(PanelCheck).where(PanelCheck.id == check_id))
    check = result.scalar_one_or_none()
    if not check:
        raise HTTPException(status_code=404, detail="Check not found")

    await session.delete(check)
    await session.commit()
    return {"message": "Check deleted"}

@router.get("/last-status/{panel_id}")
async def get_last_status_by_panel(panel_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(PanelCheck).where(PanelCheck.panel_id == panel_id).order_by(desc(PanelCheck.timestamp)).limit(1)
    )
    check = result.scalar_one_or_none()
    if not check:
        return {"status": "Not-Verified", "timestamp": None}  # no check yet
    return {"status": check.status, "timestamp": check.timestamp}

