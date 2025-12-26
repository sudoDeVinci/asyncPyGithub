from __future__ import annotations

from asyncio import Lock
from collections.abc import Coroutine as CoroutineType
from contextlib import asynccontextmanager

from httpx import AsyncClient, Limits, Response
from httpx._types import HeaderTypes
from pydantic import EmailStr, HttpUrl, PastDatetime
from typing_extensions import Any, AsyncGenerator, Callable, Final, Literal, Self, cast

from .users import PrivateUser

JSONDict = dict[str, str | int | bool | EmailStr | HttpUrl | PastDatetime | None]


class ErrorMessage:
    """
    Represents an error message with a code and description.

    Attributes:
        code (int): The error code.
        message (str): A description of the error.
        endpoint (str | None): The API endpoint where the error occurred, if applicable.
    """

    __slots__ = ("code", "message", "endpoint")

    def __init__(self, code: int, message: str, endpoint: str | None = None):
        self.code = code
        self.message = message
        self.endpoint = endpoint

    def model_dump(self, **kwargs) -> JSONDict:
        """
        Converts the error message to a JSON-compatible dictionary.

        Returns:
            JSONDict: A dictionary representation of the error message.
        """
        return {"code": self.code, "message": self.message, "endpoint": self.endpoint}

    def dict(self) -> JSONDict:
        """
        Alias for model_dump to maintain compatibility with Pydantic's dict method.

        Returns:
            JSONDict: A dictionary representation of the error message.
        """
        return self.model_dump()

    def json(self) -> JSONDict:
        """
        Alias for model_dump to allow compatability with Requests objects for easier handling.

        Returns:
        """
        return self.model_dump()


class GitHubPortal:
    """
    Base class for GitHub portals, providing authentication and user management functionality.
    This class is intended to be subclassed for specific GitHub API interactions.
    """

    _authenticated: bool = False
    _endpoint: Final[str] = "https://api.github.com"
    _client: AsyncClient | None = None
    _connection_lock: Lock = Lock()
    _version: Final[str] = "2022-11-28"
    _headers = {
        "X-GitHub-Api-Version": _version,
        "User-Agent": "asyncPyGithub/1.0.0",
        "Accept": "application/vnd.github.v3+json",
        "Authorization": None,
    }
    _user: PrivateUser | None = None

    __slots__ = ()

    @property
    def authenticated(self: Self) -> bool:
        """
        Check if the user is authenticated.
        Returns True if the user is authenticated, False otherwise.
        """
        return self._authenticated

    @classmethod
    async def start(
        cls: type["GitHubPortal"],
    ) -> None:
        """
        Initializes the asynchronous HTTP client session.
        """
        async with cls._connection_lock:
            if cls._client is None:
                cls._client = AsyncClient(
                    base_url=cast(str, cls._endpoint),
                    headers=cast(HeaderTypes, cls._headers),
                    timeout=30,
                    http2=False,  # Disable HTTP/2
                    limits=Limits(
                        max_connections=20,
                        max_keepalive_connections=10,
                    ),
                )

    @classmethod
    async def close(
        cls: type["GitHubPortal"],
    ) -> None:
        """
        Closes the asynchronous HTTP client session.
        """
        async with cls._connection_lock:
            if cls._client is not None:
                await cls._client.aclose()
                cls._client = None

    @property
    def user(self: Self) -> PrivateUser | None:
        """
        Get the authenticated user's information as a copy.
        Returns:
            PrivateUser | None: The authenticated user's information, or None if not authenticated.
        """
        return self._user.model_copy() if self._user else None

    @classmethod
    @asynccontextmanager
    async def scoped_client(
        cls: type["GitHubPortal"],
    ) -> AsyncGenerator[AsyncClient, None]:
        """
        Asynchronous context manager for the HTTP client session.
        Yields:
            AsyncClient: The asynchronous HTTP client session.
        """
        await cls.start()
        try:
            yield cls._client  # type: ignore
        finally:
            await cls.close()

    @classmethod
    async def req(
        cls: type["GitHubPortal"],
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
        url: str,
        **kwargs,
    ) -> Response:
        """
        Makes an asynchronous HTTP request to the Github API.
        Args:
            method (str): The HTTP method to use (e.g., 'GET', 'POST').
            url (str): The endpoint URL to which the request will be made.
            **kwargs: Additional keyword arguments to pass to the request.
        Returns:
            Response: The response object returned by the request.
        Raises:
            RuntimeError: If an error occurs while making the request.
        """
        if cls._client is None:
            print("HTTP client is not initialized. Starting client...")
            await cls.start()

        if cls._client is None:
            raise RuntimeError("HTTP client is not initialized.")

        response = await cls._client.request(method, url, **kwargs)

        return response

    @classmethod
    async def authenticate(
        cls: type["GitHubPortal"], token: str
    ) -> tuple[int, PrivateUser | ErrorMessage]:
        """
        Authenticate the user and return their information.
        Or return an error message if authentication fails.
        This function uses the `/user` endpoint to get the authenticated user's information.
        Available: [https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28](https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28)
        """
        try:
            cls._headers["Authorization"] = f"Bearer {token}"
            res = await cls.req("GET", "/user")
            if res.status_code != 200:
                return (
                    res.status_code,
                    ErrorMessage(
                        code=res.status_code,
                        message=res.json().get("message", "Unknown error"),
                        endpoint="/users",
                    ),
                )

            cls._user = PrivateUser(**res.json())

        except Exception as e:
            return (500, ErrorMessage(code=500, message=str(e), endpoint="/user"))

        cls._authenticated = True  # type: ignore[attr-defined]

        return (res.status_code, PrivateUser(**res.json()))


def needs_authentication(
    function: Callable[..., Any],
) -> classmethod[Any, ..., CoroutineType[Any, Any, Any]]:
    async def wrapper(cls: type[GitHubPortal], *args, **kwargs) -> Any:
        # Special case: allow authenticate() to run without being authenticated
        if function.__name__ == "authenticate":
            return await function(cls, *args, **kwargs)

        if not cls._authenticated:
            return (
                401,
                ErrorMessage(
                    code=401,
                    message="User is not authenticated. Please call authenticate() first.",
                    endpoint=kwargs.get("endpoint", None),
                ),
            )

        return await function(cls, *args, **kwargs)

    return classmethod(wrapper)
