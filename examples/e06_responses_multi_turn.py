from .client import get_client, RESPONSES_DEPLOYMENT

DESCRIPTION = "Sends a follow-up that points at the first response by its identifier. The service threads context for you, so you do not resend history."
INSTRUCTIONS = "You are a helpful AI assistant that explains technology concepts clearly."
PROMPT = "Turn 1: What is machine learning?\nTurn 2: Can you give me an example?"
SETTINGS = {
    "previous_response_id": "<chained on follow-up call>",
}


def run():
    client = get_client()

    response1 = client.responses.create(
        model=RESPONSES_DEPLOYMENT,
        instructions="You are a helpful AI assistant that explains technology concepts clearly.",
        input="What is machine learning?",
    )
    print("Assistant:", response1.output_text)
    print()

    response2 = client.responses.create(
        model=RESPONSES_DEPLOYMENT,
        instructions="You are a helpful AI assistant that explains technology concepts clearly.",
        input="Can you give me an example?",
        previous_response_id=response1.id,
    )
    print("Assistant:", response2.output_text)
