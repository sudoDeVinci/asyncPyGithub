from typing import cast, no_type_check
from asyncPyGithub import (
    API_ENDPOINT,
    GitHubRepositoryPortal,
    read_json,
    ErrorMessage,
    MinimalRepository,
)


from pytest import mark
from responses import RequestsMock, GET
from pathlib import Path

JSONDIR = Path(__file__).parent.resolve() / "traffic"


@no_type_check
@mark.asyncio
async def test_get_organization_repos_successful(mock_requests: RequestsMock) -> None:
    mock_repos = read_json(JSONDIR / "org_repos.json")
    mock_requests.add(
        GET,
        url=f"{API_ENDPOINT}/orgs/LEGO/repos",
        json=mock_repos,
        status=200,
    )

    response: tuple[int, list[MinimalRepository] | ErrorMessage] = (
        await GitHubRepositoryPortal.get_organization_repos(
            organization="LEGO",
            type="all",
            sort="full_name",
            direction="asc",
            per_page=5,
            page=1,
        )
    )
    status, repos = response
    assert status == 200, f">> Could not fetch organization repositories::{repos}"
    assert isinstance(repos, list), "Expected a list of MinimalRepository instances."
    for repo in repos:
        assert isinstance(
            repo, MinimalRepository
        ), "Expected a MinimalRepository instance."
        repo = cast(MinimalRepository, repo)
