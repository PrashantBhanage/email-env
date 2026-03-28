"""Grading logic for Email Triage Environment."""

from typing import Any


def grade_action(
    predicted_category: str,
    predicted_priority: str,
    predicted_action: str,
    expected_category: str,
    expected_priority: str,
    expected_action: str
) -> dict[str, Any]:
    """
    Grade an agent's action against expected values.
    
    Scoring:
    - correct category = +0.4
    - correct priority = +0.3
    - correct action = +0.3
    
    Returns dict with:
    - category_correct: bool
    - priority_correct: bool
    - action_correct: bool
    - score: float (0.0 to 1.0, rounded to 2 decimals)
    """
    category_correct = predicted_category.lower() == expected_category.lower()
    priority_correct = predicted_priority.lower() == expected_priority.lower()
    action_correct = predicted_action.lower() == expected_action.lower()
    
    score = 0.0
    if category_correct:
        score += 0.4
    if priority_correct:
        score += 0.3
    if action_correct:
        score += 0.3
    
    # Round to 2 decimal places
    score = round(score, 2)
    
    return {
        "category_correct": category_correct,
        "priority_correct": priority_correct,
        "action_correct": action_correct,
        "score": score,
        "expected": {
            "category": expected_category,
            "priority": expected_priority,
            "action": expected_action
        },
        "predicted": {
            "category": predicted_category,
            "priority": predicted_priority,
            "action": predicted_action
        }
    }
