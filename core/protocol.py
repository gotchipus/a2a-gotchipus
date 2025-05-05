import aiohttp
from typing import Dict, Any
from functools import wraps
from sanic import response

class A2AProtocol:
    @staticmethod
    async def send_request(endpoint: str, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send a JSON-RPC request to a remote agent."""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer gotchipus-token"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, json=payload, headers=headers) as res:
                if res.status != 200:
                    raise Exception(f"Request failed: {res.status} {await res.text()}")
                
                data = await res.json()

                if "error" in data:
                    raise Exception(data["error"]["message"])
                return data["result"]
            

def require_auth(func):
    """Simple API Key authorization decorator"""
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        if request.headers.get("Authorization") != "Bearer gotchipus-token":
            return response.json({"error": "Unauthorized"}, status=401)
        return await func(request, *args, **kwargs)
    return wrapper