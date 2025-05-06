import logging
import json
import os
from core.base_agent import A2AAgent
from core.task import A2ATask
from typing import Dict, Any, List, Literal
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI


logger = logging.getLogger(__name__)

class GeneResponse(BaseModel):
    """Response model fro GeneAgent"""
    task_id: str
    gotchi_id: str
    personality_tags: str
    short_bio: str
    full_description: str
    status: Literal["TERMINATE", ""]

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "task_id": self.task_id,
            "gotchi_id": self.gotchi_id,
            "personality_tags": self.personality_tags,
            "short_bio": self.short_bio,
            "full_description": self.full_description,
            "status": self.status
        }
        return data
    

def get_api_key() -> str:
    """Helper method to handle API Key"""
    load_dotenv()
    return os.getenv("XAI_API_KEY")


class GeneAgent(A2AAgent):
    def __init__(self):
        try:
            self.agent = OpenAI(
                api_key=get_api_key(),
                base_url="https://api.x.ai/v1"
            )

            self.initialized = True
            logger.info("GeneAgent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize GeneAgent: {e}")
            self.initialized = False


    async def execute_task(self, task: A2ATask) -> Dict[str, Any]:
        if not self.initialized:
            return {
                "task_id": task.task_id,
                "error": "Agent initialization failed"
            }
        logger.info(f"Executing task {task.task_id} for gotchi {task.params.get('gotchi_id')}")
        gotchi_id = task.params.get("gotchi_id")

        # get gene from SQL
        gene_data = {}

        SYSTEM_PROMPT = """\
You are a personality designer for Gotchipus NFTs — luminous octopus-like creatures born in the Cosmic Reef.

Each Gotchipus has a unique DNA, including traits like color, glow, intelligence pattern, and emotion response. Based on this genetic profile, generate its **personality profile**, including:

1. **Personality Tags** — 3 to 5 keywords summarizing its temperament.
2. **Short Bio** — A single, vivid sentence summarizing this Gotchipus's personality essence.
3. **Full Description** — A detailed 100-150 word description about the Gotchipus's behavior, emotional patterns, how it interacts with the world, and what makes it psychologically unique.

Respond using the following JSON structure:
```json
{
  "task_id": "{{TASK_ID}}",
  "gotchi_id": "{{GOTCHI_ID}}",
  "personality_tags": ["Tag1", "Tag2", "Tag3"],
  "short_bio": "A short bio goes here.",
  "full_description": "A detailed personality description goes here.",
  "status": "TERMINATE"
}
Example: "
{
  \"task_id\": \"TASK456\",
  \"gotchi_id\": \"GOTCHI789\",
  \"name\": \"LunaWhirl\",
  \"personality_tags\": [\"Curious\", \"Empathic\", \"Expressive\", \"Dreamy\"],
  \"short_bio\": \"A whimsical thinker who dances through starlit tides, always chasing mysteries.\",
  \"full_description\": \"LunaWhirl is a Gotchipus who thrives in the quiet glow of the Cosmic Reef's silver tide. Endlessly curious and emotionally attuned, it forms deep bonds with other reef dwellers, often leading them on gentle journeys of discovery. Its thoughts spiral like the nebula patterns across its mantle, full of imaginative connections and poetic reflections. When near others, LunaWhirl pulses gently in response to their emotions, often comforting or inspiring them. It’s known as a dream-spinner, a quiet genius with a heart tuned to the rhythms of the stars.\",
  \"status\": \"TERMINATE\"
}
"
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

        data = GeneResponse(**json.loads(res)).to_dict()

        return {
            "task_id": data["task_id"],
            "gotchi_id": data["gotchi_id"],
            "personality_tags": data["personality_tags"],
            "short_bio": data["short_bio"],
            "full_description": data["full_description"],
            "status": data["status"]
        }
    

    def get_skill(self) -> List[str]:
        return ["get-genes"]