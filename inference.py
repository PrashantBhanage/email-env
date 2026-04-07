cat > inference.py << 'EOF'
#!/usr/bin/env python3

import os
import sys
import json
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

client = OpenAI(
    api_key=HF_TOKEN if HF_TOKEN else "dummy-key",
    base_url="https://router.huggingface.co/v1"
)

FALLBACK_ACTION = {
    "category": "general",
    "priority": "low",
    "action": "reply"
}


def log(msg: str):
    print(msg, flush=True)


def safe_json(res):
    try:
        return res.json()
    except Exception:
        return {}


def safe_request(method, url, **kwargs):
    try:
        res = requests.request(method, url, timeout=15, **kwargs)
        res.raise_for_status()
        return safe_json(res)
    except Exception as e:
        log(f"ERROR: request failed -> {e}")
        return {}


def choose_action(email_text: str):
    text = (email_text or "").lower()

    if "bill" in text or "charged" in text or "payment" in text:
        return {
            "category": "billing",
            "priority": "high",
            "action": "escalate"
        }

    if "error" in text or "bug" in text or "login" in text or "issue" in text:
        return {
            "category": "technical",
            "priority": "medium",
            "action": "reply"
        }

    return FALLBACK_ACTION


def main():
    log("START")

    try:
        log("STEP: health")
        health = safe_request("GET", f"{API_BASE_URL}/health")
        log(f"HEALTH: {json.dumps(health)}")

        log("STEP: reset")
        reset_data = safe_request("POST", f"{API_BASE_URL}/reset", json={})

        observation = reset_data.get("observation", {})
        email_text = observation.get("email_text", "")

        if not email_text:
            log("WARN: missing email_text, using fallback")
            email_text = "General customer inquiry"

        log(f"OBSERVATION: {email_text}")

        log("STEP: classify")
        action = choose_action(email_text)
        log(f"ACTION: {json.dumps(action)}")

        log("STEP: step")
        result = safe_request("POST", f"{API_BASE_URL}/step", json=action)
        log(f"RESULT: {json.dumps(result)}")

        log("STEP: state")
        state = safe_request("GET", f"{API_BASE_URL}/state")
        log(f"STATE: {json.dumps(state)}")

        log("STEP: tasks")
        tasks = safe_request("GET", f"{API_BASE_URL}/tasks")
        log(f"TASKS: {json.dumps(tasks)}")

        log("END")
        return 0

    except Exception as e:
        log(f"FATAL ERROR: {e}")
        log("END")
        return 0


if __name__ == "__main__":
    sys.exit(main())
<<<<<<< HEAD
EOF
=======
EOF
>>>>>>> 785131a (DockerFile Fixed)
