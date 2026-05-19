from .client import get_client, RESPONSES_DEPLOYMENT

DESCRIPTION = "Shows what the response object carries: the generated text, a unique identifier, the token count, and a completion status."
PROMPT = "Explain machine learning in simple terms."


def run():
    client = get_client()
    response = client.responses.create(
        model=RESPONSES_DEPLOYMENT,
        input="Explain machine learning in simple terms.",
    )
    print(response.output_text)
    print(f"Response ID: {response.id}")
    print(f"Tokens used: {response.usage.total_tokens}")
    print(f"Status: {response.status}")
