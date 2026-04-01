from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Email Triage Environment Server", version="1.0.0")


@app.get("/")
def root():
    return {
        "status": "ok",
        "name": "Email Triage Environment",
        "mode": "server"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "name": "Email Triage Environment",
        "version": "1.0.0"
    }


@app.post("/reset")
def reset():
    return {
        "observation": {
            "email_text": "Subject: Urgent billing issue\n\nHi, I was charged twice this month and need this resolved immediately."
        },
        "info": {},
        "done": False
    }


@app.post("/step")
def step(action: dict):
    category = action.get("category", "general")
    priority = action.get("priority", "low")
    decision = action.get("action", "reply")

    reward = 0.8
    if category == "billing" and priority == "high" and decision == "escalate":
        reward = 1.0

    return {
        "reward": reward,
        "done": True,
        "info": {
            "category": category,
            "priority": priority,
            "action": decision
        }
    }


@app.get("/state")
def state():
    return {
        "status": "ready"
    }


@app.get("/tasks")
def tasks():
    return {
        "tasks": ["billing_email", "technical_issue", "general_query"]
    }


def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
