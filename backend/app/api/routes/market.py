from fastapi import APIRouter, HTTPException
from app.core.databricks import execute_query

router = APIRouter()

@router.get("/summary")
async def get_market_summary():
    try:
        query = """
        SELECT market, date, close, rsi, daily_return, signal
        FROM default.market_signals_summary
        ORDER BY date DESC
        LIMIT 4
        """
        results = execute_query(query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"시장 데이터 조회 실패: {str(e)}")

@router.get("/details/{symbol}")
async def get_market_details(symbol: str):
    try:
        # Map symbol to table name
        table_mapping = {
            "KOSPI": "kospi_index_processed",
            "KOSDAQ": "kosdaq_index_processed",
            "NASDAQ": "nasdaq_index_processed",
            "Bitcoin": "bitcoin_processed"
        }
        
        table_name = table_mapping.get(symbol)
        if not table_name:
            raise HTTPException(status_code=404, detail="Invalid market symbol")
        
        query = f"""
        SELECT date, close, ma5, ma20, rsi, volatility, daily_return
        FROM default.{table_name}
        ORDER BY date DESC
        LIMIT 30
        """
        results = execute_query(query)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"상세 데이터 조회 실패: {str(e)}")
