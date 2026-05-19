from .client import get_client, CHAT_DEPLOYMENT

DESCRIPTION = "Interactive chat-completions loop. Each turn appends to a messages list that is resent on every request. Type quit to leave."
INSTRUCTIONS = "You are a helpful AI assistant that answers questions and provides information."
PROMPT = "(typed interactively)"


def run():
    client = get_client()

    conversation_messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant that answers questions and provides information.",
        }
    ]

    print("Assistant: Enter a prompt (or type 'quit' to exit)")
    while True:
        input_text = input("\nYou: ")
        if input_text.lower() == "quit":
            print("Assistant: Goodbye!")
            break

        conversation_messages.append({"role": "user", "content": input_text})

        completion = client.chat.completions.create(
            model=CHAT_DEPLOYMENT,
            messages=conversation_messages,
        )
        assistant_message = completion.choices[0].message.content
        print("\nAssistant:", assistant_message)

        conversation_messages.append({"role": "assistant", "content": assistant_message})
