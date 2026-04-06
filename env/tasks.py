# env/tasks.py

from typing import List, Dict


def get_tasks() -> List[Dict]:
    """
    Returns a list of tasks for evaluation.
    Each task must have:
    - id
    - description
    - expected_output
    """

    return [
        {
            "id": "task_1",
            "description": "Classify spam email",
            "input": {
                "sender": "promo@spam.com",
                "subject": "You won a lottery!",
                "body": "Click to claim money"
            },
            "expected_output": "spam"
        },
        {
            "id": "task_2",
            "description": "Mark important email",
            "input": {
                "sender": "boss@company.com",
                "subject": "Meeting at 5 PM",
                "body": "Important discussion"
            },
            "expected_output": "important"
        },
        {
            "id": "task_3",
            "description": "Escalate issue email",
            "input": {
                "sender": "support@service.com",
                "subject": "Issue unresolved",
                "body": "Please escalate this issue"
            },
            "expected_output": "escalate"
        }
    ]