"""Tests for EmailTriageEnv environment."""

import pytest
from environment.env import EmailTriageEnv
from environment.models import Action, ResetResult


class TestEmailTriageEnv:
    """Test suite for EmailTriageEnv."""
    
    def test_reset_returns_valid_observation(self):
        """Test that reset returns a valid observation."""
        env = EmailTriageEnv()
        obs = env.reset()
        
        assert obs.task_id is not None
        assert obs.email_text is not None
        assert obs.sender_type is not None
        assert obs.difficulty in ["easy", "medium", "hard"]
        assert obs.step_count == 0
        assert obs.last_action_error is False
    
    def test_reset_with_specific_task(self):
        """Test reset with a specific task ID."""
        env = EmailTriageEnv()
        obs = env.reset(task_id="task_001")
        
        assert obs.task_id == "task_001"
        assert obs.email_text == "I forgot my password and cannot log in."
    
    def test_step_returns_score_in_range(self):
        """Test that step returns a score between 0.0 and 1.0."""
        env = EmailTriageEnv()
        env.reset(task_id="task_001")
        
        # Correct action
        action = Action(category="technical", priority="low", action="reply")
        result = env.step(action)
        
        assert 0.0 <= result.reward <= 1.0
        assert result.done is True
    
    def test_invalid_action_gets_penalty(self):
        """Test that invalid action values get -0.5 penalty."""
        env = EmailTriageEnv()
        env.reset(task_id="task_001")
        
        # Invalid category
        action = Action(category="invalid_category", priority="low", action="reply")
        result = env.step(action)
        
        assert result.reward == -0.5
        assert result.observation.last_action_error is True
        assert result.done is False
    
    def test_partial_credit_scoring(self):
        """Test that partial credit is given for correct components."""
        env = EmailTriageEnv()
        env.reset(task_id="task_001")
        
        # Only correct category
        action = Action(category="technical", priority="high", action="ignore")
        result = env.step(action)
        
        # Should get 0.4 for category, nothing for priority/action
        assert result.reward == 0.4
        assert result.info["category_correct"] is True
        assert result.info["priority_correct"] is False
        assert result.info["action_correct"] is False
    
    def test_state_returns_internal_state(self):
        """Test that state() returns internal state dict."""
        env = EmailTriageEnv()
        env.reset(task_id="task_001")
        
        state = env.state()
        
        assert "task_id" in state
        assert "step_count" in state
        assert "done" in state
        assert "last_action_error" in state
    
    def test_episode_done_after_step(self):
        """Test that episode is marked done after one step."""
        env = EmailTriageEnv()
        env.reset(task_id="task_001")
        
        action = Action(category="technical", priority="low", action="reply")
        result = env.step(action)
        
        assert result.done is True
        
        # Second step should return error
        result2 = env.step(action)
        assert result2.info.get("error") is not None
    
    def test_reset_clears_done_flag(self):
        """Test that reset clears the done flag."""
        env = EmailTriageEnv()
        env.reset(task_id="task_001")
        
        action = Action(category="technical", priority="low", action="reply")
        env.step(action)
        
        # Now reset
        env.reset(task_id="task_002")
        state = env.state()
        
        assert state["done"] is False
        assert state["step_count"] == 0
    
    def test_reset_result_wrapped_observation(self):
        """Test that reset returns a ResetResult with wrapped observation (OpenEnv compatible)."""
        env = EmailTriageEnv()
        obs = env.reset(task_id="task_001")
        
        # Wrap in ResetResult like the API does
        result = ResetResult(observation=obs)
        
        # Verify the structure
        assert "observation" in result.model_dump()
        assert result.observation.task_id == "task_001"
        assert result.observation.email_text is not None
        assert result.observation.possible_categories == ["billing", "technical", "general"]
        assert result.observation.possible_priorities == ["low", "medium", "high"]
        assert result.observation.possible_actions == ["reply", "escalate", "ignore"]
