"""FastAPI application for Email Triage Environment."""

from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from environment.env import EmailTriageEnv
from environment.models import Action, Observation, StepResult
from environment.utils import get_task_summary


# Global environment instance
env = EmailTriageEnv()

# FastAPI app
app = FastAPI(title="Email Triage Environment", version="1.0.0")


class ResetRequest(BaseModel):
    """Request body for /reset endpoint."""
    task_id: Optional[str] = None


class StepRequest(BaseModel):
    """Request body for /step endpoint."""
    category: str
    priority: str
    action: str


@app.get("/")
def root():
    """Health/status endpoint."""
    return {
        "status": "ok",
        "name": "Email Triage Environment",
        "version": "1.0.0"
    }


@app.post("/reset", response_model=Observation)
def reset(request: Optional[ResetRequest] = None):
    """Reset the environment with an optional task_id."""
    try:
        task_id = request.task_id if request else None
        observation = env.reset(task_id=task_id)
        return observation
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
    uvicorn.run(app, host="0.0.0.0", port=7860)
