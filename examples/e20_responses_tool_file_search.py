import os

from .client import get_client, RESPONSES_DEPLOYMENT

DESCRIPTION = "Uploads a document to a vector store and lets the model search the store to answer a question grounded in the file's contents."
INSTRUCTIONS = "You are an AI assistant that provides information from HR policy documents."
PROMPT = "What's the maximum amount I can claim for a taxi ride?"
SETTINGS = {
    "tools": [{"type": "file_search", "vector_store_ids": ["<created at runtime>"]}],
    "include": ["file_search_call.results"],
}

POLICY_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "expenses_policy.txt")


def run():
    client = get_client()

    vector_store = client.vector_stores.create(name="policy-docs")
    try:
        with open(POLICY_FILE, "rb") as f:
            client.vector_stores.files.upload_and_poll(
                vector_store_id=vector_store.id,
                file=f,
            )

        response = client.responses.create(
            model=RESPONSES_DEPLOYMENT,
            instructions="You are an AI assistant that provides information from HR policy documents.",
            input="What's the maximum amount I can claim for a taxi ride?",
            tools=[{
                "type": "file_search",
                "vector_store_ids": [vector_store.id],
            }],
            include=["file_search_call.results"],
        )
        print(response.output_text)
    finally:
        client.vector_stores.delete(vector_store.id)
