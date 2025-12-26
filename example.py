import asyncio
from os import environ
from types import CoroutineType
from typing import Any, no_type_check

from dotenv import load_dotenv  # type: ignore

from asyncPyGithub import (
    CACHE_DIR,
    GitHubPortal,
    GitHubRepositoryPortal,
    GitHubUserPortal,
    UserQueryReturnable,
    write_json,
)
from asyncPyGithub.base import LOGGER

try:
    assert load_dotenv(
        verbose=True
    ), "Failed to load environment variables from .env file."
    TOKEN = environ.get("GITHUB_TOKEN", environ.get("TOKEN", None))

    assert TOKEN is not None, "GITHUB_TOKEN must be set in environment variables."
except (AssertionError, AttributeError, OSError) as err:
    LOGGER.error(f"Error during global configuration:::{err}")


@no_type_check
async def main() -> None:
    if not GitHubPortal._authenticated:
        status_code, user = await GitHubPortal.authenticate(TOKEN)
        if status_code != 200:
            print(f">> Error: {user.message} (Code: {user.code})")
            return

        write_json(CACHE_DIR / "authenticate.json", user.model_dump(mode="json"))

    user = GitHubPortal._user  # type: ignore[attr-defined]
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

    write_json(CACHE_DIR / "user_update.json", results[0][1].model_dump(mode="json"))
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


if __name__ == "__main__":
    asyncio.run(main())
