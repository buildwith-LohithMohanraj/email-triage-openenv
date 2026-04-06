from fastapi import FastAPI
from pydantic import BaseModel
import random
import uvicorn

app = FastAPI()

# ================= MODELS =================
class Action(BaseModel):
    action_type: str
    content: str

# ================= DATA =================
emails = [
    {
        "email_id": "1",
        "sender": "promo@spam.com",
        "subject": "You won a lottery!",
        "body": "Click to claim money",
        "type": "spam",
    },
    {
        "email_id": "2",
        "sender": "boss@company.com",
        "subject": "Meeting at 5 PM",
        "body": "Important discussion",
        "type": "important",
    },
    {
        "email_id": "3",
        "sender": "support@service.com",
        "subject": "Issue unresolved",
        "body": "Please escalate this issue",
        "type": "escalate",
    },
]

current_email = {}

# ================= ROUTES =================

@app.get("/")
def home():
    return {"message": "Email Triage OpenEnv Running"}


@app.post("/reset")
def reset():
    global current_email
    current_email = random.choice(emails)

    return {
        "email_id": current_email["email_id"],
        "sender": current_email["sender"],
        "subject": current_email["subject"],
        "body": current_email["body"],
        "labels": [],
        "priority": None,
    }


@app.post("/step")
def step(action: Action):
    global current_email

    reward = 0.0
    done = False

    if action.action_type == "classify":
        if action.content == current_email["type"]:
            reward = 0.7
            done = True
        else:
            reward = 0.1

    elif action.action_type == "mark_priority":
        if current_email["type"] == "important":
            reward = 0.6
            done = True
        else:
            reward = 0.2

    elif action.action_type == "escalate":
        if current_email["type"] == "escalate":
            reward = 0.9
            done = True
        else:
            reward = 0.3

    return {
        "reward": reward,
        "done": done,
        "info": {
            "actions": [action.content]
        }
    }

# ================= MAIN FUNCTION =================

def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


# REQUIRED ENTRY POINT
if __name__ == "__main__":
    main()