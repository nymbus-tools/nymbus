from pathlib import Path

import pytest


@pytest.fixture
def data_location() -> Path:
    return Path(__file__).parent/"data"

