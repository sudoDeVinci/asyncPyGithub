from time import time
import asyncio

from base import (
    LOGGER,
    get_authenticated_user,
    write_json,
    REPOSLICE_JSON,
    USER_JSON,
    CACHE_DIR,
)

from repository import (
    get_organization_repo,
    get_repos_authenticated,
    get_repos_authenticated_extended,
)


async def one_by_one_example() -> None:
    status, user = await get_authenticated_user()
    LOGGER.info(f"Authenticated user: {user['login']} with status code {status}")

    status, repos = await get_organization_repo(organization="cloudflare", per_page=15)
    LOGGER.info(f"Retrieved {len(repos)} repositories with status code {status}")

    status, repos = await get_repos_authenticated(per_page=15)
    LOGGER.info(f"Retrieved {len(repos)} repositories with status code {status}")

    slice = await get_repos_authenticated_extended(per_page=15)
    LOGGER.info(
        f"Retrieved {slice['count']} repos with { '0' if not slice['errors'] else len(slice['errors'])} errors"
    )

    write_json(USER_JSON, user)
    write_json(REPOSLICE_JSON, slice)


async def async_gathered_example() -> None:
    funcs = (
        get_authenticated_user(),
        get_organization_repo(organization="cloudflare", per_page=15),
        get_repos_authenticated(per_page=15),
        get_repos_authenticated_extended(per_page=15),
    )

    results = await asyncio.gather(*funcs)
    status, user = results[0]
    LOGGER.info(f"Authenticated user: {user['login']} with status code {status}")

    status, repos = results[1]
    LOGGER.info(f"Retrieved {len(repos)} repositories with status code {status}")

    status, repos = results[2]
    LOGGER.info(f"Retrieved {len(repos)} repositories with status code {status}")

    slice = results[3]
    LOGGER.info(
        f"Retrieved {slice['count']} repos with { '0' if not slice['errors'] else len(slice['errors'])} errors"
    )

    write_json(USER_JSON, results[0][1])
    write_json(REPOSLICE_JSON, results[3])


if __name__ == "__main__":
    # Ensure the cache directory exists
    assert CACHE_DIR.exists(), "Cache directory does not exist."

    start = time()
    asyncio.run(one_by_one_example())
    end = time()
    LOGGER.info(f"one_by_one_example took {end - start:.2f} seconds")
    print(f"\n>> one_by_one_example took {end - start:.2f} seconds")

    start = time()
    asyncio.run(async_gathered_example())
    end = time()
    LOGGER.info(f"async_gathered_example took {end - start:.2f} seconds")
    print(f"\n>> async_gathered_example took {end - start:.2f} seconds")
