"""Email Triage Environment - Main environment class."""

from typing import Optional, Union

from environment.models import Action, Observation, StepResult
from environment.tasks import get_task_by_id, get_next_task_id
from environment.graders import grade_action


class EmailTriageEnv:
    """
    Email Triage Environment for AI agent training.
    
    A single-step environment where the agent receives an email
    and must classify category, priority, and choose an action.
    """
    
    VALID_CATEGORIES = ["billing", "technical", "general"]
    VALID_PRIORITIES = ["low", "medium", "high"]
    VALID_ACTIONS = ["reply", "escalate", "ignore"]
    
    def __init__(self):
        """Initialize the environment."""
        self.current_task: Optional[dict] = None
        self.step_count: int = 0
        self.done: bool = False
        self.last_action_error: bool = False
    
    def reset(self, task_id: Optional[str] = None) -> Observation:
        """
        Reset the environment with a specific task or the next in sequence.
        
        Args:
            task_id: Optional specific task ID to load. If None, loads next task.
            
        Returns:
            Observation with task details.
        """
        if task_id is None:
            current_id = self.current_task["id"] if self.current_task else None
            task_id = get_next_task_id(current_id)
        
        self.current_task = get_task_by_id(task_id)
        if self.current_task is None:
            raise ValueError(f"Task not found: {task_id}")
        
        self.step_count = 0
        self.done = False
        self.last_action_error = False
        
        return self._build_observation()
    
    def step(self, action: Union[Action, dict]) -> StepResult:
        """
        Take an action and receive the result.
        
        Args:
            action: Action object or dict with category, priority, action
            
        Returns:
            StepResult with observation, reward, done flag, and info.
        """
        if self.done:
            return StepResult(
                observation=self._build_observation(),
                reward=0.0,
                done=True,
                info={"error": "Episode already done. Call reset() first."}
            )
        
        # Parse action
        if isinstance(action, dict):
            action = Action(**action)
        
        # Validate action values
        validation_error = self._validate_action(action)
        if validation_error:
            self.last_action_error = True
            return StepResult(
                observation=self._build_observation(message=validation_error),
                reward=-0.5,
                done=False,
                info={"validation_error": validation_error}
            )
        
        # Grade the action
        expected = self.current_task
        grading_result = grade_action(
            predicted_category=action.category,
            predicted_priority=action.priority,
            predicted_action=action.action,
            expected_category=expected["expected_category"],
            expected_priority=expected["expected_priority"],
            expected_action=expected["expected_action"]
        )
        
        self.done = True
        self.step_count += 1
        
        return StepResult(
            observation=self._build_observation(),
            reward=grading_result["score"],
            done=True,
            info=grading_result
        )
    
    def state(self) -> dict:
        """
        Get the raw internal state of the environment.
        
        Returns:
            Dict with current state information.
        """
        return {
            "task_id": self.current_task["id"] if self.current_task else None,
            "step_count": self.step_count,
            "done": self.done,
            "last_action_error": self.last_action_error
        }
    
    def close(self) -> None:
        """Clean up resources (no-op for this environment)."""
        pass
    
    def _build_observation(self, message: Optional[str] = None) -> Observation:
        """Build an observation from current state."""
        return Observation(
            task_id=self.current_task["id"],
            email_text=self.current_task["email_text"],
            sender_type=self.current_task["sender_type"],
            possible_categories=self.VALID_CATEGORIES,
            possible_priorities=self.VALID_PRIORITIES,
            possible_actions=self.VALID_ACTIONS,
            difficulty=self.current_task["difficulty"],
            step_count=self.step_count,
            last_action_error=self.last_action_error,
            message=message
        )
    
    def _validate_action(self, action: Action) -> Optional[str]:
        """Validate action values. Returns error message or None."""
        if action.category.lower() not in self.VALID_CATEGORIES:
            return f"Invalid category: {action.category}. Must be one of {self.VALID_CATEGORIES}"
        if action.priority.lower() not in self.VALID_PRIORITIES:
            return f"Invalid priority: {action.priority}. Must be one of {self.VALID_PRIORITIES}"
        if action.action.lower() not in self.VALID_ACTIONS:
            return f"Invalid action: {action.action}. Must be one of {self.VALID_ACTIONS}"
        return None
