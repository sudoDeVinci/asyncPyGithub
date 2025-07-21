from asyncPyGithub import (
    API_ENDPOINT,
    GitHubUserPortal,
    read_json,
    SimpleUser,
    SimpleUserJSON,
    PrivateUser,
    PrivateUserJSON,
    ErrorMessage
)

from typing import no_type_check, Final, cast
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

    response: tuple[int, PrivateUser | ErrorMessage]  = await GitHubUserPortal.authenticate()
    status, user = response
    assert status == 200, f">> Could not authenticate User portal::{resp}"
    assert isinstance(user, PrivateUser), "Expected a PrivateUser instance."
    user = cast(PrivateUser, user)
    assert (
        GitHubUserPortal.authenticated
    ), f">> Could not authenticate User portal::{user}"
    assert user.model_dump(mode="json") == mock_user, f"User data mismatch: {user.model_dump(mode='json')} != {mock_user}"


@no_type_check
@mark.asyncio
async def test_authenticate_unsuccessful(mock_requests: RequestsMock) -> None:

    mock_error = {"message": "Bad credentials", "code": 401}
    mock_requests.add(GET, url=USER_ENDPOINT, json=mock_error, status=401)

    response: tuple[int, PrivateUser | ErrorMessage] = await GitHubUserPortal.authenticate()
    status, user = response
    
    assert status == 401, f">> Expected 401 Unauthorized, got {status}"
    assert isinstance(user, ErrorMessage), "Expected an ErrorMessage instance."
    user = cast(ErrorMessage, user)
    assert user.code == 401, f">> Expected error code 401, got {user.code}"


@no_type_check
@mark.asyncio
async def test_get_by_id_successful(
    mock_requests: RequestsMock,
) -> None:

    mock_response = read_json(JSONDIR / "user_by_id.json")
    assert mock_response is not None, "Mock data could not be loaded."

    url = f"{USER_ENDPOINT}/randomuid"
    mock_requests.add(GET, url, json=mock_response)

    response: tuple[int, PrivateUser | ErrorMessage] = await GitHubUserPortal.get_by_id("randomuid")
    status, user = response
    assert status == 200, "Could not get User by ID."
    assert isinstance(user, PrivateUser), "Expected a PrivateUser instance."
    user = cast(PrivateUser, user)
    assert user.model_dump(mode="json") == mock_response, f"User data mismatch: {user.model_dump(mode='json')} != {mock_response}"


@no_type_check
@mark.asyncio
async def test_get_by_id_unsuccessful(
    mock_requests: RequestsMock,
) -> None:
    
    mock_error = {"message": "User not found", "code": 404}
    mock_requests.add(GET, f"{USER_ENDPOINT}/nonexistent", json=mock_error, status=404)

    response: tuple[int, PrivateUser | ErrorMessage] = await GitHubUserPortal.get_by_id("nonexistent")
    status, user = response
    assert status == 404, "Expected 404 Not Found."
    assert isinstance(user, ErrorMessage), "Expected an ErrorMessage instance."
    user = cast(ErrorMessage, user)
    assert user.code == 404, f"Expected error code 404, got {user.code}"


@no_type_check
@mark.asyncio
async def test_update_user_successful(mock_requests: RequestsMock) -> None:

    mock_response = read_json(JSONDIR / "user_update.json")
    assert mock_response is not None, "Mock data could not be loaded."

    changes = {
        "description": "Swedish developer - Network Security and Hardware Programming | Developer @ CherryTe.ch and HereYouGoPup.com",
    }

    url = USER_ENDPOINT
    mock_requests.add(PATCH, url, json=mock_response)

    response: tuple[int, PrivateUser | ErrorMessage] = await GitHubUserPortal.update(changes)
    status, user = response
    assert status == 200, "Could not update User."
    assert isinstance(user, PrivateUser), "Expected a PrivateUser instance."
    user = cast(PrivateUser, user)
    assert user.model_dump(mode="json") == mock_response, f"User data mismatch: {user.model_dump(mode='json')} != {mock_response}"


@no_type_check
@mark.asyncio
async def test_update_user_unsuccessful(mock_requests: RequestsMock) -> None:

    mock_error = {"message": "Invalid request", "code": 400}
    changes = {
        "description": "Invalid update",
    }

    url = USER_ENDPOINT
    mock_requests.add(PATCH, url, json=mock_error, status=400)

    response: tuple[int, PrivateUser | ErrorMessage] = await GitHubUserPortal.update(changes)
    status, user = response
    assert status == 400, "Expected 400 Bad Request."
    assert isinstance(user, ErrorMessage), "Expected an ErrorMessage instance."
    user = cast(ErrorMessage, user)
    assert user.code == 400, f"Expected error code 400, got {user.code}"


@no_type_check
@mark.asyncio
async def test_get_by_username_successful(mock_requests: RequestsMock) -> None:

    mock_response = read_json(JSONDIR / "user_by_username.json")
    assert mock_response is not None, "Mock data could not be loaded."

    url = f"{USERS_ENDPOINT}/someusername"
    mock_requests.add(GET, url, json=mock_response)

    response: tuple[int, PrivateUser | ErrorMessage] = await GitHubUserPortal.get_by_username("someusername")
    status, user = response

    assert status == 200, "Could not get user by username"
    assert isinstance(user, PrivateUser), "Expected a PrivateUser instance."
    user = cast(PrivateUser, user)
    assert user.model_dump(mode="json") == mock_response, f"User data mismatch: {user.model_dump(mode='json')} != {mock_response}"


@no_type_check
@mark.asyncio
async def test_get_by_username_unsuccessful(mock_requests: RequestsMock) -> None:  

    mock_error = {"message": "User not found", "code": 404}
    mock_requests.add(GET, f"{USERS_ENDPOINT}/nonexistentuser", json=mock_error, status=404)

    response: tuple[int, PrivateUser | ErrorMessage] = await GitHubUserPortal.get_by_username("nonexistentuser")
    status, user = response
    assert status == 404, "Expected 404 Not Found."
    assert isinstance(user, ErrorMessage), "Expected an ErrorMessage instance."
    user = cast(ErrorMessage, user)
    assert user.code == 404, f"Expected error code 404, got {user.code}"


@no_type_check
@mark.asyncio
async def test_get_all_users_pg01_pp05(
    mock_requests: RequestsMock,
) -> None:
    """
    Test for the get_all_users method.
    This is a test for the 0.0.5 version of the API.
    """
    mock_response = cast(list[SimpleUserJSON], read_json(JSONDIR / "all_users_page1_pp5.json"))
    assert mock_response is not None, "Mock data could not be loaded."

    url = USERS_ENDPOINT
    mock_requests.add(GET, url, json=mock_response)

    response: tuple[int, list[SimpleUser] | ErrorMessage] = await GitHubUserPortal.all(per_page=5)
    status, users = response
    assert status == 200, "Could not get all users."
    assert len(users) == 5, "Expected 5 users, got a different number."
    assert isinstance(users, list), "Expected a list of SimpleUser instances."
    assert all(isinstance(user, SimpleUser) for user in users), "Expected all items to be SimpleUser instances."
    
    users = cast(list[SimpleUser], users)
    for mock_user, user in zip(mock_response, users):
        assert user.model_dump(mode="json") == mock_user, f"User data mismatch: {user.model_dump(mode='json')} != {mock_user}"
