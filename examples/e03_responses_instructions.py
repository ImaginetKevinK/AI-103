from .client import get_client, RESPONSES_DEPLOYMENT

DESCRIPTION = "Adds an instructions field that steers the model's behavior separately from the user's prompt. Useful for setting tone, persona, or rules."
INSTRUCTIONS = "You are a helpful AI assistant that answers questions clearly and concisely."
PROMPT = "Explain neural networks."


def run():
    client = get_client()
    response = client.responses.create(
        model=RESPONSES_DEPLOYMENT,
        instructions="You are a helpful AI assistant that answers questions clearly and concisely.",
        input="Explain neural networks.",
    )
    print(response.output_text)
