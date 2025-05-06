# GeneAgent

GeneAgent is a specialized A2A (Agent-to-Agent) service that provides simulated genetic data for Gotchipus NFTs, enabling modular interaction with EIP-2535 (Diamond Standard) and ERC-6551 smart contracts in a Web3 environment.

## Functionality
- **Capability**: `get-genes`
- **Task**: Returns simulated gene data (e.g., color, glow, pattern) for a given `gotchi_id`.
- **Dependencies**: Relies on `A2AProtocol` for JSON-RPC communication.

## Usage
- **A2A Endpoint**: `POST /a2a/gene-agent`
- **Agent Card**: `GET /.well-known/gene-agent.json`
- **Example**:
  ```bash
  curl -X POST http://localhost:8000/a2a/gene-agent \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer gotchipus-token" \
  -d '{"jsonrpc": "2.0", "method": "get-genes", "params": {"gotchi_id": "GOTCHI123"}, "id": 1}'