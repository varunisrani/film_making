from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any, Union
import json
import os
from dotenv import load_dotenv

# Import our agent modules
from agents.script_ingestion_agent import ScriptIngestionAgent
from agents.scheduling_agent import SchedulingAgent
from agents.budgeting_agent import BudgetingAgent
from agents.one_liner_agent import OneLinerAgent
from agents.character_agent import CharacterAgent
from agents.system_sync_agent import SystemSyncAgent

# Import logging utilities
from utils.logging_utils import get_api_logs, get_api_stats, clear_api_logs

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Film Production AI API",
    description="API for the Film Production AI Assistant",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:8000",
        "https://film-making.vercel.app",
        "https://film-making-app.vercel.app",
        "https://film-making.onrender.com",
        "https://film-making2.vercel.app"

    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    expose_headers=["Content-Length"],
    max_age=600,  # Cache preflight requests for 10 minutes
)

# Initialize agents
script_agent = ScriptIngestionAgent()
scheduling_agent = SchedulingAgent()
budgeting_agent = BudgetingAgent()
one_liner_agent = OneLinerAgent()
character_agent = CharacterAgent()
system_sync_agent = SystemSyncAgent()

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(__file__), "data", "logs")
os.makedirs(logs_dir, exist_ok=True)

# Pydantic models for request/response
class ScriptRequest(BaseModel):
    script_text: str

class ScriptResponse(BaseModel):
    scenes: List[Dict[str, Any]]

class ScheduleResponse(BaseModel):
    shooting_days: List[Dict[str, Any]]

class BudgetResponse(BaseModel):
    total_budget: float
    per_day_average: float
    contingency: float
    days: List[Dict[str, Any]]

class OneLinerResponse(BaseModel):
    scenes: List[Dict[str, Any]]

class CharacterResponse(BaseModel):
    characters: List[Dict[str, Any]]

class SystemSyncResponse(BaseModel):
    total_scenes: int
    shooting_days: int
    total_budget: float
    start_date: str
    end_date: str
    sync_status: Dict[str, str]

class ApiStats(BaseModel):
    total_calls: int
    success_rate: float
    avg_duration: float
    providers: Dict[str, int]
    models: Dict[str, int]

class ApiLog(BaseModel):
    provider: str
    model: str
    timestamp: str
    status: str
    duration: float
    prompt_length: int
    response_length: int
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

# API endpoints
@app.post("/api/script", response_model=ScriptResponse)
async def analyze_script(request: ScriptRequest):
    try:
        script_analysis = script_agent.process(request.script_text)
        return script_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/schedule", response_model=ScheduleResponse)
async def create_schedule(script_analysis: Dict[str, Any]):
    try:
        schedule_data = scheduling_agent.process(script_analysis)
        return schedule_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/budget", response_model=BudgetResponse)
async def create_budget(data: Dict[str, Any]):
    try:
        budget_data = budgeting_agent.process(
            data["script_analysis"],
            data["schedule"]
        )
        return budget_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/one-liners", response_model=OneLinerResponse)
async def create_one_liners(script_analysis: Dict[str, Any]):
    try:
        one_liner_data = one_liner_agent.process(script_analysis)
        return one_liner_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/characters", response_model=CharacterResponse)
async def analyze_characters(script_analysis: Dict[str, Any]):
    try:
        character_data = character_agent.process(script_analysis)
        return character_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/system-sync", response_model=SystemSyncResponse)
async def sync_system(data: Dict[str, Any]):
    try:
        system_data = system_sync_agent.process(
            data["script_analysis"],
            data["schedule"],
            data["budget"],
            data["one_liners"],
            data["characters"]
        )
        return system_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logs/stats", response_model=ApiStats)
async def get_stats():
    try:
        stats = get_api_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logs", response_model=List[ApiLog])
async def get_logs():
    try:
        logs = get_api_logs()
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/logs")
async def clear_logs():
    try:
        clear_api_logs()
        return {"message": "Logs cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload-script")
async def upload_script(file: UploadFile = File(...)):
    try:
        content = await file.read()
        script_text = content.decode("utf-8")
        script_analysis = script_agent.process(script_text)
        return script_analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
