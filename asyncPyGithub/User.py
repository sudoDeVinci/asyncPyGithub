from ._types import (
    ErrorMessage,
    PrivateUser,
    SimpleUserJSON,
    SimpleUser,
    HoverCard,
    HoverCardJSON,
    HoverCardContext,
    HoverCardContextJSON,
    GitHubPortal,
    needs_authentication,
)

from .base import req

from requests import get, patch
from typing import Final, Literal


UserQueryReturnable = tuple[
    int, PrivateUser | SimpleUser | list[SimpleUser] | ErrorMessage
]

USER_ENDPOINT: Final[Literal["/user"]] = "/user"
USERS_ENDPOINT: Final[Literal["/users"]] = "/users"


class GitHubUserPortal(GitHubPortal):

    @classmethod
    async def authenticate(
        cls: type["GitHubUserPortal"],
    ) -> tuple[int, PrivateUser | ErrorMessage]:
        """
        Authenticate the user and return their information.
        Or return an error message if authentication fails.
        This function uses the `/user` endpoint to get the authenticated user's information.
        Available: [https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28](https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28)
        """
        try:
            res = await req(fn=get, url="/user")
            if res.status_code != 200:
                return (
                    res.status_code,
                    ErrorMessage(
                        code=res.status_code,
                        message=res.json().get("message", "Unknown error"),
                        endpoint=USER_ENDPOINT,
                    ),
                )

        except Exception as e:
            return (500, ErrorMessage(code=500, message=str(e), endpoint="/user"))

        cls.__bases__[0]._authenticated = True  # type: ignore[attr-defined]
        return (res.status_code, PrivateUser(**res.json()))

    @needs_authentication
    async def update(
        cls: "GitHubUserPortal", changes: SimpleUserJSON
    ) -> tuple[int, PrivateUser | ErrorMessage]:
        """
        Update the authenticated user's information.
        This function uses the `/user` endpoint to update the user's information.
        Available: [https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#update-the-authenticated-user](https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#update-the-authenticated-user)
        """
        endpoint = USER_ENDPOINT
        try:
            res = await req(fn=patch, url=endpoint, json=changes)
            if res.status_code != 200:
                return (
                    res.status_code,
                    ErrorMessage(
                        code=res.status_code,
                        message=res.json().get("message", "Unknown error"),
                        endpoint=endpoint,
                    ),
                )

            """
            We would normally do an update to self.__dict__ here,
            but since this is a pydantic model, it uses __slots__,
            so we need to create a new instance with the updated data.
            """
            updated_json = res.json()
            updated_self = PrivateUser(**updated_json)

        except Exception as e:
            return (500, ErrorMessage(code=500, message=str(e), endpoint=endpoint))

        return (res.status_code, updated_self)

    @needs_authentication
    async def get_by_id(
        cls: "GitHubUserPortal", uid: int
    ) -> tuple[int, PrivateUser | ErrorMessage]:
        endpoint = f"{USER_ENDPOINT}/{uid}"
        try:
            res = await req(fn=get, url=endpoint)
            if res.status_code != 200:
                return (
                    res.status_code,
                    ErrorMessage(
                        code=res.status_code,
                        message=res.json().get("message", "Unknown error"),
                        endpoint=endpoint,
                    ),
                )

        except Exception as e:
            return (
                500,
                ErrorMessage(code=500, message=str(e), endpoint=endpoint),
            )

        return (res.status_code, PrivateUser(**res.json()))

    @needs_authentication
    async def get_by_username(
        cls: "GitHubUserPortal", username: str
    ) -> tuple[int, PrivateUser | ErrorMessage]:
        endpoint = f"{USERS_ENDPOINT}/{username}"
        try:
            res = await req(fn=get, url=endpoint)
            if res.status_code != 200:
                return (
                    res.status_code,
                    ErrorMessage(
                        code=res.status_code,
                        message=res.json().get("message", "Unknown error"),
                        endpoint=endpoint,
                    ),
                )

            return (res.status_code, PrivateUser(**res.json()))
        except Exception as e:
            return (
                500,
                ErrorMessage(code=500, message=str(e), endpoint=endpoint),
            )

    @needs_authentication
    async def all(
        cls: "GitHubUserPortal", since: int = 0, per_page: int = 30
    ) -> tuple[int, list[SimpleUser] | ErrorMessage]:
        try:
            res = await req(
                fn=get,
                url=USERS_ENDPOINT,
                params={"since": since, "per_page": per_page},
            )
            if res.status_code != 200:
                return (
                    res.status_code,
                    ErrorMessage(
                        code=res.status_code,
                        message=res.json().get("message", "Unknown error"),
                        endpoint=USERS_ENDPOINT,
                    ),
                )

        except Exception as e:
            return (
                500,
                ErrorMessage(code=500, message=str(e), endpoint=USERS_ENDPOINT),
            )

        return (res.status_code, [SimpleUser(**user) for user in res.json()])

    @needs_authentication
    async def get_hovercard(
        cls: "GitHubUserPortal", username: str
    ) -> tuple[int, HoverCard | ErrorMessage]:
        """
        Get the hovercard information for a user.
        This function uses the `/users/{username}/hovercard` endpoint to get the hovercard information.
        Available: [https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#view-a-user-hovercard](https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#view-a-user-hovercard)
        """
        endpoint = f"{USERS_ENDPOINT}/{username}/hovercard"
        try:
            res = await req(fn=get, url=endpoint)
            if res.status_code != 200:
                return (
                    res.status_code,
                    ErrorMessage(
                        code=res.status_code,
                        message=res.json().get("message", "Unknown error"),
                        endpoint=endpoint,
                    ),
                )

            cardjson: HoverCardJSON = res.json()
            contexts: list[HoverCardContextJSON] = cardjson.get("contexts", [])
            contexts_checked: list[HoverCardContext] = [
                HoverCardContext(**context) for context in contexts
            ]  # type: ignore[call-arg]
            return (res.status_code, HoverCard(contexts=contexts_checked))

        except Exception as e:
            return (
                500,
                ErrorMessage(code=500, message=str(e), endpoint=endpoint),
            )
