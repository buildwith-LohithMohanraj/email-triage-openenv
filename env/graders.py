# env/graders.py

from typing import Dict


def grade_task(task: Dict, action: str) -> float:
    """
    Returns a score strictly between 0 and 1
    """

    expected = task.get("expected_output", "").strip().lower()
    action = (action or "").strip().lower()

    if action == expected:
        return 0.9   # ✅ NOT 1.0

    # partial match
    if expected in action:
        return 0.5   # ✅ valid

    return 0.1       # ✅ NOT 0.0