from pydantic import BaseModel, HttpUrl
from typing import (
    TypedDict,
    NotRequired,
    Literal,
    List,
    Optional,
    Any,
    Dict,
)

from datetime import datetime

from .users import SimpleUserJSON, SimpleUser


RepositoryType = Literal[
    "all", "public", "private", "forks", "sources", "member", "owner"
]
"""
The different types of repositories that can be queried from GitHub.
usually defaults to 'all'.
The exact subset of types available depends on the context of the query,
such as whether it's for a user or an organization.
Refer to the [`documentation`](https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-organization-repositories)
"""


RepoSortCriterion = Literal["created", "updated", "pushed", "full_name"]
"""
The criteria by which repositories can be sorted when querying GitHub.
Usually defaults to 'full_name'.
"""


RepoSortDirection = Literal["asc", "desc"]
"""
The direction in which repositories can be sorted when querying GitHub.
Usually defaults to 'asc'.
"""


RepoVisibility = Literal["public", "private", "all"]
"""
The visibility of repositories when querying GitHub.
Usually defaults to 'all'.
"""


# TypedDict definitions
class NullDict(TypedDict):
    type: Literal["null"]


class CommitJSON(TypedDict):
    sha: str
    url: HttpUrl


class TagJSON(TypedDict):
    name: str
    commit: CommitJSON
    zipball_url: HttpUrl
    tarball_url: HttpUrl
    node_id: str


class TopicsJSON(TypedDict):
    names: List[str]


class PermissionsJSON(TypedDict):
    admin: bool
    maintain: bool
    push: bool
    triage: bool
    pull: bool


class CodeOfConductJSON(TypedDict):
    key: str
    name: str
    url: str
    body: str
    html_url: Optional[str]


class LicenseJSON(TypedDict):
    key: str
    name: str
    spdx_id: str
    url: str
    node_id: str


class SecurityStatusJSON(TypedDict):
    status: Literal["enabled", "disabled"]


class SecurityAndAnalysisJSON(TypedDict, total=False):
    advanced_security: SecurityStatusJSON
    code_security: SecurityStatusJSON
    dependabot_security_updates: SecurityStatusJSON
    secret_scanning: SecurityStatusJSON
    secret_scanning_push_protection: SecurityStatusJSON
    secret_scanning_non_provider_patterns: SecurityStatusJSON
    secret_scanning_ai_detection: SecurityStatusJSON


class MinimalRepositoryJSON(TypedDict):
    # Required fields
    id: int
    node_id: str
    name: str
    full_name: str
    owner: SimpleUserJSON
    private: bool
    html_url: HttpUrl
    description: Optional[str]
    fork: bool
    url: HttpUrl
    archive_url: str
    assignees_url: str
    blobs_url: str
    branches_url: str
    collaborators_url: str
    comments_url: str
    commits_url: HttpUrl
    compare_url: HttpUrl
    contents_url: HttpUrl
    contributors_url: HttpUrl
    deployments_url: HttpUrl
    downloads_url: HttpUrl
    events_url: str
    forks_url: str
    git_commits_url: str
    git_refs_url: str
    git_tags_url: str
    hooks_url: str
    issue_comment_url: str
    issue_events_url: str
    issues_url: str
    keys_url: str
    labels_url: str
    languages_url: str
    merges_url: str
    milestones_url: str
    notifications_url: str
    pulls_url: str
    releases_url: str
    stargazers_url: str
    statuses_url: str
    subscribers_url: str
    subscription_url: str
    tags_url: str
    teams_url: str
    trees_url: str

    # Optional fields
    git_url: NotRequired[str]
    ssh_url: NotRequired[str]
    clone_url: NotRequired[str]
    mirror_url: NotRequired[Optional[str]]
    svn_url: NotRequired[str]
    homepage: NotRequired[Optional[str]]
    language: NotRequired[Optional[str]]
    forks_count: NotRequired[int]
    stargazers_count: NotRequired[int]
    watchers_count: NotRequired[int]
    size: NotRequired[int]
    default_branch: NotRequired[str]
    open_issues_count: NotRequired[int]
    is_template: NotRequired[bool]
    topics: NotRequired[List[str]]
    has_issues: NotRequired[bool]
    has_projects: NotRequired[bool]
    has_wiki: NotRequired[bool]
    has_pages: NotRequired[bool]
    has_downloads: NotRequired[bool]
    has_discussions: NotRequired[bool]
    archived: NotRequired[bool]
    disabled: NotRequired[bool]
    visibility: NotRequired[str]
    pushed_at: NotRequired[Optional[str]]
    created_at: NotRequired[Optional[str]]
    updated_at: NotRequired[Optional[str]]
    permissions: NotRequired[PermissionsJSON]
    role_name: NotRequired[str]
    temp_clone_token: NotRequired[str]
    delete_branch_on_merge: NotRequired[bool]
    subscribers_count: NotRequired[int]
    network_count: NotRequired[int]
    code_of_conduct: NotRequired[CodeOfConductJSON]
    license: NotRequired[Optional[LicenseJSON]]
    forks: NotRequired[int]
    open_issues: NotRequired[int]
    watchers: NotRequired[int]
    allow_forking: NotRequired[bool]
    web_commit_signoff_required: NotRequired[bool]
    security_and_analysis: NotRequired[Optional[SecurityAndAnalysisJSON]]
    custom_properties: NotRequired[Dict[str, Any]]


class FullRepositoryJSON(TypedDict, total=False):
    id: int
    node_id: str
    name: str
    full_name: str
    owner: SimpleUserJSON
    private: bool
    html_url: HttpUrl
    description: Optional[str]
    fork: bool
    url: HttpUrl
    archive_url: str
    assignees_url: str
    blobs_url: str
    branches_url: str
    collaborators_url: str
    comments_url: str
    commits_url: HttpUrl
    compare_url: HttpUrl
    contents_url: HttpUrl
    contributors_url: HttpUrl
    deployments_url: HttpUrl
    downloads_url: HttpUrl
    events_url: HttpUrl
    forks_url: HttpUrl
    git_commits_url: HttpUrl
    git_refs_url: HttpUrl
    git_tags_url: HttpUrl
    hooks_url: HttpUrl
    issue_comment_url: HttpUrl
    issue_events_url: HttpUrl
    issues_url: HttpUrl
    keys_url: HttpUrl
    labels_url: HttpUrl
    languages_url: HttpUrl
    merges_url: HttpUrl
    milestones_url: HttpUrl
    notifications_url: HttpUrl
    pulls_url: HttpUrl
    releases_url: HttpUrl
    ssh_url: HttpUrl
    stargazers_url: HttpUrl
    statuses_url: HttpUrl
    subscribers_url: HttpUrl
    subscription_url: HttpUrl
    tags_url: HttpUrl
    teams_url: HttpUrl
    trees_url: HttpUrl
    clone_url: HttpUrl
    mirror_url: Optional[HttpUrl]
    svn_url: HttpUrl
    homepage: Optional[str]
    language: Optional[str]
    forks_count: int
    stargazers_count: int
    watchers_count: int
    size: int
    default_branch: str
    open_issues_count: int
    is_template: bool
    topics: List[str]
    has_issues: bool
    has_projects: bool
    has_wiki: bool
    has_pages: bool
    has_downloads: bool
    has_discussions: bool
    archived: bool
    disabled: bool
    visibility: Literal["public", "private", "internal"]
    pushed_at: str
    created_at: str
    updated_at: str
    permissions: PermissionsJSON
    allow_rebase_merge: bool
    template_repository: Optional[MinimalRepositoryJSON]
    temp_clone_token: Optional[str]
    allow_squash_merge: bool
    allow_auto_merge: bool
    delete_branch_on_merge: bool
    allow_merge_commit: bool
    use_squash_pr_title_as_default: bool
    squash_merge_commit_title: Literal["PR_TITLE", "COMMIT_OR_PR_TITLE"]
    squash_merge_commit_message: Literal["PR_BODY", "COMMIT_MESSAGES", "BLANK"]
    merge_commit_title: Literal["PR_TITLE", "MERGE_MESSAGE"]
    merge_commit_message: Literal["PR_BODY", "PR_TITLE", "BLANK"]
    allow_forking: bool
    web_commit_signoff_required: bool
    subscribers_count: int
    network_count: int
    license: Optional[LicenseJSON]
    organization: Optional[SimpleUserJSON]
    parent: Optional[MinimalRepositoryJSON]
    source: Optional[MinimalRepositoryJSON]
    forks: int
    master_branch: str
    open_issues: int
    watchers: int
    anonymous_access_enabled: bool
    code_of_conduct: Optional[CodeOfConductJSON]
    security_and_analysis: Optional[SecurityAndAnalysisJSON]
    custom_properties: Optional[Dict[str, Any]]


# Pydantic models
class Permissions(BaseModel):
    admin: bool
    maintain: bool
    push: bool
    triage: bool
    pull: bool


class CodeOfConduct(BaseModel):
    key: str
    name: str
    url: HttpUrl
    body: str
    html_url: Optional[HttpUrl] = None


class License(BaseModel):
    key: str
    name: str
    spdx_id: str
    node_id: str
    url: Optional[HttpUrl] = None


class SecurityStatus(BaseModel):
    status: Literal["enabled", "disabled"]


class SecurityAndAnalysis(BaseModel):
    advanced_security: Optional[SecurityStatus] = None
    code_security: Optional[SecurityStatus] = None
    dependabot_security_updates: Optional[SecurityStatus] = None
    secret_scanning: Optional[SecurityStatus] = None
    secret_scanning_push_protection: Optional[SecurityStatus] = None
    secret_scanning_non_provider_patterns: Optional[SecurityStatus] = None
    secret_scanning_ai_detection: Optional[SecurityStatus] = None


class MinimalRepository(BaseModel):
    id: int
    node_id: str
    name: str
    full_name: str
    owner: SimpleUser
    private: bool
    html_url: HttpUrl
    description: Optional[str]
    fork: bool
    url: HttpUrl
    archive_url: str
    assignees_url: str
    blobs_url: str
    branches_url: str
    collaborators_url: str
    comments_url: str
    commits_url: str
    compare_url: str
    contents_url: str
    contributors_url: HttpUrl
    deployments_url: HttpUrl
    downloads_url: HttpUrl
    events_url: HttpUrl
    forks_url: HttpUrl
    git_commits_url: str
    git_refs_url: str
    git_tags_url: str
    hooks_url: HttpUrl
    issue_comment_url: str
    issue_events_url: str
    issues_url: str
    keys_url: str
    labels_url: str
    languages_url: HttpUrl
    merges_url: HttpUrl
    milestones_url: str
    notifications_url: str
    pulls_url: str
    releases_url: str
    stargazers_url: HttpUrl
    statuses_url: str
    subscribers_url: HttpUrl
    subscription_url: HttpUrl
    tags_url: HttpUrl
    teams_url: HttpUrl
    trees_url: str

    # Optional fields
    git_url: Optional[str] = None
    ssh_url: Optional[str] = None
    clone_url: Optional[str] = None
    mirror_url: Optional[str] = None
    svn_url: Optional[str] = None
    homepage: Optional[str] = None
    language: Optional[str] = None
    forks_count: Optional[int] = None
    stargazers_count: Optional[int] = None
    watchers_count: Optional[int] = None
    size: Optional[int] = None
    default_branch: Optional[str] = None
    open_issues_count: Optional[int] = None
    is_template: Optional[bool] = None
    topics: Optional[List[str]] = None
    has_issues: Optional[bool] = None
    has_projects: Optional[bool] = None
    has_wiki: Optional[bool] = None
    has_pages: Optional[bool] = None
    has_downloads: Optional[bool] = None
    has_discussions: Optional[bool] = None
    archived: Optional[bool] = None
    disabled: Optional[bool] = None
    visibility: Optional[str] = None
    pushed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    permissions: Optional[Permissions] = None
    role_name: Optional[str] = None
    temp_clone_token: Optional[str] = None
    delete_branch_on_merge: Optional[bool] = None
    subscribers_count: Optional[int] = None
    network_count: Optional[int] = None
    code_of_conduct: Optional[CodeOfConduct] = None
    license: Optional[License] = None
    forks: Optional[int] = None
    open_issues: Optional[int] = None
    watchers: Optional[int] = None
    allow_forking: Optional[bool] = None
    web_commit_signoff_required: Optional[bool] = None
    security_and_analysis: Optional[SecurityAndAnalysis] = None
    custom_properties: Optional[Dict[str, Any]] = None


class FullRepository(BaseModel):
    id: int
    node_id: str
    name: str
    full_name: str
    owner: SimpleUser
    private: bool
    html_url: HttpUrl
    description: Optional[str] = None
    fork: bool
    url: HttpUrl
    archive_url: str
    assignees_url: str
    blobs_url: str
    branches_url: str
    collaborators_url: str
    comments_url: str
    commits_url: HttpUrl
    compare_url: HttpUrl
    contents_url: HttpUrl
    contributors_url: HttpUrl
    deployments_url: HttpUrl
    downloads_url: HttpUrl
    events_url: HttpUrl
    forks_url: HttpUrl
    git_commits_url: str
    git_refs_url: str
    git_tags_url: str
    hooks_url: HttpUrl
    issue_comment_url: str
    issue_events_url: str
    issues_url: HttpUrl
    keys_url: HttpUrl
    labels_url: HttpUrl
    languages_url: HttpUrl
    merges_url: HttpUrl
    milestones_url: HttpUrl
    notifications_url: HttpUrl
    pulls_url: HttpUrl
    releases_url: HttpUrl
    ssh_url: Optional[HttpUrl] = None
    stargazers_url: Optional[HttpUrl] = None
    subscribers_url: Optional[HttpUrl] = None
    subscription_url: Optional[HttpUrl] = None
    tags_url: Optional[HttpUrl] = None
    teams_url: Optional[HttpUrl] = None
    trees_url: str
    clone_url: Optional[HttpUrl] = None
    mirror_url: Optional[HttpUrl] = None
    svn_url: Optional[HttpUrl] = None
    homepage: Optional[str] = None
    language: Optional[str] = None
    forks_count: int = 0
    stargazers_count: int = 0
    watchers_count: int = 0
    size: int = 0
    default_branch: str = "main"
    open_issues_count: int = 0
    is_template: bool = False
    topics: List[str] = []
    has_issues: bool = True
    has_projects: bool = True
    has_wiki: bool = True
    has_pages: bool = False
    has_downloads: bool = True
    has_discussions: bool = False
    archived: bool = False
    disabled: bool = False
    visibility: Literal["public", "private", "internal"] = "public"
    pushed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    permissions: Optional[Permissions] = None
    role_name: Optional[str] = None
    temp_clone_token: Optional[str] = None
    delete_branch_on_merge: Optional[bool] = None
    allow_rebase_merge: bool = True
    allow_squash_merge: bool = True
    allow_auto_merge: bool = False
    allow_merge_commit: bool = True
    use_squash_pr_title_as_default: bool = False
    squash_merge_commit_title: Literal["PR_TITLE", "COMMIT_OR_PR_TITLE"] = "PR_TITLE"
    squash_merge_commit_message: Literal["PR_BODY", "COMMIT_MESSAGES", "BLANK"] = (
        "PR_BODY"
    )
    merge_commit_title: Literal["PR_TITLE", "MERGE_MESSAGE"] = "PR_TITLE"
    merge_commit_message: Literal["PR_BODY", "PR_TITLE", "BLANK"] = "PR_TITLE"
    allow_forking: bool = True
    web_commit_signoff_required: bool = False
    subscribers_count: int = 0
    network_count: int = 0
    license: Optional[License] = None
    organization: Optional[SimpleUser] = None
    parent: Optional[MinimalRepository] = None
    source: Optional[MinimalRepository] = None
    forks: int = 0
    master_branch: str = "main"
    open_issues: int = 0
    watchers: int = 0
    anonymous_access_enabled: bool = False
    code_of_conduct: Optional[CodeOfConduct] = None
    security_and_analysis: Optional[SecurityAndAnalysis] = None
    custom_properties: Optional[Dict[str, Any]] = None


class Commit(BaseModel):
    sha: str
    url: HttpUrl


class Tag(BaseModel):
    name: str
    commit: Commit
    zipball_url: HttpUrl
    tarball_url: HttpUrl
    node_id: str


class Topics(BaseModel):
    names: List[str]
