import importlib

import pytest

import main

EXAMPLE_MODULES = [
    "e01_responses_basic",
    "e02_responses_metadata",
    "e03_responses_instructions",
    "e04_responses_params",
    "e05_responses_foundry_model",
    "e06_responses_multi_turn",
    "e07_responses_chat_loop",
    "e08_responses_history_input",
    "e09_responses_retrieve",
    "e10_responses_streaming",
    "e11_responses_streaming_filtered",
    "e12_responses_async",
    "e13_responses_async_streaming",
    "e14_chat_completions_basic",
    "e15_chat_completions_multi_turn",
    "e16_chat_completions_chat_loop",
    "e17_foundry_agent_basic",
    "e18_responses_tool_code_interpreter",
    "e19_responses_tool_web_search",
    "e20_responses_tool_file_search",
    "e21_responses_tool_function",
    "e22_responses_tools_combined",
]


@pytest.mark.parametrize("module_name", EXAMPLE_MODULES)
def test_example_imports_and_has_run(module_name):
    module = importlib.import_module(f"examples.{module_name}")
    run = getattr(module, "run", None)
    assert callable(run), f"{module_name} missing callable run()"


@pytest.mark.parametrize("module_name", EXAMPLE_MODULES)
def test_example_has_description(module_name):
    module = importlib.import_module(f"examples.{module_name}")
    description = getattr(module, "DESCRIPTION", None)
    assert isinstance(description, str) and description.strip(), (
        f"{module_name} missing non-empty DESCRIPTION constant"
    )


@pytest.mark.parametrize("module_name", EXAMPLE_MODULES)
def test_example_has_prompt(module_name):
    module = importlib.import_module(f"examples.{module_name}")
    prompt = getattr(module, "PROMPT", None)
    assert isinstance(prompt, str) and prompt.strip(), (
        f"{module_name} missing non-empty PROMPT constant"
    )


@pytest.mark.parametrize("module_name", EXAMPLE_MODULES)
def test_example_instructions_is_valid_if_present(module_name):
    module = importlib.import_module(f"examples.{module_name}")
    instructions = getattr(module, "INSTRUCTIONS", None)
    if instructions is not None:
        assert isinstance(instructions, str) and instructions.strip(), (
            f"{module_name} INSTRUCTIONS must be a non-empty string when defined"
        )


@pytest.mark.parametrize("module_name", EXAMPLE_MODULES)
def test_example_settings_is_valid_if_present(module_name):
    module = importlib.import_module(f"examples.{module_name}")
    settings = getattr(module, "SETTINGS", None)
    if settings is not None:
        assert isinstance(settings, dict) and settings, (
            f"{module_name} SETTINGS must be a non-empty dict when defined"
        )
        for key in settings:
            assert isinstance(key, str) and key.strip(), (
                f"{module_name} SETTINGS keys must be non-empty strings"
            )


def test_menu_modules_match_example_modules_list():
    flat_names = [name for name, _ in main._flat()]
    assert flat_names == EXAMPLE_MODULES


def test_client_module_exposes_expected_constants():
    from examples import client

    for attr in (
        "ENDPOINT",
        "API_KEY",
        "API_VERSION",
        "DEFAULT_DEPLOYMENT",
        "RESPONSES_DEPLOYMENT",
        "CHAT_DEPLOYMENT",
        "FOUNDRY_DEPLOYMENT",
        "FOUNDRY_PROJECT_ENDPOINT",
        "FOUNDRY_AGENT_NAME",
        "FOUNDRY_AGENT_VERSION",
    ):
        assert hasattr(client, attr), f"client.py missing constant {attr}"


def test_client_factories_return_correct_types():
    from openai import AsyncAzureOpenAI, AzureOpenAI

    from examples import client

    sync_client = client.get_client()
    async_client = client.get_async_client()
    assert isinstance(sync_client, AzureOpenAI)
    assert isinstance(async_client, AsyncAzureOpenAI)


@pytest.mark.parametrize(
    "module_name",
    [
        "e07_responses_chat_loop",
        "e16_chat_completions_chat_loop",
        "e21_responses_tool_function",
    ],
)
def test_interactive_chat_loop_exits_on_quit(module_name, monkeypatch, capsys):
    inputs = iter(["quit"])
    monkeypatch.setattr("builtins.input", lambda *_args: next(inputs))
    module = importlib.import_module(f"examples.{module_name}")
    module.run()
    captured = capsys.readouterr()
    assert "Goodbye" in captured.out
