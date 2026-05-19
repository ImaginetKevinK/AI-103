from .client import get_client, RESPONSES_DEPLOYMENT

DESCRIPTION = "Same streaming call, but filters the stream down to just the text fragments. Produces a typewriter-style display as the model speaks."
PROMPT = "Write a short story about a robot learning to paint."
SETTINGS = {"stream": True}


def run():
    client = get_client()
    response_id = None
    stream = client.responses.create(
        model=RESPONSES_DEPLOYMENT,
        input="Write a short story about a robot learning to paint.",
        stream=True,
    )
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)
        elif event.type == "response.completed":
            response_id = event.response.id
    print()
    if response_id:
        print(f"\nResponse ID: {response_id}")
