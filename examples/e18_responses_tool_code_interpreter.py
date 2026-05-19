from .client import get_client, RESPONSES_DEPLOYMENT

DESCRIPTION = "Equips the model with a sandboxed Python tool. It writes and runs code on the server to answer math questions, then returns the result."
INSTRUCTIONS = "You are an AI assistant that provides information. Use the python tool to run code for math problems."
PROMPT = "What is the square root of 16?"
SETTINGS = {
    "tools": [{"type": "code_interpreter", "container": {"type": "auto"}}],
}


def run():
    client = get_client()
    response = client.responses.create(
        model=RESPONSES_DEPLOYMENT,
        instructions="You are an AI assistant that provides information. Use the python tool to run code for math problems.",
        input="What is the square root of 16?",
        tools=[{"type": "code_interpreter", "container": {"type": "auto"}}],
    )
    print(response.output_text)
