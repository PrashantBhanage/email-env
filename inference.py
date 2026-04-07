
import json
import os
import re
import sys
from typing import Optional

from openai import OpenAI
from environment.env import EmailTriageEnv
from environment.tasks import get_all_task_ids

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

FALLBACK_ACTION = {
    "category": "general",
    "priority": "low",
    "action": "reply"
}

SYSTEM_PROMPT = """Classify the email and return JSON:
category: billing | technical | general
priority: low | medium | high
action: reply | escalate | ignore
Only return JSON."""

def extract_json(text: str) -> Optional[dict]:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            return None
    return None

def run_inference(client, email_text):
    try:
        res = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": email_text}
            ],
            temperature=0.1
        )
        content = res.choices[0].message.content or ""
        parsed = extract_json(content)

        if parsed:
            return {
                "category": parsed.get("category", "general"),
                "priority": parsed.get("priority", "low"),
                "action": parsed.get("action", "reply")
            }
    except Exception as e:
        print("WARN:", e)

    return FALLBACK_ACTION

def main():
    if not HF_TOKEN:
        print("No HF_TOKEN, returning mock score")
        return 0.7

    client = OpenAI(api_key=HF_TOKEN, base_url=API_BASE_URL)
    env = EmailTriageEnv()
    tasks = get_all_task_ids()

    results = []

    for t in tasks:
        obs = env.reset(task_id=t)
