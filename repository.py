from requests import get
from time import time
import asyncio
from types import CoroutineType
from typing import cast, Any, Literal, Sequence
from base import req, LOGGER
from _types import (
    Repository,
    RepoSlice,
    ErrorMessage,
    RepositoryType,
    RepoSortDirection,
    RepoSortCriterion,
    RepoVisibility,
)


async def get_organization_repo(
    organization: str,
    type: RepositoryType = "all",
    sort: RepoSortCriterion = "full_name",
    direction: RepoSortDirection = "asc",
    per_page: int = 30,
    page: int = 1,
) -> tuple[int, list[Repository]]:
    """
    Lists repositories for the specified organization.
    This endpoint can be used without authentication, or
    with read access to public repositories.
    """
    params = {
        "type": type,
        "sort": sort,
        "direction": direction,
        "per_page": per_page,
        "page": page,
    }

    response = await req(
        fn=get,
        url=f"/orgs/{organization}/repos",
        params=params,
        headers={"accept": "application/vnd.github+json"},
    )

    return (response.status_code, cast(list[Repository], response.json()))


async def get_repo_languages(
    username: str, repository: str
) -> tuple[int, dict[str, int]]:
    """
    Asynchronously retrieves the programming languages used in a specific repository.
    Args:
        username (str): The GitHub username of the repository owner.
        repository (str): The name of the repository.

    Returns:
        tuple[int, dict[str, int]]: A tuple containing the HTTP status code and a dictionary mapping language names to their respective byte counts.
    """
    response = await req(
        fn=get,
        url=f"/repos/{username}/{repository}/languages",
    )

    return (response.status_code, cast(dict[str, int], response.json()))


async def get_repos_authenticated(
    visibility: RepoVisibility = "all",
    per_page: int = 30,
    affiliation: Sequence[Literal["owner", "collaborator", "organization_member"]] = (
        "owner",
        "collaborator",
        "organization_member",
    ),
    type: RepositoryType | None = None,
    sort: RepoSortCriterion = "full_name",
    direction: RepoSortDirection = "asc",
    page: int = 1,
    since: str = None,
    before: str = None,
) -> tuple[int, list[Repository]]:
    """
    Asynchronously retrieves repositories for the authenticated user from the GitHub API.

    Reference: https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repositories-for-a-user

    Args:
        visibility (str): Limit results to repositories with the specified visibility. Default: 'all'
        affiliation (Sequence[str]): Limit results to repositories the specified user is affiliated with. Default: ('owner', 'collaborator', 'organization_member')
        type (str | None): Limit results to repositories of the specified type. Will cause a 422 error if used in the same request as visibility or affiliation.
        sort (str): The field to sort repositories by. Default: 'full_name'
        direction (str): The direction to sort repositories. Default: 'asc' when using 'full_name', otherwise 'desc'
        per_page (int): The number of results per page. Default: 30. for more info see: https://docs.github.com/rest/using-the-rest-api/using-pagination-in-the-rest-api
        page (int): The page number to retrieve. Default: 1
        Only show repositories updated after the given time. This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
        since (str): Only show repositories updated after the given time. This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
        before (str): Only show repositories updated before the given time. This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ

    Returns:
        tuple[int, list[Repository]]: A tuple containing the HTTP status code and a list of repositories for the authenticated user.
    """
    params = {
        "per_page": per_page,
        "sort": sort,
        "direction": direction,
        "page": page,
        "since": since,
        "before": before,
    }

    (
        params.update(
            {
                "visibility": visibility,
                "affiliation": ",".join(affiliation),
            }
        )
        if type is None
        else params.update(
            {
                "type": type,
            }
        )
    )

    res = await req(
        fn=get,
        url="/user/repos",
        params=params,
    )

    return (res.status_code, cast(list[Repository], res.json()))


async def get_repos_authenticated_extended(
    visibility: RepoVisibility = "all",
    per_page: int = 30,
    affiliation: Sequence[Literal["owner", "collaborator", "organization_member"]] = (
        "owner",
        "collaborator",
        "organization_member",
    ),
    type: Literal["all", "owner", "public", "private", "member"] | None = None,
    sort: Literal["created", "updated", "pushed", "full_name"] = "full_name",
    direction: Literal["asc", "desc"] = "asc",
    page: int = 1,
    since: str = None,
    before: str = None,
) -> RepoSlice:
    """
    Asynchronously retrieves repositories for the authenticated user from the GitHub API.
    Unlike ``get_repos_authenticated``, this function retrieves a RepoSlice instead of a list
    of repositories. This means that the ``Repository`` objects are encapsulated by the `RepoSlice`,
    which holds metadata on them. Each `Repository` also includes the `languages` field after fetching
    the languages of each repo.

    Reference: https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repositories-for-a-user

    Args:
        visibility (str): Limit results to repositories with the specified visibility. Default: 'all'
        affiliation (Sequence[str]): Limit results to repositories the specified user is affiliated with. Default: ('owner', 'collaborator', 'organization_member')
        type (str | None): Limit results to repositories of the specified type. Will cause a 422 error if used in the same request as visibility or affiliation.
        sort (str): The field to sort repositories by. Default: 'full_name'
        direction (str): The direction to sort repositories. Default: 'asc' when using 'full_name', otherwise 'desc'
        per_page (int): The number of results per page. Default: 30. for more info see: https://docs.github.com/rest/using-the-rest-api/using-pagination-in-the-rest-api
        page (int): The page number to retrieve. Default: 1
        Only show repositories updated after the given time. This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
        since (str): Only show repositories updated after the given time. This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
        before (str): Only show repositories updated before the given time. This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ

    Returns:
        RepoSlice: A RepoSlice object containing the count of repositories, a list of Repository objects, and any errors encountered during the request.
    """

    outputSlice: RepoSlice = RepoSlice(count=0, repos=[], errors=[])

    reporesponse = await get_repos_authenticated(
        visibility=visibility,
        per_page=per_page,
        affiliation=affiliation,
        type=type,
        sort=sort,
        direction=direction,
        page=page,
        since=since,
        before=before,
    )

    if reporesponse[0] != 200:
        LOGGER.error(
            f"Failed to retrieve repositories with::{reporesponse[0]}::{reporesponse[1]}"
        )
        outputSlice["errors"].append(
            ErrorMessage(
                message=f"Failed to retrieve repositories with::{reporesponse[0]}::{reporesponse[1]}",
                code=reporesponse[0],
                endpoint="/user/repos",
            )
        )

        gotlist: bool = isinstance(reporesponse[1], list)
        outputSlice["count"] = len(reporesponse[1]) if gotlist else 0
        outputSlice["updated"] = int(time())
        outputSlice["repos"] = reporesponse[1] if gotlist else []
        return outputSlice

    languagecoroutines: list[CoroutineType[Any, Any, tuple[int, dict[str, int]]]] = [
        get_repo_languages(username=repo["owner"]["login"], repository=repo["name"])
        for repo in reporesponse[1]
    ]

    language_results = await asyncio.gather(*languagecoroutines)
    languages = [list(langs.keys()) for _, langs in language_results]
    for index, langlist in enumerate(languages):
        reporesponse[1][index]["languages"] = langlist if langlist else None

    outputSlice["count"] = len(reporesponse[1])
    outputSlice["updated"] = int(time())
    outputSlice["repos"] = reporesponse[1]
    outputSlice["errors"] = None
    LOGGER.info(
        f"get_repos_authenticated_extended:::Retrieved {outputSlice['count']} repositories for authenticated user."
    )
    return outputSlice
