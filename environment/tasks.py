"""Task loading and management for Email Triage Environment."""

import json
from pathlib import Path
from typing import Optional


def load_tasks() -> list[dict]:
    """Load all tasks from data/emails.json."""
    data_path = Path(__file__).parent.parent / "data" / "emails.json"
    with open(data_path, "r") as f:
        return json.load(f)


def get_task_by_id(task_id: str) -> Optional[dict]:
    """Get a specific task by ID."""
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def get_all_task_ids() -> list[str]:
    """Get all available task IDs."""
    tasks = load_tasks()
    return [task["id"] for task in tasks]


def get_next_task_id(current_id: Optional[str] = None) -> str:
    """Get the next task ID in sequence."""
    tasks = load_tasks()
    task_ids = [task["id"] for task in tasks]
    
    if current_id is None or current_id not in task_ids:
        return task_ids[0]
    
    current_idx = task_ids.index(current_id)
    next_idx = (current_idx + 1) % len(task_ids)
    return task_ids[next_idx]
