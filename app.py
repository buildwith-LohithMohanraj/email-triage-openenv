from fastapi import FastAPI
from env.environment import EmailEnv
from env.models import EmailAction

app = FastAPI()
env = EmailEnv()

@app.get("/")
def home():
    return {"message": "Email Triage OpenEnv Running"}

@app.get("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: EmailAction):
    result = env.step(action)
    return {
        "reward": result.reward,
        "done": result.done,
        "info": result.info
    }