import logging
import json 
from sanic.response import json as sanic_json
from sanic import Blueprint
from core.protocol import A2AProtocol, require_auth
from core.task import A2ATask
from agents.story_agent.task_manager import StoryTaskManager


logger = logging.getLogger(__name__)

story = Blueprint("story", url_prefix="story-agent")
story_task_manager = StoryTaskManager()


@story.route("/api/story-agent/generate", methods=["POST"])
@require_auth
async def generate_story(request):
    data = request.json
    task = A2ATask(
        task_id=data["task_id"],
        agent_id="story-agent",
        params={"gotchi_id": data["gotchi_id"]}
    )
    result = await story_task_manager.create_task(task)
    return sanic_json(result)


@story.route("/a2a/story-agent/generate", methods=["POST"])
@require_auth
async def story_agent_endpoint(request):
    data = request.json
    if data.get("jsonrpc") != "2.0":
        return sanic_json({"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": None})

    result = await story_task_manager.create_task(
        A2ATask(task_id=str(data["id"]), agent_id="story-agent", params=data["params"])
    )
    return sanic_json({"jsonrpc": "2.0", "result": result, "id": data["id"]})


@story.route("/.well-known/story-agent.json", methods=["GET"])
async def get_agent_card(request):
    try:
        with open("./.well-known/story-agent.json", "r") as f:
            return sanic_json(json.loads(f.read()))

    except FileNotFoundError:
        return sanic_json({"error": "Agent Card not found"}, status=404)