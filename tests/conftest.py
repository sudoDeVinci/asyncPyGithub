from collections.abc import Generator
from pathlib import Path
import pytest
from unittest.mock import patch
from responses import RequestsMock
from os import environ, _Environ
from typing import (
    Final
)

MOCK_ENV_VARS: Final[dict[str, str]] = {
    "GITHUB_TOKEN": "mock_token"
}

@pytest.fixture(autouse=True)
def mock_requests() -> Generator[RequestsMock, None, None]:
    """
    Fixture for mocking HTTP requests
    """
    with RequestsMock() as rsps:
        yield rsps

@pytest.fixture(scope="session")
def mock_environment() -> Generator[_Environ[str], None, None]:
    """
    Fixture to mock environment variables for testing.
    Sets GITHUB_TOKEN and API_VERSION to known values.
    """
    with patch.dict(environ, MOCK_ENV_VARS):
        yield environ


