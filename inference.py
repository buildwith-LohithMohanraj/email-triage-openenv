import os
import asyncio
from typing import List
from openai import OpenAI
import requests

# ================= ENV VARIABLES (STRICT) =================
API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]
MODEL_NAME = os.environ["MODEL_NAME"]

ENV_URL = os.environ.get("ENV_URL", "http://localhost:7860")

MAX_STEPS = 5

# ================= OPENAI CLIENT =================
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

# ================= LOGGING =================
def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error):
    error_val = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error_val}",
        flush=True,
    )

def log_end(success: bool, steps: int, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}",
        flush=True,
    )

# ================= MODEL CALL =================
def get_action_from_model(email_text: str) -> str:
    """
    MUST call LLM via proxy (VERY IMPORTANT)
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "Classify the email into one word: spam, important, or escalate."},
            {"role": "user", "content": email_text},
        ],
        max_tokens=10,
        temperature=0.3,
    )

    output = response.choices[0].message.content.strip().lower()

    # Ensure valid output
    if "spam" in output:
        return "spam"
    elif "important" in output:
        return "important"
    elif "escalate" in output:
        return "escalate"

    return "spam"  # fallback but still after API call

# ================= MAIN LOOP =================
async def main():
    rewards = []
    steps_taken = 0
    success = False

    log_start(task="email_triage", env="openenv", model=MODEL_NAME)

    try:
        # RESET
        res = requests.post(f"{ENV_URL}/reset")
        data = res.json()

        for step in range(1, MAX_STEPS + 1):
            email_text = f"{data['subject']} {data['body']}"

            action_content = get_action_from_model(email_text)

            payload = {
                "action_type": "classify",
                "content": action_content
            }

            res = requests.post(f"{ENV_URL}/step", json=payload)
            result = res.json()

            reward = float(result.get("reward", 0.1))
            done = result.get("done", False)

            rewards.append(reward)
            steps_taken = step

            log_step(step, action_content, reward, done, None)

            if done:
                break

        success = True

    except Exception as e:
        log_step(steps_taken, "error", 0.10, True, str(e))

    finally:
        log_end(success, steps_taken, rewards)


# ================= ENTRY =================
if __name__ == "__main__":
    asyncio.run(main())