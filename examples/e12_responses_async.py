import asyncio

from .client import get_async_client, RESPONSES_DEPLOYMENT

DESCRIPTION = "Uses the asynchronous client so the call yields control back to the event loop while waiting on the network."
PROMPT = "Explain quantum computing briefly."


async def _run():
    client = get_async_client()
    try:
        response = await client.responses.create(
            model=RESPONSES_DEPLOYMENT,
            input="Explain quantum computing briefly.",
        )
        print(response.output_text)
    finally:
        await client.close()


def run():
    asyncio.run(_run())
