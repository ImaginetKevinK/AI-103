import os

from dotenv import load_dotenv
from openai import AzureOpenAI, AsyncAzureOpenAI

load_dotenv()

ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"]
API_KEY = os.environ["AZURE_OPENAI_API_KEY"]
API_VERSION = os.environ.get("AZURE_OPENAI_API_VERSION", "2025-04-01-preview")

DEFAULT_DEPLOYMENT = os.environ["AZURE_OPENAI_DEPLOYMENT"]
RESPONSES_DEPLOYMENT = os.environ.get("AZURE_OPENAI_RESPONSES_DEPLOYMENT", DEFAULT_DEPLOYMENT)
CHAT_DEPLOYMENT = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT", DEFAULT_DEPLOYMENT)
FOUNDRY_DEPLOYMENT = os.environ.get("AZURE_OPENAI_FOUNDRY_DEPLOYMENT", DEFAULT_DEPLOYMENT)

FOUNDRY_PROJECT_ENDPOINT = os.environ.get("AZURE_FOUNDRY_PROJECT_ENDPOINT", "")
FOUNDRY_AGENT_NAME = os.environ.get("AZURE_FOUNDRY_AGENT_NAME", "")
FOUNDRY_AGENT_VERSION = os.environ.get("AZURE_FOUNDRY_AGENT_VERSION", "1")


def get_client() -> AzureOpenAI:
    return AzureOpenAI(
        azure_endpoint=ENDPOINT,
        api_key=API_KEY,
        api_version=API_VERSION,
    )


def get_async_client() -> AsyncAzureOpenAI:
    return AsyncAzureOpenAI(
        azure_endpoint=ENDPOINT,
        api_key=API_KEY,
        api_version=API_VERSION,
    )
