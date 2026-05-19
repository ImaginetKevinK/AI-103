import importlib
import io
from contextlib import redirect_stdout

import pytest


@pytest.mark.integration
def test_e17_foundry_agent_basic_runs_against_live_endpoint():
    module = importlib.import_module("examples.e17_foundry_agent_basic")
    buf = io.StringIO()
    with redirect_stdout(buf):
        module.run()
    output = buf.getvalue()
    assert "Response output:" in output
    assert len(output.strip()) > len("Response output:") + 20
