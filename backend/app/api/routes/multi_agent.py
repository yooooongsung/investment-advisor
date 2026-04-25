from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter()

# Databricks 설정 (환경 변수에서 로드)
DATABRICKS_HOST = os.getenv("DATABRICKS_SERVER_HOSTNAME", "https://dbc-00f9187e-c67a.cloud.databricks.com")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_ACCESS_TOKEN")
MULTI_AGENT_JOB_ID = "32251191378772"

@router.post("/trigger")
async def trigger_multi_agent():
    """Multi Agent AI 분석 실행"""
    try:
        if not DATABRICKS_TOKEN:
            raise HTTPException(status_code=500, detail="Databricks token not configured")
        
        url = f"https://{DATABRICKS_HOST}/api/2.1/jobs/run-now"
        headers = {
            "Authorization": f"Bearer {DATABRICKS_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {"job_id": int(MULTI_AGENT_JOB_ID)}
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            return {
                "status": "success",
                "message": "AI 분석이 시작되었습니다!",
                "run_id": result.get("run_id")
            }
        else:
            raise HTTPException(status_code=500, detail="Job trigger failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 분석 실행 실패: {str(e)}")

@router.get("/status/{run_id}")
async def get_multi_agent_status(run_id: int):
    """Multi Agent 실행 상태 조회"""
    try:
        if not DATABRICKS_TOKEN:
            raise HTTPException(status_code=500, detail="Databricks token not configured")
        
        url = f"https://{DATABRICKS_HOST}/api/2.1/jobs/runs/get"
        headers = {"Authorization": f"Bearer {DATABRICKS_TOKEN}"}
        params = {"run_id": run_id}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            result = response.json()
            state = result.get("state", {})
            return {
                "run_id": run_id,
                "life_cycle_state": state.get("life_cycle_state"),
                "result_state": state.get("result_state"),
                "state_message": state.get("state_message")
            }
        else:
            raise HTTPException(status_code=500, detail="Status check failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"상태 조회 실패: {str(e)}")
