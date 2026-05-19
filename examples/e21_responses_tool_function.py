import time

from .client import get_client, RESPONSES_DEPLOYMENT

DESCRIPTION = "Registers a local Python function as a tool. The model decides when to call it; the script runs the function locally and feeds the result back."
INSTRUCTIONS = "You are an AI assistant that provides information."
PROMPT = "(typed interactively)"
SETTINGS = {
    "tools": [{"type": "function", "name": "get_time", "description": "Get the current time"}],
}


def get_time():
    return f"The time is {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"


def run():
    client = get_client()

    function_tools = [
        {
            "type": "function",
            "name": "get_time",
            "description": "Get the current time",
        }
    ]

    messages = [
        {"role": "developer", "content": "You are an AI assistant that provides information."},
    ]

    print("Assistant: Enter a prompt (or type 'quit' to exit)")
    while True:
        prompt = input("\nYou: ")
        if prompt.lower() == "quit":
            print("Assistant: Goodbye!")
            break

        messages.append({"role": "user", "content": prompt})

        response = client.responses.create(
            model=RESPONSES_DEPLOYMENT,
            input=messages,
            tools=function_tools,
        )

        messages += response.output

        for item in response.output:
            if item.type == "function_call" and item.name == "get_time":
                current_time = get_time()
                messages.append({
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": current_time,
                })

                response = client.responses.create(
                    model=RESPONSES_DEPLOYMENT,
                    instructions="Answer only with the tool output.",
                    input=messages,
                    tools=function_tools,
                )

        print("\nAssistant:", response.output_text)
