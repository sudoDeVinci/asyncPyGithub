from types import CoroutineType
from typing import Any, no_type_check
from asyncPyGithub import User, UserQueryReturnable, write_json, CACHE_DIR

if __name__ == "__main__":
    import asyncio

    @no_type_check
    async def main() -> None:
        status_code, user = await User.authenticate()
        if status_code != 200:
            print(f">> Error: {user.message} (Code: {user.code})")
            return

        changes = {
            "description": "Swedish developer - Network Security and Hardware Programming | Developer @ CherryTe.ch and HereYouGoPup.com",
        }

        awaitables: list[CoroutineType[Any, Any, UserQueryReturnable]] = [
            user.update(changes),
            User.get_by_id(user.id),
            User.get_by_username(user.login),
            User.all(since=0, per_page=5),
        ]
        results = await asyncio.gather(*awaitables)

        write_json(
            CACHE_DIR / "user_by_username.json", results[2][1].model_dump(mode="json")
        )

        for result in results:
            stat, user_or_error = result
            print(f">> Status Code: {stat}")

    asyncio.run(main())
