import importlib
import json
import msvcrt
import os
import subprocess
import sys
from pathlib import Path

EXIT_WORDS = {"quit", "exit", "q", ""}


def _bootstrap_venv():
    """Re-execute under the project's .venv interpreter if not already there.

    Lets `python main.py` work from a fresh shell without manual venv
    activation. Only called when main.py is run as __main__, so tests that
    import main are unaffected.
    """
    project_root = Path(__file__).resolve().parent
    if os.name == "nt":
        venv_python = project_root / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = project_root / ".venv" / "bin" / "python"

    if not venv_python.exists():
        print(
            f"No virtual environment found at {venv_python.parent.parent}.\n"
            "Set it up first:\n"
            "  python -m venv .venv\n"
            "  .\\.venv\\Scripts\\Activate.ps1   (or: source .venv/bin/activate)\n"
            "  pip install -r requirements.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    if Path(sys.executable).resolve() == venv_python.resolve():
        return  # already inside the venv

    result = subprocess.run(
        [str(venv_python), str(Path(__file__).resolve()), *sys.argv[1:]]
    )
    sys.exit(result.returncode)


EXAMPLES = [
    ("Responses API", [
        ("e01_responses_basic", "Basic request"),
        ("e02_responses_metadata", "Inspect response.id / tokens / status"),
        ("e03_responses_instructions", "With instructions (system prompt)"),
        ("e04_responses_params", "With params (temperature, max_output_tokens)"),
        ("e05_responses_foundry_model", "Foundry direct model (e.g. phi-4)"),
        ("e06_responses_multi_turn", "Multi-turn via previous_response_id"),
        ("e07_responses_chat_loop", "Interactive chat loop (previous_response_id)"),
        ("e08_responses_history_input", "Multi-turn via conversation history input"),
        ("e09_responses_retrieve", "Retrieve a previous response by ID"),
        ("e10_responses_streaming", "Streaming (raw events)"),
        ("e11_responses_streaming_filtered", "Streaming filtered to text deltas"),
        ("e12_responses_async", "Async client"),
        ("e13_responses_async_streaming", "Async streaming"),
    ]),
    ("Chat Completions API", [
        ("e14_chat_completions_basic", "Basic request"),
        ("e15_chat_completions_multi_turn", "Manual conversation history"),
        ("e16_chat_completions_chat_loop", "Interactive chat loop"),
    ]),
    ("Foundry Agent (project SDK + Azure AD)", [
        ("e17_foundry_agent_basic", "Call agent via AIProjectClient + DefaultAzureCredential"),
    ]),
    ("Tools (Responses API)", [
        ("e18_responses_tool_code_interpreter", "code_interpreter tool"),
        ("e19_responses_tool_web_search", "web_search tool"),
        ("e20_responses_tool_file_search", "file_search tool (vector store)"),
        ("e21_responses_tool_function", "function tool (interactive get_time)"),
        ("e22_responses_tools_combined", "file_search + web_search (travel assistant)"),
    ]),
]


def _flat():
    return [item for _, items in EXAMPLES for item in items]


def _print_menu():
    print("AI-103 Tutorial Examples")
    print("=" * 28)
    n = 1
    for group_name, items in EXAMPLES:
        print(f"\n{group_name}")
        for _, desc in items:
            print(f"  {n:>2}. {desc}")
            n += 1
    print()


def _resolve(arg):
    flat = _flat()
    if arg.isdigit():
        idx = int(arg) - 1
        if 0 <= idx < len(flat):
            return flat[idx][0]
        return None
    for module_name, _ in flat:
        if arg == module_name or arg == module_name.split("_", 1)[1]:
            return module_name
    return None


def _clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def _print_field(label, value):
    if isinstance(value, dict):
        print(f"{label}:")
        for k, v in value.items():
            display = v if isinstance(v, str) else json.dumps(v)
            print(f"  {k}: {display}")
    elif "\n" in str(value):
        print(f"{label}:")
        for line in str(value).splitlines():
            print(f"  {line}")
    else:
        print(f"{label}: {value}")
    print()


def _run_module(module_name):
    module = importlib.import_module(f"examples.{module_name}")
    print(f"--- {module_name} ---\n")
    for label, attr in (
        ("Description", "DESCRIPTION"),
        ("Instructions", "INSTRUCTIONS"),
        ("Settings", "SETTINGS"),
        ("Prompt", "PROMPT"),
    ):
        value = getattr(module, attr, None)
        if value:
            _print_field(label, value)
    print("Response:")
    module.run()


def main():
    # One-shot mode: `python main.py <selection>` runs once and exits.
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        module_name = _resolve(arg)
        if module_name is None:
            print(f"Unknown selection: {arg}", file=sys.stderr)
            sys.exit(1)
        _run_module(module_name)
        return

    # Interactive mode: clear → run → separator → menu → prompt, repeating.
    while True:
        _print_menu()
        try:
            arg = input("Pick a number (or example module name): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return

        if arg.lower() in EXIT_WORDS:
            return

        module_name = _resolve(arg)
        if module_name is None:
            print(f"Unknown selection: {arg}", file=sys.stderr)
            continue

        _clear_screen()
        _run_module(module_name)
        print()
        print("(Press any key to continue.) ", end="", flush=True)
        msvcrt.getch()
        _clear_screen()


if __name__ == "__main__":
    _bootstrap_venv()
    main()
