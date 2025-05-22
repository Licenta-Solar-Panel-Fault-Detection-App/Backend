from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, func, case, literal_column, column
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import async_session
from models.panel_check import PanelCheck
from models.report import Report
from models.panel import SolarPanel
from schemas.check import CheckResponse
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

async def get_session():
    async with async_session() as session:
        yield session


from sqlalchemy import text

from sqlalchemy import text

@router.get("/stats/{user_id}")
async def get_dashboard_stats(user_id: int, session: AsyncSession = Depends(get_session)):
    try:
        # Query per model
        model_query = text("""
            SELECT 
                panelcheck.model, 
                COUNT(panelcheck.id) AS total, 
                SUM(CASE WHEN report.id IS NOT NULL THEN 1 ELSE 0 END) AS reported
            FROM panelcheck
            LEFT JOIN solarpanel ON solarpanel.id = panelcheck.panel_id
            LEFT JOIN report ON report.panel_check_id = panelcheck.id
            WHERE (solarpanel.user_id = :user_id OR panelcheck.panel_id IS NULL)            GROUP BY panelcheck.model
        """)

        result = await session.execute(model_query, {"user_id": user_id})
        model_data = result.all()

        # Query total
        total_query = text("""
            SELECT 
                COUNT(panelcheck.id), 
                SUM(CASE WHEN report.id IS NOT NULL THEN 1 ELSE 0 END)
            FROM panelcheck
            LEFT JOIN solarpanel ON solarpanel.id = panelcheck.panel_id
            LEFT JOIN report ON report.panel_check_id = panelcheck.id
            WHERE (solarpanel.user_id = :user_id OR panelcheck.panel_id IS NULL)        """)

        total_result = await session.execute(total_query, {"user_id": user_id})
        total_predictions, total_reported = total_result.one()

        return {
            "total_predictions": total_predictions or 0,
            "total_reported": total_reported or 0,
            "models": {
                str(model): {"total": total, "reported": reported or 0}
                for model, total, reported in model_data
            }
        }

    except Exception as e:
        logger.exception(f"Error in get_dashboard_stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")




from sqlalchemy import text

@router.get("/predictions", response_model=List[Dict[str, Any]])
async def get_predictions_filtered(
    user_id: int,
    reported: Optional[bool] = Query(None),
    model: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session)
):
    try:
        # Bază query SQL
        base_sql = """
            SELECT 
                panelcheck.id, 
                panelcheck.panel_id, 
                panelcheck.timestamp, 
                panelcheck.model, 
                panelcheck.status, 
                panelcheck.image_path, 
                report.id AS report_id,
                report.description
            FROM panelcheck
            LEFT JOIN solarpanel ON solarpanel.id = panelcheck.panel_id
            LEFT JOIN report ON report.panel_check_id = panelcheck.id
            WHERE (solarpanel.user_id = :user_id OR panelcheck.panel_id IS NULL)
        """

        # Adăugăm dynamic WHERE filters
        conditions = []
        params = {"user_id": user_id}

        if reported is not None:
            conditions.append("report.id IS NOT NULL" if reported else "report.id IS NULL")

        if model:
            conditions.append("panelcheck.model = :model")
            params["model"] = model

        # Concatenează condițiile suplimentare
        if conditions:
            base_sql += " AND " + " AND ".join(conditions)

        stmt = text(base_sql)

        result = await session.execute(stmt, params)
        rows = result.fetchall()

        predictions = []
        for row in rows:
            predictions.append({
                "id": row.id,
                "panel_id": row.panel_id,
                "timestamp": row.timestamp,
                "model": row.model,
                "status": row.status,
                "image_path": row.image_path,
                "report_id": row.report_id,
                "description": row.description
            })

        return predictions

    except Exception as e:
        logger.exception(f"Error in get_predictions_filtered: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

