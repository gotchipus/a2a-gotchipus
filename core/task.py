from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class A2ATask:
    task_id: str
    agent_id: str
    params: Dict[str, Any]
    status: str = "pending"
    result: Dict[str, Any] = None