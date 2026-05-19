from .client import get_client, CHAT_DEPLOYMENT

DESCRIPTION = "Calls the older chat-completions interface with a list of system and user messages. Shows the alternative to the newer Responses interface."
INSTRUCTIONS = "You are a helpful assistant."
PROMPT = "When was Microsoft founded?"


def run():
    client = get_client()
    completion = client.chat.completions.create(
        model=CHAT_DEPLOYMENT,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "When was Microsoft founded?"},
        ],
    )
    print(completion.choices[0].message.content)
