import asyncio
from core.task import A2ATask
from .task_manager import StoryTaskManager

async def main():
    manager = StoryTaskManager()

    task = A2ATask(
        task_id="gotchi-task-123",
        agent_id="story-agent",
        params={"gotchi_id": "GOTCHI #1"}
    )

    async for response in manager.stream_task(task):
        print(response)


if __name__ == "__main__":
    asyncio.run(main())