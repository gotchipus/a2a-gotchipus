import logging
import json 
from sanic.response import json as sanic_json
from sanic import Blueprint
from core.protocol import require_auth
from core.task import A2ATask
from agents.gene_agent.task_manager import GeneTaskManager


logger = logging.getLogger(__name__)

gene = Blueprint("gene", url_prefix="gene-agent")
gene_task_manager = GeneTaskManager()


@gene.route("/api/gene-agent/generate-personality", methods=["POST"])
@require_auth
async def generate_personality(request):
    data = request.json
    task = A2ATask(
        task_id=data["task_id"],
        agent_id="gene-agent",
        params={"gotchi_id": "GOTCHI #1"}
    )

    result = await gene_task_manager.create_task(task)
    return sanic_json(result)


@gene.route("/a2a/gene-agent/generate-personality", methods=["POST"])
@require_auth
async def gene_agent_endpoint(request):
    data = request.json
    if data.get("jsonrpc") != "2.0":
        return sanic_json({"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": None})

    result = await gene_task_manager.create_task(
        A2ATask(task_id=str(data["id"]), agent_id="gene-agent", params=data["params"])
    )
    return sanic_json({"jsonrpc": "2.0", "result": result, "id": data["id"]})


@gene.route("/.well-known/gene-agent.json", methods=["GET"])
async def get_agent_card(request):
    try:
        with open("./.well-known/gene-agent.json", "r") as f:
            return sanic_json(json.loads(f.read()))

    except FileNotFoundError:
        return sanic_json({"error": "Agent Card not found"}, status=404)