from typing import Literal, Optional

from typing_extensions import Self

from ._types import (
    Contributor,
    ErrorMessage,
    FullRepository,
    GitHubPortal,
    MinimalRepository,
    RepositoryType,
    RepoSortCriterion,
    RepoSortDirection,
    Tag,
    Topics,
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
            res = await cls.req(
                "GET",
                f"/orgs/{organization}/repos",
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

    @needs_authentication
    async def create_organization_repo(
        cls: Self,
        organization: str,
        name: str,
        description: str = "",
        homepage: str = "",
        private: bool = False,
        visibility: Literal["public", "private"] = "public",
        has_issues: bool = True,
        has_projects: bool = True,
        has_wiki: bool = True,
        has_downloads: bool = True,
        is_template: bool = False,
        team_id: int | None = None,
        auto_init: bool = False,
        gitignore_template: Optional[str] = None,
        license_template: Optional[str] = None,
        allow_squash_merge: bool = True,
        allow_merge_commit: bool = True,
        allow_rebase_merge: bool = True,
        allow_auto_merge: bool = False,
        delete_branch_on_merge: bool = False,
        use_squash_pr_title_as_default: bool = False,
        squash_merge_commit_title: Literal[
            "PR_TITLE", "COMMIT_OR_PR_TITLE"
        ] = "PR_TITLE",
        squash_merge_commit_message: Literal[
            "PR_BODY", "COMMIT_MESSAGES", "BLANK"
        ] = "PR_BODY",
        merge_commit_title: Literal["PR_TITLE", "MERGE_MESSAGE"] = "PR_TITLE",
        merge_commit_message: Literal["PR_BODY", "PR_TITLE", "BLANK"] = "PR_TITLE",
        custom_properties: dict[str, str | bool | int] | None = None,
    ) -> tuple[int, FullRepository | ErrorMessage]:
        params = {
            "name": name,
            "description": description,
            "homepage": homepage,
            "private": private,
            "visibility": visibility,
            "has_issues": has_issues,
            "has_projects": has_projects,
            "has_wiki": has_wiki,
            "has_downloads": has_downloads,
            "is_template": is_template,
            "team_id": team_id,
            "auto_init": auto_init,
            "gitignore_template": gitignore_template,
            "license_template": license_template,
            "allow_squash_merge": allow_squash_merge,
            "allow_merge_commit": allow_merge_commit,
            "allow_rebase_merge": allow_rebase_merge,
            "allow_auto_merge": allow_auto_merge,
            "delete_branch_on_merge": delete_branch_on_merge,
            "use_squash_pr_title_as_default": use_squash_pr_title_as_default,
            "squash_merge_commit_title": squash_merge_commit_title,
            "squash_merge_commit_message": squash_merge_commit_message,
            "merge_commit_title": merge_commit_title,
            "merge_commit_message": merge_commit_message,
        }

        if custom_properties:
            params.update(custom_properties)

        try:
            res = await cls.req(
                "POST",
                f"/orgs/{organization}/repos",
                params=params,
                headers={"accept": "application/vnd.github+json"},
            )

            if res.status_code != 201:
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

        return (res.status_code, FullRepository(**res.json()))

    @needs_authentication
    async def get_user_repo(
        cls: Self,
        owner: str,
        repo: str,
    ) -> tuple[int, FullRepository | ErrorMessage]:
        """
        Lists repositories for the authenticated user.
        This endpoint can be used without authentication, or
        with read access to public repositories.
        """
        try:
            res = await cls.req(
                "GET",
                f"repos/{owner}/{repo}",
                headers={"accept": "application/vnd.github+json"},
            )

            if res.status_code != 200:
                return (
                    res.status_code,
                    ErrorMessage(
                        code=res.status_code,
                        message=res.json().get("message", "Unknown error"),
                        endpoint="repos/{owner}/{repo}",
                    ),
                )

        except Exception as e:
            return (
                500,
                ErrorMessage(
                    code=500,
                    message=str(e),
                    endpoint="/user/repos",
                ),
            )

        return (res.status_code, FullRepository(**res.json()))

    @needs_authentication
    async def update_repository(
        cls: Self,
        owner: str,
        repo: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        homepage: Optional[str] = None,
        private: Optional[bool] = None,
        visibility: Optional[Literal["public", "private"]] = None,
        has_issues: Optional[bool] = None,
        has_projects: Optional[bool] = None,
        has_wiki: Optional[bool] = None,
        is_template: Optional[bool] = None,
        default_branch: Optional[str] = None,
        allow_squash_merge: Optional[bool] = None,
        allow_merge_commit: Optional[bool] = None,
        allow_rebase_merge: Optional[bool] = None,
        allow_auto_merge: Optional[bool] = None,
        delete_branch_on_merge: Optional[bool] = None,
        use_squash_pr_title_as_default: Optional[bool] = None,
        squash_merge_commit_title: Optional[
            Literal["PR_TITLE", "COMMIT_OR_PR_TITLE"]
        ] = None,
        squash_merge_commit_message: Optional[
            Literal["PR_BODY", "COMMIT_MESSAGES", "BLANK"]
        ] = None,
        merge_commit_title: Optional[Literal["PR_TITLE", "MERGE_MESSAGE"]] = None,
        merge_commit_message: Optional[Literal["PR_BODY", "PR_TITLE", "BLANK"]] = None,
        archived: Optional[bool] = None,
        allow_forking: Optional[bool] = None,
        web_commit_signoff_required: Optional[bool] = None,
    ) -> tuple[int, FullRepository | ErrorMessage]:
        """
        Updates a repository.
        This endpoint can be used with write access to the repository.
        """

        params = {
            "name": name,
            "description": description,
            "homepage": homepage,
            "private": private,
            "visibility": visibility,
            "has_issues": has_issues,
            "has_projects": has_projects,
            "has_wiki": has_wiki,
            "is_template": is_template,
            "default_branch": default_branch,
            "allow_squash_merge": allow_squash_merge,
            "allow_merge_commit": allow_merge_commit,
            "allow_rebase_merge": allow_rebase_merge,
            "allow_auto_merge": allow_auto_merge,
            "delete_branch_on_merge": delete_branch_on_merge,
            "use_squash_pr_title_as_default": use_squash_pr_title_as_default,
            "squash_merge_commit_title": squash_merge_commit_title,
            "squash_merge_commit_message": squash_merge_commit_message,
            "merge_commit_title": merge_commit_title,
            "merge_commit_message": merge_commit_message,
            "archived": archived,
            "allow_forking": allow_forking,
            "web_commit_signoff_required": web_commit_signoff_required,
        }

        try:
            res = await cls.req(
                "PATCH",
                f"repos/{owner}/{repo}",
                params={k: v for k, v in params.items() if v is not None},
                headers={"accept": "application/vnd.github+json"},
            )

            if res.status_code != 200:
                return (
                    res.status_code,
                    ErrorMessage(
                        code=res.status_code,
                        message=res.json().get("message", "Unknown error"),
                        endpoint=f"repos/{owner}/{repo}",
                    ),
                )
        except Exception as e:
            return (
                500,
                ErrorMessage(
                    code=500,
                    message=str(e),
                    endpoint=f"repos/{owner}/{repo}",
                ),
            )

        return (res.status_code, FullRepository(**res.json()))

    @needs_authentication
    async def delete_repository(
        cls: Self, owner: str, repo: str
    ) -> tuple[int, Optional[ErrorMessage]]:
        """
        Deletes a repository.
        This endpoint can be used with write access to the repository.
        """
        try:
            res = await cls.req(
                "DELETE",
                f"repos/{owner}/{repo}",
                headers={"accept": "application/vnd.github+json"},
            )

            if res.status_code != 204:
                return (
                    res.status_code,
                    ErrorMessage(
                        code=res.status_code,
                        message=res.json().get("message", "Unknown error"),
                        endpoint=f"repos/{owner}/{repo}",
                    ),
                )
        except Exception as e:
            return (
                500,
                ErrorMessage(
                    code=500,
                    message=str(e),
                    endpoint=f"repos/{owner}/{repo}",
                ),
            )

        return (res.status_code, None)

    @needs_authentication
    async def list_contributors(
        cls: Self,
        owner: str,
        repo: str,
        anon: bool = False,
        per_page: int = 30,
        page: int = 1,
    ) -> tuple[int, list[Contributor] | ErrorMessage]:
        """
        Lists contributors to the specified repository and sorts them by the number of commits per contributor in descending order. This endpoint may return information that is a few hours old because the GitHub REST API caches contributor data to improve performance.
        """

        params = {"anon": anon, "per_page": per_page, "page": page}

        try:
            res = await cls.req(
                "GET",
                f"repos/{owner}/{repo}/contributors",
                params=params,
                headers={"accept": "application/vnd.github+json"},
            )

            if res.status_code != 200:
                return (
                    res.status_code,
                    ErrorMessage(
                        code=res.status_code,
                        message=res.json().get("message", "Unknown error"),
                        endpoint=f"repos/{owner}/{repo}/contributors",
                    ),
                )
        except Exception as e:
            return (
                500,
                ErrorMessage(
                    code=500,
                    message=str(e),
                    endpoint=f"repos/{owner}/{repo}/contributors",
                ),
            )
        return (
            res.status_code,
            [Contributor(**contributor) for contributor in res.json()],
        )

    @needs_authentication
    async def list_repository_languages(
        cls: Self, owner: str, repo: str
    ) -> tuple[int, dict[str, int] | ErrorMessage]:
        """
        Lists languages for the specified repository. The value shown for each language is the number of bytes of code written in that language.
        """

        try:
            res = await cls.req(
                "GET",
                f"repos/{owner}/{repo}/languages",
                headers={"accept": "application/vnd.github+json"},
            )

            if res.status_code != 200:
                return (
                    res.status_code,
                    ErrorMessage(
                        code=res.status_code,
                        message=res.json().get("message", "Unknown error"),
                        endpoint=f"repos/{owner}/{repo}/languages",
                    ),
                )
        except Exception as e:
            return (
                500,
                ErrorMessage(
                    code=500,
                    message=str(e),
                    endpoint=f"repos/{owner}/{repo}/languages",
                ),
            )
        return (res.status_code, res.json())

    @needs_authentication
    async def list_repository_tags(
        cls: Self, owner: str, repo: str, per_page: int = 30, page: int = 1
    ) -> tuple[int, list[Tag] | ErrorMessage]:
        """
        Lists tags for the specified repository.
        This endpoint can be used without authentication, or
        with read access to public repositories.
        """

        params = {"per_page": per_page, "page": page}

        try:
            res = await cls.req(
                "GET",
                f"repos/{owner}/{repo}/tags",
                params=params,
                headers={"accept": "application/vnd.github+json"},
            )

            if res.status_code != 200:
                return (
                    res.status_code,
                    ErrorMessage(
                        code=res.status_code,
                        message=res.json().get("message", "Unknown error"),
                        endpoint=f"repos/{owner}/{repo}/tags",
                    ),
                )
        except Exception as e:
            return (
                500,
                ErrorMessage(
                    code=500,
                    message=str(e),
                    endpoint=f"repos/{owner}/{repo}/tags",
                ),
            )

        return (res.status_code, [Tag(**tag) for tag in res.json()])

    @needs_authentication
    async def get_repository_topics(
        cls: Self, owner: str, repo: str
    ) -> tuple[int, Topics | ErrorMessage]:
        """
        Lists topics for the specified repository.
        This endpoint can be used without authentication, or
        with read access to public repositories.
        """

        try:
            res = await cls.req(
                "GET",
                f"repos/{owner}/{repo}/topics",
                headers={"accept": "application/vnd.github+json"},
            )

            if res.status_code != 200:
                return (
                    res.status_code,
                    ErrorMessage(
                        code=res.status_code,
                        message=res.json().get("message", "Unknown error"),
                        endpoint=f"repos/{owner}/{repo}/topics",
                    ),
                )
        except Exception as e:
            return (
                500,
                ErrorMessage(
                    code=500,
                    message=str(e),
                    endpoint=f"repos/{owner}/{repo}/topics",
                ),
            )

        return (res.status_code, Topics(**res.json()))
