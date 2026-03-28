"""Utility functions for Email Triage Environment."""

from environment.tasks import load_tasks


def get_task_summary() -> list[dict]:
    """Get a summary of all tasks (id and difficulty only)."""
    tasks = load_tasks()
    return [{"id": task["id"], "difficulty": task["difficulty"]} for task in tasks]


def get_task_count() -> int:
    """Get total number of available tasks."""
    return len(load_tasks())
