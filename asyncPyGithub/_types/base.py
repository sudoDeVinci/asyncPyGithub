from __future__ import annotations
from typing_extensions import Self, Callable, Any
from collections.abc import Coroutine as CoroutineType
from pydantic import EmailStr, HttpUrl, PastDatetime


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
        return {"code": self.code, "message": self.message, "endpoint": self.endpoint, "extras": kwargs}

    def dict(self) -> JSONDict:
        """
        Alias for model_dump to maintain compatibility with Pydantic's dict method.

        Returns:
            JSONDict: A dictionary representation of the error message.
        """
        return self.model_dump()


class GitHubPortal:
    """
    Base class for GitHub portals, providing authentication and user management functionality.
    This class is intended to be subclassed for specific GitHub API interactions.
    """

    _authenticated: bool = False

    __slots__ = ()

    @property
    def authenticated(self: Self) -> bool:
        """
        Check if the user is authenticated.
        Returns True if the user is authenticated, False otherwise.
        """
        return self._authenticated


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
