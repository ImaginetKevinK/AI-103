from .client import get_client, RESPONSES_DEPLOYMENT

DESCRIPTION = "Sends one prompt and prints the model's reply. The simplest possible call to the Responses interface."
PROMPT = "What is Microsoft Foundry?"


def run():
    client = get_client()
    response = client.responses.create(
        model=RESPONSES_DEPLOYMENT,
        input="What is Microsoft Foundry?",
    )
    print(response.output_text)
