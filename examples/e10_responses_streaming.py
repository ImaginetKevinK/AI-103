from .client import get_client, RESPONSES_DEPLOYMENT

DESCRIPTION = "Receives the reply as a stream of events instead of one finished blob. Prints the raw event objects so every event type is visible."
PROMPT = "Write a short story about a robot learning to paint."
SETTINGS = {"stream": True}


def run():
    client = get_client()
    stream = client.responses.create(
        model=RESPONSES_DEPLOYMENT,
        input="Write a short story about a robot learning to paint.",
        stream=True,
    )
    for event in stream:
        print(event, end="", flush=True)
    print()
