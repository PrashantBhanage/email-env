"""Tests for grading logic."""

import pytest
from environment.graders import grade_action


class TestGrading:
    """Test suite for grading functions."""
    
    def test_perfect_score(self):
        """Test that perfect action gets 1.0."""
        result = grade_action(
            predicted_category="technical",
            predicted_priority="low",
            predicted_action="reply",
            expected_category="technical",
            expected_priority="low",
            expected_action="reply"
        )
        
        assert result["score"] == 1.0
        assert result["category_correct"] is True
        assert result["priority_correct"] is True
        assert result["action_correct"] is True
    
    def test_only_category_correct(self):
        """Test score when only category is correct."""
        result = grade_action(
            predicted_category="technical",
            predicted_priority="high",
            predicted_action="ignore",
            expected_category="technical",
            expected_priority="low",
            expected_action="reply"
        )
        
        assert result["score"] == 0.4
        assert result["category_correct"] is True
        assert result["priority_correct"] is False
        assert result["action_correct"] is False
    
    def test_only_priority_correct(self):
        """Test score when only priority is correct."""
        result = grade_action(
            predicted_category="general",
            predicted_priority="low",
            predicted_action="ignore",
            expected_category="technical",
            expected_priority="low",
            expected_action="reply"
        )
        
        assert result["score"] == 0.3
        assert result["category_correct"] is False
        assert result["priority_correct"] is True
        assert result["action_correct"] is False
    
    def test_only_action_correct(self):
        """Test score when only action is correct."""
        result = grade_action(
            predicted_category="general",
            predicted_priority="high",
            predicted_action="reply",
            expected_category="technical",
            expected_priority="low",
            expected_action="reply"
        )
        
        assert result["score"] == 0.3
        assert result["category_correct"] is False
        assert result["priority_correct"] is False
        assert result["action_correct"] is True
    
    def test_category_and_priority_correct(self):
        """Test score when category and priority are correct."""
        result = grade_action(
            predicted_category="technical",
            predicted_priority="low",
            predicted_action="ignore",
            expected_category="technical",
            expected_priority="low",
            expected_action="reply"
        )
        
        assert result["score"] == 0.7
        assert result["category_correct"] is True
        assert result["priority_correct"] is True
        assert result["action_correct"] is False
    
    def test_category_and_action_correct(self):
        """Test score when category and action are correct."""
        result = grade_action(
            predicted_category="technical",
            predicted_priority="high",
            predicted_action="reply",
            expected_category="technical",
            expected_priority="low",
            expected_action="reply"
        )
        
        assert result["score"] == 0.7
        assert result["category_correct"] is True
        assert result["priority_correct"] is False
        assert result["action_correct"] is True
    
    def test_priority_and_action_correct(self):
        """Test score when priority and action are correct."""
        result = grade_action(
            predicted_category="general",
            predicted_priority="low",
            predicted_action="reply",
            expected_category="technical",
            expected_priority="low",
            expected_action="reply"
        )
        
        assert result["score"] == 0.6
        assert result["category_correct"] is False
        assert result["priority_correct"] is True
        assert result["action_correct"] is True
    
    def test_nothing_correct(self):
        """Test score when nothing is correct."""
        result = grade_action(
            predicted_category="general",
            predicted_priority="high",
            predicted_action="ignore",
            expected_category="technical",
            expected_priority="low",
            expected_action="reply"
        )
        
        assert result["score"] == 0.0
        assert result["category_correct"] is False
        assert result["priority_correct"] is False
        assert result["action_correct"] is False
    
    def test_case_insensitive(self):
        """Test that grading is case insensitive."""
        result = grade_action(
            predicted_category="TECHNICAL",
            predicted_priority="Low",
            predicted_action="REPLY",
            expected_category="technical",
            expected_priority="low",
            expected_action="reply"
        )
        
        assert result["score"] == 1.0
    
    def test_score_is_rounded_to_two_decimals(self):
        """Test that score is rounded to 2 decimal places."""
        result = grade_action(
            predicted_category="technical",
            predicted_priority="low",
            predicted_action="escalate",
            expected_category="technical",
            expected_priority="low",
            expected_action="reply"
        )
        
        # 0.4 + 0.3 = 0.7, should be formatted correctly
        assert isinstance(result["score"], float)
        assert result["score"] == 0.7
    
    def test_result_includes_expected_and_predicted(self):
        """Test that result includes expected and predicted values."""
        result = grade_action(
            predicted_category="billing",
            predicted_priority="high",
            predicted_action="escalate",
            expected_category="technical",
            expected_priority="low",
            expected_action="reply"
        )
        
        assert "expected" in result
        assert "predicted" in result
        assert result["expected"]["category"] == "technical"
        assert result["predicted"]["category"] == "billing"
