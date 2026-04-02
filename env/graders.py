def grade_email(email, actions):
    subject = email["subject"].lower()
    score = 0.0

    # Easy: spam
    if "lottery" in subject:
        if "spam" in actions and "archive" in actions:
            return 1.0
        elif "spam" in actions:
            return 0.5

    # Medium: work
    elif "report" in subject:
        if "high" in actions and "reply" in actions:
            return 1.0
        elif "high" in actions:
            return 0.5

    # Hard: complaint
    elif "complaint" in subject:
        if "escalate" in actions and "reply" in actions:
            return 1.0
        elif "escalate" in actions:
            return 0.5

    return round(score, 2)