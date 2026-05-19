from .client import get_client, RESPONSES_DEPLOYMENT

DESCRIPTION = "Adds two generation knobs: temperature for randomness and a cap on reply length. Useful for tuning creativity and cost."
INSTRUCTIONS = "You are a helpful AI assistant that answers questions clearly and concisely."
PROMPT = "Write a creative story about AI."
SETTINGS = {
    "temperature": 0.8,
    "max_output_tokens": 200,
}


def run():
    client = get_client()
    response = client.responses.create(
        model=RESPONSES_DEPLOYMENT,
        instructions="You are a helpful AI assistant that answers questions clearly and concisely.",
        input="Write a creative story about AI.",
        temperature=0.8,
        max_output_tokens=200,
    )
    print(response.output_text)
