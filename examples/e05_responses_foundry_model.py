from .client import get_client, FOUNDRY_DEPLOYMENT

DESCRIPTION = "Targets a small open-weight model deployed through Foundry instead of a flagship model. Same call shape, different deployment name."
INSTRUCTIONS = "You are a helpful AI assistant that answers questions clearly and concisely."
PROMPT = "What are the benefits of small language models?"


def run():
    client = get_client()
    response = client.responses.create(
        model=FOUNDRY_DEPLOYMENT,
        instructions="You are a helpful AI assistant that answers questions clearly and concisely.",
        input="What are the benefits of small language models?",
    )
    print(response.output_text)
