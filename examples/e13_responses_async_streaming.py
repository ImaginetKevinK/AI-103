import asyncio

from .client import get_async_client, RESPONSES_DEPLOYMENT

DESCRIPTION = "Combines asynchronous with streaming: an async loop walks the event stream and prints each text fragment as it arrives."
PROMPT = "Write a haiku about coding."
SETTINGS = {"stream": True}


async def _run():
    client = get_async_client()
    try:
        stream = await client.responses.create(
            model=RESPONSES_DEPLOYMENT,
            input="Write a haiku about coding.",
            stream=True,
        )
        async for event in stream:
            if event.type == "response.output_text.delta":
                print(event.delta, end="", flush=True)
        print()
    finally:
        await client.close()


def run():
    asyncio.run(_run())
