# env/graders.py

from typing import Dict


def grade_task(task: Dict, action: str) -> float:
    """
    Returns a score between 0.0 and 1.0
    """

    expected = task.get("expected_output", "").strip().lower()
    action = (action or "").strip().lower()

    if action == expected:
        return 1.0

    # Partial scoring logic (safe fallback)
    if expected in action:
        return 0.5

    return 0.0