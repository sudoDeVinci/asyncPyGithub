from collections.abc import AsyncGenerator, Generator
from os import _Environ, environ
from typing import Final
from unittest.mock import patch

import pytest
import pytest_asyncio
import respx
from httpx import Response

from asyncPyGithub import GitHubPortal

MOCK_ENV_VARS: Final[dict[str, str]] = {"GITHUB_TOKEN": "mock_token"}
API_BASE_URL: Final[str] = "https://api.github.com"


@pytest.fixture
def mock_requests() -> Generator[respx.MockRouter, None, None]:
    """
    Fixture for mocking HTTP requests with respx (httpx mock).
    """
    with respx.mock(base_url=API_BASE_URL) as rsps:
        yield rsps


@pytest_asyncio.fixture(autouse=True)
async def reset_portal_state() -> AsyncGenerator[None, None]:
    """
    Reset GitHubPortal state before and after each test.
    """
    # Reset before test
    GitHubPortal._authenticated = False
    GitHubPortal._client = None
    GitHubPortal._headers["Authorization"] = None

    yield

    # Cleanup after test
    if GitHubPortal._client is not None:
        await GitHubPortal.close()
    GitHubPortal._authenticated = False
    GitHubPortal._headers["Authorization"] = None


@pytest.fixture(scope="session")
def mock_environment() -> Generator[_Environ[str], None, None]:
    """
    Fixture to mock environment variables for testing.
    Sets GITHUB_TOKEN and API_VERSION to known values.
    """
    with patch.dict(environ, MOCK_ENV_VARS):
        yield environ
