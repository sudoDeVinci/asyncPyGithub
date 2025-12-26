from pathlib import Path
from typing import Final, cast, no_type_check

import respx
from httpx import Response
from pytest import mark

from asyncPyGithub import (
    ErrorMessage,
    GitHubPortal,
    GitHubUserPortal,
    PrivateUser,
    SimpleUser,
    SimpleUserJSON,
    read_json,
)

JSONDIR = Path(__file__).parent.resolve() / "traffic"
USER_ENDPOINT: Final[str] = "/user"
USERS_ENDPOINT: Final[str] = "/users"


@no_type_check
@mark.asyncio
async def test_authenticate_sucessful(mock_requests: respx.MockRouter) -> None:
    mock_user = read_json(JSONDIR / "authenticate.json")
    mock_requests.get(USER_ENDPOINT).mock(return_value=Response(200, json=mock_user))

    response: tuple[int, PrivateUser | ErrorMessage] = await GitHubPortal.authenticate(
        "mock_token"
    )
    status, user = response
    assert status == 200, f">> Could not authenticate User portal::{user}"
    assert isinstance(user, PrivateUser), "Expected a PrivateUser instance."
    user = cast(PrivateUser, user)
    assert GitHubPortal._authenticated, f">> Could not authenticate User portal::{user}"
    assert user.model_dump(mode="json") == mock_user, (
        f"User data mismatch: {user.model_dump(mode='json')} != {mock_user}"
    )


@no_type_check
@mark.asyncio
async def test_authenticate_unsuccessful(mock_requests: respx.MockRouter) -> None:
    mock_error = {"message": "Bad credentials", "code": 401}
    mock_requests.get(USER_ENDPOINT).mock(return_value=Response(401, json=mock_error))

    response: tuple[int, PrivateUser | ErrorMessage] = await GitHubPortal.authenticate(
        "bad_token"
    )
    status, user = response

    assert status == 401, f">> Expected 401 Unauthorized, got {status}"
    assert isinstance(user, ErrorMessage), "Expected an ErrorMessage instance."
    user = cast(ErrorMessage, user)
    assert user.code == 401, f">> Expected error code 401, got {user.code}"


@no_type_check
@mark.asyncio
async def test_get_by_id_successful(mock_requests: respx.MockRouter) -> None:
    # First authenticate
    mock_auth = read_json(JSONDIR / "authenticate.json")
    mock_requests.get(USER_ENDPOINT).mock(return_value=Response(200, json=mock_auth))
    await GitHubPortal.authenticate("mock_token")

    mock_response = read_json(JSONDIR / "user_by_id.json")
    assert mock_response is not None, "Mock data could not be loaded."

    mock_requests.get(f"{USER_ENDPOINT}/randomuid").mock(
        return_value=Response(200, json=mock_response)
    )

    response: tuple[int, PrivateUser | ErrorMessage] = await GitHubUserPortal.get_by_id(
        "randomuid"
    )
    status, user = response
    assert status == 200, "Could not get User by ID."
    assert isinstance(user, PrivateUser), "Expected a PrivateUser instance."
    user = cast(PrivateUser, user)
    assert user.model_dump(mode="json") == mock_response, (
        f"User data mismatch: {user.model_dump(mode='json')} != {mock_response}"
    )


@no_type_check
@mark.asyncio
async def test_get_by_id_unsuccessful(mock_requests: respx.MockRouter) -> None:
    # First authenticate
    mock_auth = read_json(JSONDIR / "authenticate.json")
    mock_requests.get(USER_ENDPOINT).mock(return_value=Response(200, json=mock_auth))
    await GitHubPortal.authenticate("mock_token")

    mock_error = {"message": "User not found", "code": 404}
    mock_requests.get(f"{USER_ENDPOINT}/nonexistent").mock(
        return_value=Response(404, json=mock_error)
    )

    response: tuple[int, PrivateUser | ErrorMessage] = await GitHubUserPortal.get_by_id(
        "nonexistent"
    )
    status, user = response
    assert status == 404, "Expected 404 Not Found."
    assert isinstance(user, ErrorMessage), "Expected an ErrorMessage instance."
    user = cast(ErrorMessage, user)
    assert user.code == 404, f"Expected error code 404, got {user.code}"


@no_type_check
@mark.asyncio
async def test_update_user_successful(mock_requests: respx.MockRouter) -> None:
    # First authenticate
    mock_auth = read_json(JSONDIR / "authenticate.json")
    mock_requests.get(USER_ENDPOINT).mock(return_value=Response(200, json=mock_auth))
    await GitHubPortal.authenticate("mock_token")

    mock_response = read_json(JSONDIR / "user_update.json")
    assert mock_response is not None, "Mock data could not be loaded."

    changes = {
        "description": "Swedish developer - Network Security and Hardware Programming | Developer @ CherryTe.ch and HereYouGoPup.com",
    }

    mock_requests.patch(USER_ENDPOINT).mock(
        return_value=Response(200, json=mock_response)
    )

    response: tuple[int, PrivateUser | ErrorMessage] = await GitHubUserPortal.update(
        changes
    )
    status, user = response
    assert status == 200, "Could not update User."
    assert isinstance(user, PrivateUser), "Expected a PrivateUser instance."
    user = cast(PrivateUser, user)
    assert user.model_dump(mode="json") == mock_response, (
        f"User data mismatch: {user.model_dump(mode='json')} != {mock_response}"
    )


@no_type_check
@mark.asyncio
async def test_update_user_unsuccessful(mock_requests: respx.MockRouter) -> None:
    # First authenticate
    mock_auth = read_json(JSONDIR / "authenticate.json")
    mock_requests.get(USER_ENDPOINT).mock(return_value=Response(200, json=mock_auth))
    await GitHubPortal.authenticate("mock_token")

    mock_error = {"message": "Invalid request", "code": 400}
    changes = {
        "description": "Invalid update",
    }

    mock_requests.patch(USER_ENDPOINT).mock(return_value=Response(400, json=mock_error))

    response: tuple[int, PrivateUser | ErrorMessage] = await GitHubUserPortal.update(
        changes
    )
    status, user = response
    assert status == 400, "Expected 400 Bad Request."
    assert isinstance(user, ErrorMessage), "Expected an ErrorMessage instance."
    user = cast(ErrorMessage, user)
    assert user.code == 400, f"Expected error code 400, got {user.code}"


@no_type_check
@mark.asyncio
async def test_get_by_username_successful(mock_requests: respx.MockRouter) -> None:
    # First authenticate
    mock_auth = read_json(JSONDIR / "authenticate.json")
    mock_requests.get(USER_ENDPOINT).mock(return_value=Response(200, json=mock_auth))
    await GitHubPortal.authenticate("mock_token")

    mock_response = read_json(JSONDIR / "user_by_username.json")
    assert mock_response is not None, "Mock data could not be loaded."

    mock_requests.get(f"{USERS_ENDPOINT}/someusername").mock(
        return_value=Response(200, json=mock_response)
    )

    response: tuple[
        int, PrivateUser | ErrorMessage
    ] = await GitHubUserPortal.get_by_username("someusername")
    status, user = response

    assert status == 200, "Could not get user by username"
    assert isinstance(user, PrivateUser), "Expected a PrivateUser instance."
    user = cast(PrivateUser, user)
    assert user.model_dump(mode="json") == mock_response, (
        f"User data mismatch: {user.model_dump(mode='json')} != {mock_response}"
    )


@no_type_check
@mark.asyncio
async def test_get_by_username_unsuccessful(mock_requests: respx.MockRouter) -> None:
    # First authenticate
    mock_auth = read_json(JSONDIR / "authenticate.json")
    mock_requests.get(USER_ENDPOINT).mock(return_value=Response(200, json=mock_auth))
    await GitHubPortal.authenticate("mock_token")

    mock_error = {"message": "User not found", "code": 404}
    mock_requests.get(f"{USERS_ENDPOINT}/nonexistentuser").mock(
        return_value=Response(404, json=mock_error)
    )

    response: tuple[
        int, PrivateUser | ErrorMessage
    ] = await GitHubUserPortal.get_by_username("nonexistentuser")
    status, user = response
    assert status == 404, "Expected 404 Not Found."
    assert isinstance(user, ErrorMessage), "Expected an ErrorMessage instance."
    user = cast(ErrorMessage, user)
    assert user.code == 404, f"Expected error code 404, got {user.code}"


@no_type_check
@mark.asyncio
async def test_get_all_users_pg01_pp05(mock_requests: respx.MockRouter) -> None:
    """
    Test for the get_all_users method.
    This is a test for the 0.0.5 version of the API.
    """
    # First authenticate
    mock_auth = read_json(JSONDIR / "authenticate.json")
    mock_requests.get(USER_ENDPOINT).mock(return_value=Response(200, json=mock_auth))
    await GitHubPortal.authenticate("mock_token")

    mock_response = cast(
        list[SimpleUserJSON], read_json(JSONDIR / "all_users_page1_pp5.json")
    )
    assert mock_response is not None, "Mock data could not be loaded."

    mock_requests.get(USERS_ENDPOINT).mock(
        return_value=Response(200, json=mock_response)
    )

    response: tuple[int, list[SimpleUser] | ErrorMessage] = await GitHubUserPortal.all(
        per_page=5
    )
    status, users = response
    assert status == 200, "Could not get all users."
    assert len(users) == 5, "Expected 5 users, got a different number."
    assert isinstance(users, list), "Expected a list of SimpleUser instances."
    assert all(isinstance(user, SimpleUser) for user in users), (
        "Expected all items to be SimpleUser instances."
    )

    users = cast(list[SimpleUser], users)
    for mock_user, user in zip(mock_response, users):
        assert user.model_dump(mode="json") == mock_user, (
            f"User data mismatch: {user.model_dump(mode='json')} != {mock_user}"
        )
