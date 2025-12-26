from pathlib import Path
from typing import cast, no_type_check

import respx
from httpx import Response
from pytest import mark

from asyncPyGithub import (
    ErrorMessage,
    GitHubPortal,
    GitHubRepositoryPortal,
    MinimalRepository,
    read_json,
)

JSONDIR = Path(__file__).parent.resolve() / "traffic"
USER_ENDPOINT = "/user"


@no_type_check
@mark.asyncio
async def test_get_organization_repos_successful(
    mock_requests: respx.MockRouter,
) -> None:
    # First authenticate
    mock_auth = read_json(JSONDIR / "authenticate.json")
    mock_requests.get(USER_ENDPOINT).mock(return_value=Response(200, json=mock_auth))
    await GitHubPortal.authenticate("mock_token")

    mock_repos = read_json(JSONDIR / "org_repos.json")
    mock_requests.get("/orgs/LEGO/repos").mock(
        return_value=Response(200, json=mock_repos)
    )

    response: tuple[
        int, list[MinimalRepository] | ErrorMessage
    ] = await GitHubRepositoryPortal.get_organization_repos(
        organization="LEGO",
        type="all",
        sort="full_name",
        direction="asc",
        per_page=5,
        page=1,
    )
    status, repos = response
    assert status == 200, f">> Could not fetch organization repositories::{repos}"
    assert isinstance(repos, list), "Expected a list of MinimalRepository instances."
    for repo in repos:
        assert isinstance(repo, MinimalRepository), (
            "Expected a MinimalRepository instance."
        )
        repo = cast(MinimalRepository, repo)
