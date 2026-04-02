from env.models import EmailObservation, EmailAction, StepResult
from env.tasks import INBOX
from env.graders import grade_email


class EmailEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.inbox = INBOX.copy()
        self.current_index = 0
        self.actions_taken = []
        self.done = False
        return self._get_observation()

    def _get_observation(self):
        email = self.inbox[self.current_index]
        self.current_email = email

        return EmailObservation(
            email_id=email["email_id"],
            sender=email["sender"],
            subject=email["subject"],
            body=email["body"],
            labels=[],
            priority=None
        )

    def step(self, action: EmailAction):
        reward = 0.0

        # ✅ Track actions properly
        if action.action_type == "classify":
            self.actions_taken.append(action.content)
            reward += 0.2

        elif action.action_type == "archive":
            self.actions_taken.append("archive")
            reward += 0.2

        elif action.action_type == "reply":
            self.actions_taken.append("reply")
            reward += 0.3

        elif action.action_type == "mark_priority":
            self.actions_taken.append(action.content)
            reward += 0.2

        elif action.action_type == "escalate":
            self.actions_taken.append("escalate")
            reward += 0.3

        # ❌ Penalty for repeating same action
        if self.actions_taken.count(action.action_type) > 1:
            reward -= 0.2

        # ⚠️ Urgency penalty (hard task)
        if "complaint" in self.current_email["subject"].lower():
            if action.action_type not in ["escalate", "reply"]:
                reward -= 0.3

        done = False
        final_actions = None  # ✅ store actions before reset

        # ✅ Move to next email after 2 actions
        if len(self.actions_taken) >= 2:
            final_actions = self.actions_taken.copy()

            # 🎯 Apply grading
            score = grade_email(self.current_email, final_actions)
            reward += score

            self.current_index += 1
            self.actions_taken = []

            # ✅ Check if all emails done
            if self.current_index >= len(self.inbox):
                done = True
            else:
                self._get_observation()

        # ✅ Safe observation handling
        observation = None if done else self._get_observation()

        return StepResult(
            observation=observation,
            reward=round(reward, 2),
            done=done,
            info={
                "actions": final_actions if final_actions else self.actions_taken
            }
        )

    def state(self):
        return {
            "current_index": self.current_index,
            "actions": self.actions_taken
        }