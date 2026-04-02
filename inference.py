from env.environment import EmailEnv
from env.models import EmailAction
from env.graders import grade_email

print("[START]")

env = EmailEnv()
obs = env.reset()

done = False

while not done:
    subject = obs.subject.lower()

    if "lottery" in subject:
        action = EmailAction(action_type="classify", content="spam")
    elif "report" in subject:
        action = EmailAction(action_type="mark_priority", content="high")
    elif "complaint" in subject:
        action = EmailAction(action_type="escalate")
    else:
        action = EmailAction(action_type="reply", content="ok")

    result = env.step(action)

    print("[STEP]")
    print(f"action: {action.action_type}")
    print(f"reward: {result.reward}")

    done = result.done
    if not done:
        obs = result.observation

print("[END]")
print("score: completed")