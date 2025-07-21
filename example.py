from types import CoroutineType
from typing import Any, no_type_check
from asyncPyGithub import (
    write_json,
    CACHE_DIR,
    GitHubUserPortal,
    UserQueryReturnable,
    GitHubRepositoryPortal,
)


if __name__ == "__main__":
    import asyncio

    @no_type_check
    async def main() -> None:
        status_code, user = await GitHubUserPortal.authenticate()
        if status_code != 200:
            print(f">> Error: {user.message} (Code: {user.code})")
            return

        write_json(CACHE_DIR / "authenticate.json", user.model_dump(mode="json"))

        changes = {
            "description": "Swedish developer - Network Security and Hardware Programming | Developer @ CherryTe.ch and HereYouGoPup.com",
        }

        awaitables: list[CoroutineType[Any, Any, UserQueryReturnable]] = [
            GitHubUserPortal.update(changes),
            GitHubUserPortal.get_by_id(user.id),
            GitHubUserPortal.get_by_username(user.login),
            GitHubUserPortal.all(since=0, per_page=5),
            GitHubUserPortal.get_hovercard(user.login),
            GitHubRepositoryPortal.get_organization_repos(
                organization="LEGO",
                type="all",
                sort="full_name",
                direction="asc",
                per_page=5,
                page=1,
            ),
        ]
        results = await asyncio.gather(*awaitables)

        write_json(
            CACHE_DIR / "user_update.json", results[0][1].model_dump(mode="json")
        )
        write_json(CACHE_DIR / "user_by_id.json", results[1][1].model_dump(mode="json"))
        write_json(
            CACHE_DIR / "user_by_username.json", results[2][1].model_dump(mode="json")
        )
        write_json(
            CACHE_DIR / "all_users_page1_pp5.json",
            (
                [user.model_dump(mode="json") for user in results[3][1]]
                if isinstance(results[3][1], list)
                else results[3][1].model_dump(mode="json")
            ),
        )
        write_json(CACHE_DIR / "hovercard.json", results[4][1].model_dump(mode="json"))
        write_json(
            CACHE_DIR / "org_repos.json",
            (
                [repo.model_dump(mode="json") for repo in results[5][1]]
                if isinstance(results[5][1], list)
                else results[5][1].model_dump(mode="json")
            ),
        )

        for result in results:
            stat, _ = result
            print(f">> Status Code: {stat}")

    asyncio.run(main())
