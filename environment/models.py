"""Pydantic models for Email Triage Environment."""

from typing import Optional
from pydantic import BaseModel, Field


class Observation(BaseModel):
    """Observation returned by the environment after reset or step."""
    task_id: str
    email_text: str
    sender_type: str
    possible_categories: list[str] = Field(default_factory=lambda: ["billing", "technical", "general"])
    possible_priorities: list[str] = Field(default_factory=lambda: ["low", "medium", "high"])
    possible_actions: list[str] = Field(default_factory=lambda: ["reply", "escalate", "ignore"])
    difficulty: str
    step_count: int = 0
    last_action_error: bool = False
    message: Optional[str] = None


class Action(BaseModel):
    """Action taken by the agent."""
    category: str
    priority: str
    action: str


class StepResult(BaseModel):
    """Result returned after taking an action."""
    observation: Observation
    reward: float
    done: bool
    info: dict = Field(default_factory=dict)
