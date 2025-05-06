import logging
from core.task import A2ATask
from typing import Dict, Any
from .agent import GeneAgent


logger = logging.getLogger(__name__)


class GeneTaskManager:
    def __init__(self):
        self.task = Dict[str, A2ATask] = {}
        self.agent = GeneAgent()

    
    async def create_task(self, task: A2ATask) -> Dict[str, Any]:
        """Create and execute a story task."""
        logger.info(f"Creating task {task.task_id}")
        self.task[task.task_id] = task
        result = await self.agent.execute_task(task)
        task.status = "Completed"
        task.result = result
        return result
