from azure.identity import AzureCliCredential
from azure.ai.projects import AIProjectClient

from .client import (
    FOUNDRY_PROJECT_ENDPOINT,
    FOUNDRY_AGENT_NAME,
    FOUNDRY_AGENT_VERSION,
)

DESCRIPTION = "Calls a hosted agent defined in the Foundry portal. Signs in with Azure credentials instead of a key, and routes through the project client."
PROMPT = "Tell me what you can help with."
SETTINGS = {
    "agent_reference": f"{FOUNDRY_AGENT_NAME} v{FOUNDRY_AGENT_VERSION}",
}


def run():
    project_client = AIProjectClient(
        endpoint=FOUNDRY_PROJECT_ENDPOINT,
        credential=AzureCliCredential(),
    )
    openai_client = project_client.get_openai_client()

    response = openai_client.responses.create(
        input=[{"role": "user", "content": "Tell me what you can help with."}],
        extra_body={
            "agent_reference": {
                "name": FOUNDRY_AGENT_NAME,
                "version": FOUNDRY_AGENT_VERSION,
                "type": "agent_reference",
            }
        },
    )
    print(response.output_text)
