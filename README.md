# Email Triage Env

A lightweight AI agent environment for email triage classification. The agent receives business/customer emails and must classify the email category, assign priority, and choose the correct action.

## Overview

This environment simulates a real-world business workflow: email triage. An AI agent receives an email and must make three decisions:

1. **Category** - Is this billing, technical, or general inquiry?
2. **Priority** - Is this low, medium, or high urgency?
3. **Action** - Should we reply, escalate, or ignore?

## Why This Environment Matters

Email triage is a common business operations task. Automating this with AI can:
- Reduce response times for urgent issues
- Route emails to the right teams automatically
- Improve customer satisfaction through faster resolution
- Free up human agents for complex cases

This environment provides a clean, reproducible benchmark for testing AI agent performance on classification tasks.

## Environment Design

### Observation Space

After calling `reset()`, the agent receives an observation:

```python
{
    "task_id": "task_001",
    "email_text": "I forgot my password and cannot log in.",
    "sender_type": "customer",
    "possible_categories": ["billing", "technical", "general"],
    "possible_priorities": ["low", "medium", "high"],
    "possible_actions": ["reply", "escalate", "ignore"],
    "difficulty": "easy",
    "step_count": 0,
    "last_action_error": False,
    "message": None
}
```

### Action Space

The agent must respond with:

```python
{
    "category": "technical",  # billing, technical, general
    "priority": "low",          # low, medium, high
    "action": "reply"          # reply, escalate, ignore
}
```

### Reward Logic

Scoring is deterministic with partial credit:

- Correct category: **+0.4**
- Correct priority: **+0.3**
- Correct action: **+0.3**
- Invalid action: **-0.5**

Maximum score: **1.0** (perfect classification)
Minimum score: **0.0**

### Episode Flow

1. Call `reset(task_id)` to load a task
2. Agent analyzes the email
3. Agent calls `step(action)` with classification
4. Environment returns score and grading details
5. Episode ends (single-step environment)

## Tasks

| ID | Difficulty | Email | Expected |
|----|------------|-------|----------|
| task_001 | Easy | "I forgot my password and cannot log in." | technical / low / reply |
| task_002 | Easy | "What are your support hours on weekends?" | general / low / reply |
| task_003 | Medium | "I was charged twice for my monthly subscription." | billing / high / escalate |
| task_004 | Medium | "The app crashes every time I upload a PDF." | technical / medium / escalate |
| task_005 | Hard | "I requested a refund 10 days ago and still haven't received it. This is unacceptable." | billing / high / escalate |

## Project Structure

```
email-triage-env/
├── app.py              # FastAPI server
├── inference.py        # Baseline OpenAI inference
├── openenv.yaml        # Environment metadata
├── Dockerfile          # Container build
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── .env.example        # Environment variables template
├── environment/
│   ├── __init__.py
│   ├── env.py          # Main environment class
│   ├── models.py       # Pydantic models
│   ├── tasks.py        # Task loading
│   ├── graders.py      # Scoring logic
│   └── utils.py        # Utilities
├── data/
│   └── emails.json     # Task definitions
└── tests/
    ├── test_env.py
    ├── test_tasks.py
    └── test_graders.py
```

## Local Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the API server
uvicorn app:app --host 0.0.0.0 --port 7860
```

## API Usage

### Health Check

```bash
curl http://localhost:7860/
```

### Reset Environment

```bash
# Reset with specific task
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": "task_001"}'

# Reset with next task
curl -X POST http://localhost:7860/reset
```

### Take Action

```bash
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{"category": "technical", "priority": "low", "action": "reply"}'
```

### Get Environment State

```bash
curl http://localhost:7860/state
```

### List Tasks

```bash
curl http://localhost:7860/tasks
```

## Baseline Inference

Run the baseline OpenAI inference script:

```bash
# Set environment variables
export OPENAI_API_KEY="your-api-key"
export API_BASE_URL="https://api.openai.com/v1"  # or your custom endpoint
export MODEL_NAME="gpt-4o-mini"

# Run inference
python inference.py
```

This will:
1. Load all 5 tasks
2. Run each through the configured OpenAI model
3. Score each response
4. Print detailed results and average score

## Docker

### Build Image

```bash
docker build -t email-triage-env .
```

### Run Container

```bash
docker run -p 7860:7860 email-triage-env
```

### Hugging Face Spaces Deployment

1. Push the project to a GitHub repository
2. Create a new Space on Hugging Face
3. Select "Docker" as the SDK
4. Point to your GitHub repo
5. The Dockerfile will be used to build the Space

## Testing

```bash
pytest tests/ -v
```

## Notes

- **Deterministic Grading**: Same action always produces the same score
- **Lightweight**: Runs on 2 vCPU / 8 GB RAM
- **Single-Step Episodes**: One email, one decision, one score
- **No External Dependencies**: Uses only standard libraries + minimal packages
- **API-First Design**: Can be used via HTTP or imported directly
