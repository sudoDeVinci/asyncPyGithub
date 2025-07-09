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

from .users import (
    SimpleUserJSON,
    SimpleUser
)



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
    # Required fields
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


class FullRepositoryJSON(TypedDict, total=False):
    pass