from asyncPyGithub import API_ENDPOINT, GitHubUserPortal, read_json
from typing import no_type_check, Final
from responses import RequestsMock, GET, PATCH
from pathlib import Path
from pytest import mark

JSONDIR = Path(__file__).parent.resolve() / "traffic"
USER_ENDPOINT: Final[str] = f"{API_ENDPOINT}/user"
USERS_ENDPOINT: Final[str] = f"{API_ENDPOINT}/users"


@no_type_check
@mark.asyncio
async def test_authenticate_sucessful(mock_requests: RequestsMock) -> None:

    mock_user = read_json(JSONDIR / "authenticate.json")
    mock_requests.add(GET, url=USER_ENDPOINT, json=mock_user, status=200)

    status, resp = await GitHubUserPortal.authenticate()
    assert status == 200, f">> Could not authenticate User portal::{resp}"
    assert (
        GitHubUserPortal.authenticated
    ), f">> Could not authenticate User portal::{resp}"


@no_type_check
@mark.asyncio
async def test_get_by_id_successful(
    mock_requests: RequestsMock,
) -> None:

    mock_response = read_json(JSONDIR / "user_by_id.json")
    assert mock_response is not None, "Mock data could not be loaded."

    url = f"{USER_ENDPOINT}/randomuid"
    mock_requests.add(GET, url, json=mock_response)

    status, resp = await GitHubUserPortal.get_by_id("randomuid")
    assert status == 200, "Could not get User by ID."


@no_type_check
@mark.asyncio
async def test_update_usersuccessful(mock_requests: RequestsMock) -> None:

    mock_response = read_json(JSONDIR / "user_update.json")
    assert mock_response is not None, "Mock data could not be loaded."

    changes = {
        "description": "Swedish developer - Network Security and Hardware Programming | Developer @ CherryTe.ch and HereYouGoPup.com",
    }

    url = USER_ENDPOINT
    mock_requests.add(PATCH, url, json=mock_response)

    status, resp = await GitHubUserPortal.update(changes)
    assert status == 200, "Could not update User."


@no_type_check
@mark.asyncio
async def test_get_by_username_successful(mock_requests: RequestsMock) -> None:

    mock_response = read_json(JSONDIR / "user_by_username.json")
    assert mock_response is not None, "Mock data could not be loaded."

    url = f"{USERS_ENDPOINT}/someusername"
    mock_requests.add(GET, url, json=mock_response)

    status, resp = await GitHubUserPortal.get_by_username("someusername")
    assert status == 200, "Could not get user by username"
