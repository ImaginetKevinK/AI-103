import glob
import os

from .client import get_client, RESPONSES_DEPLOYMENT

DESCRIPTION = "Combines file search over uploaded brochures with web search for everything else. The model picks the right tool per question and threads context across turns."
INSTRUCTIONS = (
    "You are a travel assistant that provides information on travel services "
    "available from Margie's Travel. Answer questions about services offered by "
    "Margie's Travel using the provided travel brochures. Search the web for "
    "general information about destinations or current travel advice."
)
PROMPT = "(typed interactively)"
SETTINGS = {
    "tools": [
        {"type": "file_search", "vector_store_ids": ["<created at runtime>"]},
        {"type": "web_search"},
    ],
    "previous_response_id": "<chained from prior turn>",
}

BROCHURE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "brochures")


def run():
    client = get_client()

    print("Creating vector store and uploading brochures...")
    vector_store = client.vector_stores.create(name="travel-brochures")

    file_paths = sorted(glob.glob(os.path.join(BROCHURE_DIR, "*.pdf"))) + sorted(
        glob.glob(os.path.join(BROCHURE_DIR, "*.txt"))
    )
    if not file_paths:
        print(f"No brochures found in {BROCHURE_DIR}")
        client.vector_stores.delete(vector_store.id)
        return

    file_streams = [open(p, "rb") for p in file_paths]
    try:
        file_batch = client.vector_stores.file_batches.upload_and_poll(
            vector_store_id=vector_store.id,
            files=file_streams,
        )
        print(f"Vector store created with {file_batch.file_counts.completed} files.")
    finally:
        for f in file_streams:
            f.close()

    try:
        last_response_id = None
        print("\nAssistant: Enter a prompt (or type 'quit' to exit)")
        while True:
            input_text = input("\nYou: ")
            if input_text.lower() == "quit":
                print("Assistant: Goodbye!")
                break

            response = client.responses.create(
                model=RESPONSES_DEPLOYMENT,
                instructions=(
                    "You are a travel assistant that provides information on travel services "
                    "available from Margie's Travel. Answer questions about services offered by "
                    "Margie's Travel using the provided travel brochures. Search the web for "
                    "general information about destinations or current travel advice."
                ),
                input=input_text,
                previous_response_id=last_response_id,
                tools=[
                    {"type": "file_search", "vector_store_ids": [vector_store.id]},
                    {"type": "web_search"},
                ],
            )
            print("\nAssistant:", response.output_text)
            last_response_id = response.id
    finally:
        client.vector_stores.delete(vector_store.id)
