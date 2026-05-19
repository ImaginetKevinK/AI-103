from .client import get_client, RESPONSES_DEPLOYMENT

DESCRIPTION = "Equips the model with a web search tool. It looks up live information and cites the sources for questions about current events."
INSTRUCTIONS = "You are an AI assistant. Use web search when current information is required."
PROMPT = "What are three major announcements from Microsoft Build this week?"
SETTINGS = {
    "tools": [{"type": "web_search"}],
}


def run():
    client = get_client()
    response = client.responses.create(
        model=RESPONSES_DEPLOYMENT,
        instructions="You are an AI assistant. Use web search when current information is required.",
        input="What are three major announcements from Microsoft Build this week?",
        tools=[{"type": "web_search"}],
    )
    print(response.output_text)
