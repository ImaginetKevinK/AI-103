from .client import get_client, RESPONSES_DEPLOYMENT

DESCRIPTION = "Carries conversation context manually by appending each turn to a list and resending it. The alternative to chaining by identifier."
PROMPT = "Turn 1: What is machine learning?\nTurn 2: Can you give me an example?"


def run():
    client = get_client()

    conversation_history = [
        {
            "type": "message",
            "role": "user",
            "content": "What is machine learning?",
        }
    ]

    response1 = client.responses.create(
        model=RESPONSES_DEPLOYMENT,
        input=conversation_history,
    )
    print("Assistant:", response1.output_text)
    print()

    conversation_history += response1.output

    conversation_history.append({
        "type": "message",
        "role": "user",
        "content": "Can you give me an example?",
    })

    response2 = client.responses.create(
        model=RESPONSES_DEPLOYMENT,
        input=conversation_history,
    )
    print("Assistant:", response2.output_text)
