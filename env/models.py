from pydantic import BaseModel
from typing import List, Optional

class EmailObservation(BaseModel):
    email_id: str
    sender: str
    subject: str
    body: str
    labels: List[str]
    priority: Optional[str]

class EmailAction(BaseModel):
    action_type: str
    content: Optional[str] = None

class StepResult(BaseModel):
    observation: EmailObservation
    reward: float
    done: bool
    info: dict