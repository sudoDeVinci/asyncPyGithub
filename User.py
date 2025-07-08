from typing import Any

from types import (
    CoroutineType,
)

from _types import (
    UserPlanJSON,
    ErrorMessage,
    JSONDict,
    User,
    UserJSON,
    SimpleUserJSON,
    SimpleUser,
)

from base import (
    req,
    write_json,
    CACHE_DIR
)

from requests import (
    get,
    post,
    put,
    patch,
    Response
)


async def authenticate() -> tuple[int, User | ErrorMessage]:
    """
    Authenticate the user and return their information.
    Or return an error message if authentication fails.
    This function uses the `/user` endpoint to get the authenticated user's information.
    Available: [https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28](https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28)
    """
    try:
        res = await req(
            fn = get,
            url='/user'
        )
        if res.status_code != 200:
            return (
                res.status_code,
                ErrorMessage(
                    code=res.status_code,
                    message=res.json().get('message', 'Unknown error'),
                    endpoint='/user'
                )
            )
        
    except Exception as e:
        return (
            500,
            ErrorMessage(
                code=500,
                message=str(e),
                endpoint='/user'
            )
        )

    return (res.status_code, User(**res.json()))


async def update(
        self: User,
        changes: UserJSON
) -> tuple[int, User | ErrorMessage]:
    """
    Update the authenticated user's information.
    This function uses the `/user` endpoint to update the user's information.
    Available: [https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#update-the-authenticated-user](https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28#update-the-authenticated-user)
    """
    try:
        res = await req(
            fn=patch,
            url='/user',
            json=changes
        )
        if res.status_code != 200:
            return (
                res.status_code,
                ErrorMessage(
                    code=res.status_code,
                    message=res.json().get('message', 'Unknown error'),
                    endpoint='/user'
                )
            )
        
        """
        We would normally do an update to self.__dict__ here,
        but since this is a pydantic model, it uses __slots__,
        so we need to create a new instance with the updated data.
        """
        updated_json = res.json()
        updated_self  = self.model_copy(update=updated_json)
        
    except Exception as e:
        return (
            500,
            ErrorMessage(
                code=500,
                message=str(e),
                endpoint='/user'
            )
        )
    
    return (res.status_code, updated_self)
    

async def get_by_id(uid: int) -> tuple[int, User | ErrorMessage]:
    try:
        res = await req(
            fn=get,
            url=f'/user/{uid}'
        )
        if res.status_code != 200:
            return (
                res.status_code,
                ErrorMessage(
                    code=res.status_code,
                    message=res.json().get('message', 'Unknown error'),
                    endpoint=f'/user/{uid}'
                )
            )

    except Exception as e:
        return (
            500,
            ErrorMessage(
                code=500,
                message=str(e),
                endpoint=f'/user/{uid}'
            )
        )
    
    return (res.status_code, User(**res.json())) 


async def get_by_username(username: str) -> tuple[int, User | ErrorMessage]:
    try:
        res = await req(
            fn=get,
            url=f'/users/{username}'
        )
        if res.status_code != 200:
            return (
                res.status_code,
                ErrorMessage(
                    code=res.status_code,
                    message=res.json().get('message', 'Unknown error'),
                    endpoint=f'/users/{username}'
                )
            )

        return (res.status_code, User(**res.json()))
    except Exception as e:
        return (
            500,
            ErrorMessage(
                code=500,
                message=str(e),
                endpoint=f'/users/{username}'
            )
        )


async def all(
    since: int = 0,
    per_page: int = 30
) -> tuple[int, list[SimpleUser] | ErrorMessage]:
    try:
        res = await req(
            fn=get,
            url='/users',
            params={
                'since': since,
                'per_page': per_page
            }
        )
        if res.status_code != 200:
            return (
                res.status_code,
                ErrorMessage(
                    code=res.status_code,
                    message=res.json().get('message', 'Unknown error'),
                    endpoint='/users'
                )
            )

    except Exception as e:
        return (
            500,
            ErrorMessage(
                code=500,
                message=str(e),
                endpoint='/users'
            )
        )

    return (res.status_code, [SimpleUser(**user) for user in res.json()])









User.update = update
User.authenticate = staticmethod(authenticate)
User.get_by_id = staticmethod(get_by_id)
User.get_by_username = staticmethod(get_by_username)
User.all = staticmethod(all)

UserQueryReturnable = tuple[int, User | SimpleUser | list[SimpleUser] | ErrorMessage]


if __name__ == '__main__':
    import asyncio

    async def main():
        status_code, user = await User.authenticate()
        if status_code != 200:
            print(f">> Error: {user.message} (Code: {user.code})")
            return

        changes = {
            "description": "Swedish developer - Network Security and Hardware Programming | Developer @ CherryTe.ch and HereYouGoPup.com",
        }

        awaitables: list[CoroutineType[UserQueryReturnable, Any, Any]] = [
            user.update(changes),
            User.get_by_id(user.id),
            User.get_by_username(user.login),
            User.all(since=0, per_page=5)
        ]
        results = await asyncio.gather(*awaitables)

        write_json(CACHE_DIR/'user_by_username.json', results[2][1].model_dump(mode='json'))

        for result in results:
            stat, user_or_error = result
            print(f">> Status Code: {stat}")

        
    
    asyncio.run(main())