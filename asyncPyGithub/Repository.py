from requests import get
from time import time
import asyncio
from types import CoroutineType
from typing import cast, Any, Literal, Sequence
from typing_extensions import Self
from asyncPyGithub.base import req, LOGGER
from ._types import (
    ErrorMessage,
    RepositoryType,
    RepoSortDirection,
    RepoSortCriterion,
    RepoVisibility,
    MinimalRepositoryJSON,
    MinimalRepository,
    GitHubPortal,
    needs_authentication,
)


class GitHubRepositoryPortal(GitHubPortal):
    """
    A class to interact with GitHub repositories.
    This class provides methods to list repositories for a user or organization.
    """

    @needs_authentication
    async def get_organization_repos(
        cls: Self,
        organization: str,
        type: RepositoryType = "all",
        sort: RepoSortCriterion = "full_name",
        direction: RepoSortDirection = "asc",
        per_page: int = 30,
        page: int = 1,
    ) -> tuple[int, list[MinimalRepository] | ErrorMessage]:
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

        try:
            res = await req(
                fn=get,
                url=f"/orgs/{organization}/repos",
                params=params,
                headers={"accept": "application/vnd.github+json"},
            )

            if res.status_code != 200:
                return (
                    res.status_code,
                    ErrorMessage(
                        code=res.status_code,
                        message=res.json().get("message", "Unknown error"),
                        endpoint=f"/orgs/{organization}/repos",
                    ),
                )

        except Exception as e:
            return (
                500,
                ErrorMessage(
                    code=500,
                    message=str(e),
                    endpoint=f"/orgs/{organization}/repos",
                ),
            )
        return (res.status_code, [MinimalRepository(**repo) for repo in res.json()])


