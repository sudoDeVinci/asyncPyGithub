from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    EmailStr
)

from typing import (
    TypedDict,
    NotRequired,
    Literal,
)

from .users import UserJSON
from .base import ErrorMessage


RepositoryType = Literal[
    'all',
    'public',
    'private',
    'forks',
    'sources',
    'member',
    'owner'
]
"""
The different types of repositories that can be queried from GitHub.
usually defaults to 'all'.
The exact subset of types available depends on the context of the query,
such as whether it's for a user or an organization.
Refer to the [`documentation`](https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-organization-repositories)
"""


RepoSortCriterion = Literal[
    'created',
    'updated',
    'pushed',
    'full_name'
]
"""
The criteria by which repositories can be sorted when querying GitHub.
Usually defaults to 'full_name'.
"""


RepoSortDirection = Literal[
    'asc',
    'desc'
]
"""
The direction in which repositories can be sorted when querying GitHub.
Usually defaults to 'asc'.
"""


RepoVisibility = Literal[
    'public',
    'private',
    'all'
]
"""
The visibility of repositories when querying GitHub.
Usually defaults to 'all'.
"""


class Repository(TypedDict, total=False):
    """
    A GitHub repository with essential details.

    Attributes:
        id (int): The unique identifier for the repository.
        node_id (str): The node ID of the repository.
        name (str): The name of the repository.
        full_name (str): The full name of the repository, including the owner's username.
        private (bool): Whether the repository is private.
        owner (User): The owner of the repository, represented as a User object.
        html_url (str): The URL to the repository on GitHub.
        description (str | None): A brief description of the repository, if available.
        fork (bool): Whether the repository is a fork of another repository.
        url (str): The API URL for the repository.
        forks_url (str): The URL to fetch forks of this repository.
        keys_url (str): The URL to fetch keys associated with this repository.
        collaborators_url (str): The URL to fetch collaborators of this repository.
        teams_url (str): The URL to fetch teams associated with this repository.
        hooks_url (str): The URL to fetch webhooks for this repository.
        issue_events_url (str): The URL to fetch issue events for this repository.
        events_url (str): The URL to fetch public events for this repository.
        assignees_url (str): The URL to fetch assignees for issues in this repository.
        branches_url (str): The URL to fetch branches in this repository.
        tags_url (str): The URL to fetch tags in this repository.
        blobs_url (str): The URL to fetch blobs in this repository.
        git_tags_url (str): The URL to fetch git tags in this repository.
        git_refs_url (str): The URL to fetch git references in this repository.
        trees_url (str): The URL to fetch trees in this repository.
        statuses_url (str): The URL to fetch commit statuses in this repository.
        languages_url (str): The URL to fetch programming languages used in this repository.
        stargazers_url (str): The URL to fetch stargazers of this repository.
        contributors_url (str): The URL to fetch contributors of this repository.
        subscribers_url (str): The URL to fetch subscribers of this repository.
        subscription_url (str): The URL for managing subscriptions for this repository.
        commits_url (str): The URL to fetch commits in this repository.
        git_commits_url (str): The URL to fetch git commits in this repository.
        comments_url (str): The URL to fetch comments in this repository.
        issue_comment_url (str): The URL to fetch issue comments in this repository.
        contents_url (str): The URL to fetch contents of this repository.
        compare_url (str): The URL to compare commits in this repository.
        merges_url (str): The URL to fetch merge information for this repository.
        archive_url (str): The URL to fetch archived contents of this repository.
        downloads_url (str): The URL to fetch downloads associated with this repository.
        issues_url (str): The URL to fetch issues in this repository.
        pulls_url (str): The URL to fetch pull requests in this repository.
        milestones_url (str): The URL to fetch milestones in this repository.
        notifications_url (str): The URL to fetch notifications for this repository.
        labels_url (str): The URL to fetch labels in this repository.
        releases_url (str): The URL to fetch releases in this repository.
        deployments_url (str): The URL to fetch deployments for this repository.
        created_at (str): Timestamp when the repository was created.
        updated_at (str): Timestamp when the repository was last updated.
        pushed_at (str): Timestamp when the repository was last pushed to.
        git_url (str): The Git URL for the repository.
        ssh_url (str): The SSH URL for the repository.
        clone_url (str): The HTTPS URL for cloning the repository.
        svn_url (str): The SVN URL for the repository.
        homepage (str | None): The homepage URL for the repository, if available.
        size (int): The size of the repository in kilobytes.
        stargazers_count (int): The number of stars the repository has received.
        watchers_count (int): The number of watchers for the repository.
        language (str | None): The primary programming language of the repository, if available.
        has_issues (bool): Whether the repository has issues enabled.
        has_projects (bool): Whether the repository has projects enabled.
        has_downloads (bool): Whether the repository allows downloads.
        has_wiki (bool): Whether the repository has a wiki enabled.
        has_pages (bool): Whether the repository has GitHub Pages enabled.
        has_discussions (bool): Whether the repository has discussions enabled.
        forks_count (int): The number of forks of this repository.
        mirror_url (str | None): The mirror URL of the repository, if available.
        archived (bool): Whether the repository is archived.
        disabled (bool): Whether the repository is disabled.
        open_issues_count (int): The number of open issues in the repository.
        license (dict[str, str | None] | None): Information about the repository's license, if available.
        allow_forking (bool): Whether forking is allowed for this repository.
        is_template (bool): Whether the repository is a template.
        web_commit_signoff_required (bool): Whether web commit signoff is required for this repository.
        topics (list[str]): A list of topics associated with the repository.
        visibility (str): The visibility of the repository (e.g., "public", "private").
        forks (int): The number of forks of this repository.
        open_issues (int): The number of open issues in this repository.
        watchers (int): The number of watchers for this repository.
        default_branch (str): The default branch of the repository.
        permissions (dict[str, bool] | None): Permissions for the authenticated user on this repository.
    """
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    owner: UserJSON
    html_url: str
    description: str | None
    fork: bool
    url: str
    forks_url: str
    keys_url: str
    collaborators_url: str
    teams_url: str
    hooks_url: str
    issue_events_url: str
    events_url: str
    assignees_url: str
    branches_url: str
    tags_url: str
    blobs_url: str
    git_tags_url: str
    git_refs_url: str
    trees_url: str
    statuses_url: str
    languages_url: str
    stargazers_url: str
    contributors_url: str
    subscribers_url: str
    subscription_url: str
    commits_url: str
    git_commits_url: str
    comments_url: str
    issue_comment_url: str
    contents_url: str
    compare_url: str
    merges_url: str
    archive_url: str
    downloads_url: str
    issues_url: str
    pulls_url: str
    milestones_url: str
    notifications_url: str
    labels_url: str
    releases_url: str
    deployments_url: str
    created_at: str
    updated_at: str
    pushed_at: str
    git_url: str
    ssh_url: str
    clone_url: str
    svn_url: str
    homepage: str | None
    size: int
    stargazers_count: int
    watchers_count: int
    language: str | None
    languages: NotRequired[list[str]]
    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    has_discussions: bool
    forks_count: int
    mirror_url: str | None
    archived: bool
    disabled: bool
    open_issues_count: int
    license: dict[str, str | None] | None
    allow_forking: bool
    is_template: bool
    web_commit_signoff_required: bool
    topics: list[str]
    visibility: str
    forks: int
    open_issues: int
    watchers: int
    default_branch: str
    permissions: dict[str, bool] | None
    

class ContentFile(TypedDict, total=False):
    """
    Represents a file in a GitHub repository with essential details.

    Attributes:
        name (str): The name of the file.
        type (str): The type of the file (e.g., "file", "dir").
        size (int): The size of the file in bytes.
        encoding (str): The encoding of the file content.
        content (str): The base64 encoded content of the file.
        sha (str): The SHA hash of the file.
        url (str): The API URL to access the file.
        html_url (str): The HTML URL to view the file on GitHub.
        git_url (str): The Git URL for the file.
        download_url (str | None): The URL to download the file, if available.
        _links (dict[str, str]): Links related to the file, such as self, git, and html URLs.
    """
    name: str
    type: str
    size: int
    encoding: str
    content: str
    sha: str
    url: str
    html_url: str
    git_url: str
    download_url: str | None
    _links: dict[str, str]


class RepoSlice(TypedDict, total=False):
    """
    Represents a slice of GitHub repositories with metadata.
    
    Attributes:
        count (int): The total number of repositories in this slice.
        updated (int): The timestamp when this slice was last updated.
        repos (list[RepoGist | Repository]): A list of repositories.
        errors (list[ErrorMessage] | None): A list of error messages, if any.
    """
    count: int
    updated: int
    repos: list[Repository]
    errors: list[ErrorMessage] | None
