from .client import get_client, CHAT_DEPLOYMENT

DESCRIPTION = "Carries chat-completions context by appending each turn to a messages list and resending the whole list every time."
INSTRUCTIONS = "You are a helpful AI assistant that answers questions and provides information."
PROMPT = "Turn 1: When was Microsoft founded?\nTurn 2: Who founded it?"


def run():
    client = get_client()

    conversation_messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant that answers questions and provides information.",
        },
        {"role": "user", "content": "When was Microsoft founded?"},
    ]

    completion = client.chat.completions.create(
        model=CHAT_DEPLOYMENT,
        messages=conversation_messages,
    )
    assistant_message = completion.choices[0].message.content
    print("Assistant:", assistant_message)

    conversation_messages.append({"role": "assistant", "content": assistant_message})
    conversation_messages.append({"role": "user", "content": "Who founded it?"})

    completion = client.chat.completions.create(
        model=CHAT_DEPLOYMENT,
        messages=conversation_messages,
    )
    assistant_message = completion.choices[0].message.content
    print("Assistant:", assistant_message)
