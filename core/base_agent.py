from abc import ABC, abstractmethod
from typing import Dict, List, Any
from .task import A2ATask

class A2AAgent(ABC):
    @abstractmethod
    async def execute_task(self, task: A2ATask) -> Dict[str, Any]:
        """Execute an A2A task"""
        pass


    @abstractmethod
    async def get_skill(self) -> List[str]:
        """Return the agent's skill"""
        pass