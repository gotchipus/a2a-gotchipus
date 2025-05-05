import logging
from typing import Dict, AsyncIterable, Any
from core.task import A2ATask
from .agent import StoryAgent


logger = logging.getLogger(__name__)


class StoryTaskManager:
    def __int__(self):
        self.task = Dict[str, A2ATask] = {}
        self.agent = StoryAgent()


    async def create_task(self, task: A2ATask) -> Dict[str, Any]:
        """Create and execute a story task."""
        logger.info(f"Creating task {task.task_id}")
        self.task[task.task_id] = task
        result = await self.agent.execute_task(task)
        task.status = "Completed"
        task.result = result
        return result
    
    async def stream_task(self, task: A2ATask) -> AsyncIterable[Dict[str, Any]]:
        """Stream task updates."""
        async for response in self.agent.stream(task):
            yield response

            