from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from database.database import async_session
from models.panel_check import PanelCheck
from schemas.check import CheckCreate, CheckResponse
from typing import List
from datetime import datetime

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
