from ._types import (
    ErrorMessage,
    User,
    UserJSON,
    SimpleUser,
)

from asyncPyGithub.base import req

from requests import get, patch


async def authenticate() -> tuple[int, User | ErrorMessage]:
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
                    endpoint="/user",
                ),
            )

    except Exception as e:
        return (500, ErrorMessage(code=500, message=str(e), endpoint="/user"))

    return (res.status_code, User(**res.json()))


async def update(self: User, changes: UserJSON) -> tuple[int, User | ErrorMessage]:
    """
    Update the authenticated user's information.
    This function uses the `/user` endpoint to update the user's information.
    Available: [https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#update-the-authenticated-user](https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#update-the-authenticated-user)
    """
    try:
        res = await req(fn=patch, url="/user", json=changes)
        if res.status_code != 200:
            return (
                res.status_code,
                ErrorMessage(
                    code=res.status_code,
                    message=res.json().get("message", "Unknown error"),
                    endpoint="/user",
                ),
            )

        """
        We would normally do an update to self.__dict__ here,
        but since this is a pydantic model, it uses __slots__,
        so we need to create a new instance with the updated data.
        """
        updated_json = res.json()
        updated_self = self.model_copy(update=updated_json)

    except Exception as e:
        return (500, ErrorMessage(code=500, message=str(e), endpoint="/user"))

    return (res.status_code, updated_self)


async def get_by_id(uid: int) -> tuple[int, User | ErrorMessage]:
    try:
        res = await req(fn=get, url=f"/user/{uid}")
        if res.status_code != 200:
            return (
                res.status_code,
                ErrorMessage(
                    code=res.status_code,
                    message=res.json().get("message", "Unknown error"),
                    endpoint=f"/user/{uid}",
                ),
            )

    except Exception as e:
        return (500, ErrorMessage(code=500, message=str(e), endpoint=f"/user/{uid}"))

    return (res.status_code, User(**res.json()))


async def get_by_username(username: str) -> tuple[int, User | ErrorMessage]:
    try:
        res = await req(fn=get, url=f"/users/{username}")
        if res.status_code != 200:
            return (
                res.status_code,
                ErrorMessage(
                    code=res.status_code,
                    message=res.json().get("message", "Unknown error"),
                    endpoint=f"/users/{username}",
                ),
            )

        return (res.status_code, User(**res.json()))
    except Exception as e:
        return (
            500,
            ErrorMessage(code=500, message=str(e), endpoint=f"/users/{username}"),
        )


async def all(
    since: int = 0, per_page: int = 30
) -> tuple[int, list[SimpleUser] | ErrorMessage]:
    try:
        res = await req(
            fn=get, url="/users", params={"since": since, "per_page": per_page}
        )
        if res.status_code != 200:
            return (
                res.status_code,
                ErrorMessage(
                    code=res.status_code,
                    message=res.json().get("message", "Unknown error"),
                    endpoint="/users",
                ),
            )

    except Exception as e:
        return (500, ErrorMessage(code=500, message=str(e), endpoint="/users"))

    return (res.status_code, [SimpleUser(**user) for user in res.json()])


setattr(User, "update", update)
setattr(User, "authenticate", staticmethod(authenticate))
setattr(User, "get_by_id", staticmethod(get_by_id))
setattr(User, "get_by_username", staticmethod(get_by_username))
setattr(User, "all", staticmethod(all))

UserQueryReturnable = tuple[int, User | SimpleUser | list[SimpleUser] | ErrorMessage]
