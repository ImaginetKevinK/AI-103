from .client import get_client, RESPONSES_DEPLOYMENT

DESCRIPTION = "Wraps previous-response chaining in a loop so you can hold a free-form conversation. Type quit to leave."
INSTRUCTIONS = "You are a helpful AI assistant that explains technology concepts clearly."
PROMPT = "(typed interactively)"
SETTINGS = {
    "previous_response_id": "<chained from prior turn>",
}


def run():
    client = get_client()
    last_response_id = None

    print("Assistant: Enter a prompt (or type 'quit' to exit)")
    while True:
        input_text = input("\nYou: ")
        if input_text.lower() == "quit":
            print("Assistant: Goodbye!")
            break

        response = client.responses.create(
            model=RESPONSES_DEPLOYMENT,
            instructions="You are a helpful AI assistant that explains technology concepts clearly.",
            input=input_text,
            previous_response_id=last_response_id,
        )
        print("\nAssistant:", response.output_text)
        last_response_id = response.id
