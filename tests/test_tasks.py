"""Tests for task loading."""

import pytest
from environment.tasks import load_tasks, get_task_by_id, get_all_task_ids, get_next_task_id


class TestTaskLoading:
    """Test suite for task loading functions."""
    
    def test_load_tasks_returns_list(self):
        """Test that load_tasks returns a list."""
        tasks = load_tasks()
        assert isinstance(tasks, list)
        assert len(tasks) >= 5
    
    def test_load_tasks_has_required_fields(self):
        """Test that each task has required fields."""
        tasks = load_tasks()
        
        for task in tasks:
            assert "id" in task
            assert "email_text" in task
            assert "sender_type" in task
            assert "expected_category" in task
            assert "expected_priority" in task
            assert "expected_action" in task
            assert "difficulty" in task
    
    def test_get_task_by_id(self):
        """Test getting a specific task by ID."""
        task = get_task_by_id("task_001")
        
        assert task is not None
        assert task["id"] == "task_001"
        assert task["expected_category"] == "technical"
        assert task["expected_priority"] == "low"
        assert task["expected_action"] == "reply"
    
    def test_get_task_by_invalid_id(self):
        """Test getting a non-existent task returns None."""
        task = get_task_by_id("nonexistent_task")
        assert task is None
    
    def test_get_all_task_ids(self):
        """Test getting all task IDs."""
        task_ids = get_all_task_ids()
        
        assert isinstance(task_ids, list)
        assert len(task_ids) >= 5
        assert "task_001" in task_ids
        assert "task_005" in task_ids
    
    def test_get_next_task_id(self):
        """Test getting next task ID in sequence."""
        next_id = get_next_task_id("task_001")
        assert next_id == "task_002"
    
    def test_get_next_task_id_wraps(self):
        """Test that next task wraps to first after last."""
        task_ids = get_all_task_ids()
        last_id = task_ids[-1]
        
        next_id = get_next_task_id(last_id)
        assert next_id == task_ids[0]
    
    def test_get_next_task_id_first_if_none(self):
        """Test that first task is returned if current is None."""
        next_id = get_next_task_id(None)
        assert next_id == "task_001"
    
    def test_all_difficulties_present(self):
        """Test that all difficulty levels are present."""
        tasks = load_tasks()
        difficulties = {task["difficulty"] for task in tasks}
        
        assert "easy" in difficulties
        assert "medium" in difficulties
        assert "hard" in difficulties
