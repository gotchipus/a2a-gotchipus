import os
import logging
import json
from core.base_agent import A2AAgent
from core.task import A2ATask
from core.protocol import A2AProtocol
from typing import Dict, Any, List, Literal, AsyncIterable
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI


logger = logging.getLogger(__name__)

class StoryResponse(BaseModel):
    """Response model for StoryAgent"""
    task_id: str
    gotchi_id: str
    name: str
    story: str
    status: Literal["TERMINATE", ""]

    def format(self) -> str:
        """Format the response as a string"""
        return f"Name: {self.name}\nStory: {self.story}"
    

    def to_dict(self) -> Dict[str, Any]:
        """Convert string to dict"""
        data = {
            "task_id": self.task_id,
            "gotchi_id": self.gotchi_id,
            "name": self.name,
            "story": self.story,
            "status": self.status
        }

        return data
    

def get_api_key() -> str:
    """Helper method to handle API Key"""
    load_dotenv()
    return os.getenv("XAI_API_KEY")


class StoryAgent(A2AAgent):
    def __init__(self):
        try:
            self.agent = OpenAI(
                api_key=get_api_key(),
                base_url="https://api.x.ai/v1"
            )

            self.initialized = True
            logger.info("StoryAgent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize StoryAgent: {e}")
            self.initialized = False


    async def execute_task(self, task: A2ATask) -> Dict[str, Any]:
        if not self.initialized:
            return {
                "task_id": task.task_id,
                "error": "Agent initialization failed"
            }
        
        gotchi_id = task.params.get("gotchi_id")

        # get gene data
        gene_endpoint = "http://localhost:8000/a2a/gene-agent"
        gene_data = await A2AProtocol.send_request(
            gene_endpoint, "get-genes", {"gotchi_id": gotchi_id}
        )

        # generate gotchi story with Grok
        SYSTEM_PROMPT = """\
You are a creative assistant for generating unique background stories and names for Gotchipus NFTs. 
Each Gotchipus is a bioluminescent octopus-like creature with unique genes (color, glow, pattern). 
Generate a vivid story set in the Cosmic Reef, incorporating the NFT's gene data, and a fitting name. 
Respond using the StoryResponse format with fields: task_id, gotchi_id, name, story, status='TERMINATE'.
Example: "
{\"task_id\": \"TASK123\", \"gotchi_id\": \"GOTCHI123\", \"name\": \"StarWave\", 
\"story\": \"In the Cosmic Reef, GOTCHI123...\", \"status\": \"TERMINATE\"}"
"""
        completion = self.agent.chat.completions.create(
            model="grok-beta",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": gene_data}
            ],
        )

        res = completion.choices[0].message.content
        if res.startswith("```json") and res.endswith("```"):
            res = res[len("```json"):].strip()
            res = res.rstrip("```").strip()

        data = StoryResponse(**json.loads(res)).to_dict()
        
        return {
            "task_id": data["task_id"],
            "gotchi_id": data["gotchi_id"],
            "name": data["name"],
            "story": data["story"],
            "status": data["status"]
        }
    

    async def stream(self, task: A2ATask) -> AsyncIterable[Dict[str, Any]]:
        """Stream updates for a story generation task."""
        if not self.initialized:
            yield {
                "is_task_complete": False,
                "require_user_input": True,
                "content": "Agent initialization failed"
            }
            return 
        
        yield {
            "is_task_complete": False,
            "require_user_input": False,
            "content": "Processing story generation..."
        }

        try:
            result = await self.execute_task(task)
            model = StoryResponse(**result)
            yield {
                "is_task_complete": False,
                "require_user_input": False,
                "content": model.format()
            }

        except Exception as e:
            logger.error(f"Error in streaming: {e}")
            yield {
                "is_task_complete": False,
                "require_user_input": True,
                "content": f"Error generating story: {str(e)}"
            }
        
    
    def get_skill(self) -> List[str]:
        return ["generate-story"]