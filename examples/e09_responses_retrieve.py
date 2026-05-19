import os

from .client import get_client, RESPONSES_DEPLOYMENT

DESCRIPTION = "Fetches an existing response by its identifier. Lets you re-read past output without regenerating it."
PROMPT = "Say one short sentence so we have a response to retrieve."


def run():
    client = get_client()

    response_id = os.environ.get("AZURE_OPENAI_RESPONSE_ID")
    if not response_id:
        seed = client.responses.create(
            model=RESPONSES_DEPLOYMENT,
            input="Say one short sentence so we have a response to retrieve.",
        )
        response_id = seed.id
        print(f"(seeded response {response_id})")
        print()

    previous_response = client.responses.retrieve(response_id)
    print(f"Previous response: {previous_response.output_text}")
