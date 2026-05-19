import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def pytest_addoption(parser):
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="Run integration tests that call live Azure endpoints (costs tokens, requires az login)",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "integration: marks tests that hit live Azure endpoints (deselect with -m 'not integration')",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--integration"):
        return
    skip_integration = pytest.mark.skip(reason="needs --integration flag")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)
