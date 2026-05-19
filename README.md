# AI-103

Microsoft Azure AI / OpenAI tutorial sandbox. Each Microsoft tutorial snippet
lives as its own example module under `examples/`, picked from a menu in
`main.py`.

For VS Code-specific instructions (interpreter selection, run button, debug
configuration with arguments) see [`SETUP.md`](./SETUP.md).

## Setup

```pwsh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your values:

```pwsh
copy .env.example .env
```

Required keys:

- `AZURE_OPENAI_ENDPOINT` – resource endpoint (no trailing path)
- `AZURE_OPENAI_API_KEY` – key from Azure Portal -> Keys and Endpoint
- `AZURE_OPENAI_DEPLOYMENT` – default model deployment name

Optional keys:

- `AZURE_OPENAI_API_VERSION` (defaults to `2025-04-01-preview` for Responses API support)
- `AZURE_OPENAI_RESPONSES_DEPLOYMENT` – override for examples 1-13
- `AZURE_OPENAI_CHAT_DEPLOYMENT` – override for examples 14-16
- `AZURE_OPENAI_FOUNDRY_DEPLOYMENT` – override for example 5 (Foundry direct model)
- `AZURE_OPENAI_RESPONSE_ID` – preset response id for example 9

Foundry Agent keys (example 17 only):

- `AZURE_FOUNDRY_PROJECT_ENDPOINT` – the `https://<resource>.services.ai.azure.com/api/projects/<project>` URL
- `AZURE_FOUNDRY_AGENT_NAME` – the agent name from the Foundry portal
- `AZURE_FOUNDRY_AGENT_VERSION` – defaults to `1`

Example 17 uses `DefaultAzureCredential` (Azure AD), not the API key. Before running it:

```pwsh
az login
```

## Run

Interactive menu:

```pwsh
python main.py
```

Or jump straight to an example by number or module name:

```pwsh
python main.py 1
python main.py e07_responses_chat_loop
python main.py responses_streaming_filtered
```

## Examples

### Responses API

1. Basic request
2. Inspect `response.id` / tokens / status
3. With instructions (system prompt)
4. With params (`temperature`, `max_output_tokens`)
5. Foundry direct model (e.g. `microsoft-phi-4`)
6. Multi-turn via `previous_response_id`
7. Interactive chat loop using `previous_response_id`
8. Multi-turn via conversation history input
9. Retrieve a previous response by ID
10. Streaming (raw events)
11. Streaming filtered to text deltas
12. Async client
13. Async streaming

### Chat Completions API

14. Basic request
15. Manual conversation history
16. Interactive chat loop

### Foundry Agent (project SDK + Azure AD)

17. Call agent via `AIProjectClient` + `DefaultAzureCredential`

### Tools (Responses API)

18. `code_interpreter` tool (auto-managed container)
19. `web_search` tool
20. `file_search` tool (creates a vector store from `data/expenses_policy.txt`)
21. `function` tool (interactive loop calling a local `get_time()`)
22. `file_search` + `web_search` combined (travel assistant; reads `data/brochures/*.txt`)

## Test

Unit tests (no network calls, fast):

```pwsh
pytest
```

Includes the integration test that calls the live Foundry agent (requires `az login`):

```pwsh
pytest --integration
```

Run only a single test file or pattern:

```pwsh
pytest tests/test_launcher.py
pytest -k resolve
```

The suite covers:

- **`tests/test_launcher.py`** — menu rendering, number/name resolution, and edge cases (invalid numbers, negative, zero, empty, unknown names, case sensitivity)
- **`tests/test_examples.py`** — every example module imports and exposes a callable `run()`, menu registry matches the module list, `client.py` exposes the expected constants, factory functions return the right types, and the interactive chat loops (`e07`, `e16`) exit cleanly on `quit`
- **`tests/test_integration.py`** — live call to example 17 (gated behind `--integration`)
