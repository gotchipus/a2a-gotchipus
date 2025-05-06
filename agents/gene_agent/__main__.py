import asyncio
from core.task import A2ATask
from .task_manager import GeneTaskManager

async def main():
    manager = GeneTaskManager()

    task = A2ATask(
        task_id="gotchi-task-123",
        agent_id="gene-agent",
        params={"gotchi_id": "GOTCHI #1"}
    )

    response = manager.create_task(task)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())