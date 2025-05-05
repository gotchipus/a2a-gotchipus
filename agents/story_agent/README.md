# StoryAgent

The `StoryAgent` generates unique background stories and names for Gotchipus NFTs, powered by Grok.

## Functionality
- **Capability**: `generate-story`
- **Task**: Creates a story and name based on NFT gene data from GeneAgent.
- **Dependencies**: Requires `GeneAgent` for gene data, `A2AProtocol` for JSON-RPC, and Grok integration.

## Usage
- **A2A Endpoint**: `POST /a2a/story-agent`
- **Agent Card**: `GET /.well-known/story-agent.json`
- **Example**:
  ```bash
  curl -X POST http://localhost:8000/a2a/story-agent \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer gotchipus-token" \
  -d '{"jsonrpc": "2.0", "method": "generate-story", "params": {"gotchi_id": "GOTCHI #1"}, "id": 1}'