"""FastAPI application for Email Triage Environment - Premium Landing Page + API Backend."""

import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel

from environment.env import EmailTriageEnv
from environment.models import Action, Observation, StepResult, ResetResult
from environment.utils import get_task_summary


# Global environment instance
env = EmailTriageEnv()

# FastAPI app
app = FastAPI(
    title="Email Triage Environment",
    version="1.0.0",
    description="AI-Powered Email Classification & Smart Triage API"
)

# Setup templates and static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Mount static files if directory exists
static_dir = os.path.join(BASE_DIR, "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


class ResetRequest(BaseModel):
    """Request body for /reset endpoint."""
    task_id: Optional[str] = None


class StepRequest(BaseModel):
    """Request body for /step endpoint."""
    category: str
    priority: str
    action: str


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Render the premium animated landing page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
def health():
    """Health/status endpoint returning JSON."""
    return {
        "status": "ok",
        "name": "Email Triage Environment",
        "version": "1.0.0"
    }


@app.post("/reset")
def reset(request: Optional[ResetRequest] = None):
    """Reset the environment with an optional task_id.
    
    Returns a ResetResult with wrapped observation for OpenEnv validator compatibility.
    """
    try:
        task_id = request.task_id if request else None
        observation = env.reset(task_id=task_id)
        result = ResetResult(observation=observation)
        return JSONResponse(content=result.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/step")
def step(request: StepRequest):
    """Take an action and receive the result."""
    try:
        action = Action(
            category=request.category,
            priority=request.priority,
            action=request.action
        )
        result = env.step(action)
        return JSONResponse(content=result.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/state")
def state():
    """Get current environment state."""
    return env.state()


@app.get("/tasks")
def tasks():
    """Get list of available tasks."""
    return get_task_summary()


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)