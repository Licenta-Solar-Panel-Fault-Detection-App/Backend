from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import desc
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import async_session
from models import PanelCheck
from models.report import Report
from sqlmodel import select
from schemas.report import ReportCreate, ReportUpdate, ReportDelete

router = APIRouter(prefix="/reports", tags=["reports"])

async def get_session():
    async with async_session() as session:
        yield session


@router.post("/add")
async def create_report(data: ReportCreate, session: AsyncSession = Depends(get_session)):
    existing = await session.execute(select(Report).where(Report.panel_check_id == data.panel_check_id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="A report already exists for this check.")

    report = Report(
        panel_check_id=data.panel_check_id,
        user_id=data.user_id,
        description=data.description
    )
    session.add(report)
    await session.commit()
    await session.refresh(report)
    return report

@router.put("/update/{report_id}")
async def update_report(report_id: int, data: ReportUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    report.description = data.description
    report.timestamp = datetime.utcnow()
    session.add(report)
    await session.commit()
    return {"message": "Report updated"}

@router.delete("/delete/{report_id}")
async def delete_report(report_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Report).where(Report.id == report_id))
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    await session.delete(report)
    await session.commit()
    return {"message": "Report deleted"}

@router.get("/user/{user_id}")
async def get_reports_by_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Report).where(Report.user_id == user_id))
    return result.scalars().all()


@router.get("/check/{check_id}")
async def get_report_by_check(check_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Report).where(Report.panel_check_id == check_id))
    report = result.scalar_one_or_none()
    return report


