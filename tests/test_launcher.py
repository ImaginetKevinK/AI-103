import io
from contextlib import redirect_stdout

import pytest

import main


def test_flat_count():
    assert len(main._flat()) == 22


def test_first_and_last_examples():
    flat = main._flat()
    assert flat[0][0] == "e01_responses_basic"
    assert flat[-1][0] == "e22_responses_tools_combined"


def test_examples_grouped_in_order():
    groups = [name for name, _ in main.EXAMPLES]
    assert groups == [
        "Responses API",
        "Chat Completions API",
        "Foundry Agent (project SDK + Azure AD)",
        "Tools (Responses API)",
    ]


@pytest.mark.parametrize("n", range(1, 23))
def test_resolve_by_number(n):
    flat = main._flat()
    assert main._resolve(str(n)) == flat[n - 1][0]


@pytest.mark.parametrize(
    "name",
    [
        "e01_responses_basic",
        "e07_responses_chat_loop",
        "e13_responses_async_streaming",
        "e14_chat_completions_basic",
        "e17_foundry_agent_basic",
        "e18_responses_tool_code_interpreter",
        "e22_responses_tools_combined",
    ],
)
def test_resolve_by_full_module_name(name):
    assert main._resolve(name) == name


@pytest.mark.parametrize(
    "short_name,expected",
    [
        ("responses_basic", "e01_responses_basic"),
        ("responses_metadata", "e02_responses_metadata"),
        ("responses_chat_loop", "e07_responses_chat_loop"),
        ("responses_async_streaming", "e13_responses_async_streaming"),
        ("chat_completions_basic", "e14_chat_completions_basic"),
        ("chat_completions_chat_loop", "e16_chat_completions_chat_loop"),
        ("foundry_agent_basic", "e17_foundry_agent_basic"),
        ("responses_tool_code_interpreter", "e18_responses_tool_code_interpreter"),
        ("responses_tool_function", "e21_responses_tool_function"),
        ("responses_tools_combined", "e22_responses_tools_combined"),
    ],
)
def test_resolve_by_short_name(short_name, expected):
    assert main._resolve(short_name) == expected


@pytest.mark.parametrize(
    "arg",
    [
        "0",
        "99",
        "100",
        "-1",
        "1.5",
        "abc",
        "",
        " ",
        "foo",
        "basic",
        "responses",
        "RESPONSES_BASIC",
    ],
)
def test_resolve_invalid_returns_none(arg):
    assert main._resolve(arg) is None


def test_print_menu_contains_all_groups_and_numbers():
    buf = io.StringIO()
    with redirect_stdout(buf):
        main._print_menu()
    out = buf.getvalue()
    assert "AI-103 Tutorial Examples" in out
    assert "Responses API" in out
    assert "Chat Completions API" in out
    assert "Foundry Agent" in out
    assert "Tools (Responses API)" in out
    for n in range(1, 23):
        assert f"{n:>2}." in out


def test_main_with_invalid_arg_exits_with_error(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["main.py", "nonexistent_example"])
    with pytest.raises(SystemExit) as excinfo:
        main.main()
    assert excinfo.value.code == 1
    captured = capsys.readouterr()
    assert "Unknown selection" in captured.err


def test_main_without_arg_prints_menu_and_reads_input(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["main.py"])
    inputs = iter(["nonexistent", "quit"])
    monkeypatch.setattr("builtins.input", lambda *_args: next(inputs))
    main.main()
    captured = capsys.readouterr()
    assert "AI-103 Tutorial Examples" in captured.out
    assert "Unknown selection" in captured.err


def test_main_interactive_exits_on_quit(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["main.py"])
    monkeypatch.setattr("builtins.input", lambda *_args: "quit")
    main.main()
    captured = capsys.readouterr()
    assert "AI-103 Tutorial Examples" in captured.out


def test_main_interactive_exits_on_eof(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["main.py"])

    def _raise_eof(*_args):
        raise EOFError

    monkeypatch.setattr("builtins.input", _raise_eof)
    main.main()
    captured = capsys.readouterr()
    assert "AI-103 Tutorial Examples" in captured.out
