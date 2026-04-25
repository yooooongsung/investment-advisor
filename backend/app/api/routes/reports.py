from fastapi import APIRouter, HTTPException, Query
from app.core.databricks import execute_query

router = APIRouter()

@router.get("/latest")
async def get_latest_report():
    try:
        query = """
        SELECT report_title, recommendations, created_at, day_of_week
        FROM default.investment_reports
        ORDER BY created_at DESC
        LIMIT 1
        """
        results = execute_query(query)
        if not results:
            return {"message": "No reports available"}
        return results[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"리포트 조회 실패: {str(e)}")

@router.get("/history")
async def get_report_history(days: int = Query(7, ge=1, le=30)):
    try:
        query = f"""
        SELECT report_title, recommendations, created_at, day_of_week
        FROM default.investment_reports
        ORDER BY created_at DESC
        LIMIT {days}
        """
        results = execute_query(query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"리포트 이력 조회 실패: {str(e)}")
