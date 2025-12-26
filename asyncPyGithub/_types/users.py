from pydantic import BaseModel, EmailStr, HttpUrl, PastDatetime
from typing_extensions import Optional, TypedDict


class ContributorJSON(TypedDict):
    contributions: int
    type: str
    login: Optional[str]
    id: Optional[int]
    node_id: Optional[str]
    avatar_url: Optional[HttpUrl]
    gravatar_id: Optional[str]
    url: Optional[HttpUrl]
    html_url: Optional[HttpUrl]
    followers_url: Optional[HttpUrl]
    following_url: Optional[str]
    gists_url: Optional[str]
    starred_url: Optional[str]
    subscriptions_url: Optional[HttpUrl]
    organizations_url: Optional[HttpUrl]
    repos_url: Optional[HttpUrl]
    events_url: Optional[str]
    received_events_url: Optional[HttpUrl]
    site_admin: Optional[bool]
    email: Optional[EmailStr]
    name: Optional[str]
    user_view_type: Optional[str]


class UserPlanJSON(TypedDict):
    """
    A GitHub authenticated User's plan.
    """

    collaborators: int
    name: str
    space: int
    private_repos: int


class PrivateUserJSON(TypedDict, total=False):
    """
    A GitHub User.
    """

    # Required fields according to the Public User schema
    login: str
    id: int
    node_id: str
    avatar_url: HttpUrl  # has "format": "uri"
    gravatar_id: Optional[str]  # can be null but required
    url: HttpUrl  # has "format": "uri"
    html_url: HttpUrl  # has "format": "uri"
    followers_url: HttpUrl  # has "format": "uri"
    following_url: str  # no format specified (template URL)
    gists_url: str  # no format specified (template URL)
    starred_url: str  # no format specified (template URL)
    subscriptions_url: HttpUrl  # has "format": "uri"
    organizations_url: HttpUrl  # has "format": "uri"
    repos_url: HttpUrl  # has "format": "uri"
    events_url: str  # no format specified (template URL)
    received_events_url: HttpUrl  # has "format": "uri"
    type: str
    site_admin: bool
    name: Optional[str]  # can be null but required
    company: Optional[str]  # can be null but required
    blog: Optional[str]  # can be null but required
    location: Optional[str]  # can be null but required
    email: Optional[EmailStr]  # can be null but required
    hireable: Optional[bool]  # can be null but required
    bio: Optional[str]  # can be null but required
    public_repos: int
    public_gists: int
    followers: int
    following: int
    created_at: PastDatetime
    updated_at: PastDatetime

    # Optional fields (not in required array)
    user_view_type: Optional[str]
    notification_email: Optional[EmailStr]
    twitter_username: Optional[str]
    plan: Optional[UserPlanJSON]
    private_gists: Optional[int]
    total_private_repos: Optional[int]
    owned_private_repos: Optional[int]
    disk_usage: Optional[int]
    collaborators: Optional[int]
    two_factor_authentication: Optional[bool]
    business_plus: Optional[bool]
    ldap_dn: Optional[str]


class PrivateUser(BaseModel):
    """
    A GitHub User.
    """

    # Required fields according to the Public User schema
    login: str
    id: int
    node_id: str
    avatar_url: HttpUrl  # has "format": "uri"
    gravatar_id: Optional[str]  # can be null but required
    url: HttpUrl  # has "format": "uri"
    html_url: HttpUrl  # has "format": "uri"
    followers_url: HttpUrl  # has "format": "uri"
    following_url: str  # no format specified (template URL)
    gists_url: str  # no format specified (template URL)
    starred_url: str  # no format specified (template URL)
    subscriptions_url: HttpUrl  # has "format": "uri"
    organizations_url: HttpUrl  # has "format": "uri"
    repos_url: HttpUrl  # has "format": "uri"
    events_url: str  # no format specified (template URL)
    received_events_url: HttpUrl  # has "format": "uri"
    type: str
    site_admin: bool
    name: Optional[str]  # can be null but required
    company: Optional[str]  # can be null but required
    blog: Optional[str]  # can be null but required
    location: Optional[str]  # can be null but required
    email: Optional[EmailStr]  # can be null but required
    hireable: Optional[bool]  # can be null but required
    bio: Optional[str]  # can be null but required
    public_repos: int
    public_gists: int
    followers: int
    following: int
    created_at: PastDatetime
    updated_at: PastDatetime

    # Optional fields (not in required array)
    user_view_type: Optional[str] = None
    notification_email: Optional[EmailStr] = None
    twitter_username: Optional[str] = None
    plan: Optional[UserPlanJSON] = None
    private_gists: Optional[int] = None
    total_private_repos: Optional[int] = None
    owned_private_repos: Optional[int] = None
    disk_usage: Optional[int] = None
    collaborators: Optional[int] = None
    two_factor_authentication: Optional[bool] = True
    business_plus: Optional[bool] = False
    ldap_dn: Optional[str] = None


class SimpleUserJSON(TypedDict):
    """
    A simple GitHub user.
    """

    name: Optional[str]
    email: Optional[str]
    login: str
    id: int
    node_id: str
    avatar_url: HttpUrl  # has "format": "uri"
    gravatar_id: Optional[str]  # can be null but required
    url: HttpUrl  # has "format": "uri"
    html_url: HttpUrl  # has "format": "uri"
    followers_url: HttpUrl  # has "format": "uri"
    following_url: str  # no format specified (template URL)
    gists_url: str  # no format specified (template URL)
    starred_url: str  # no format specified (template URL)
    subscriptions_url: HttpUrl  # has "format": "uri"
    organizations_url: HttpUrl  # has "format": "uri"
    repos_url: HttpUrl  # has "format": "uri"
    events_url: str  # no format specified (template URL)
    received_events_url: HttpUrl  # has "format": "uri"
    type: str
    site_admin: bool
    starred_at: Optional[str]
    user_view_type: Optional[str]


class SimpleUser(BaseModel):
    """
    A simple GitHub user.
    """

    name: Optional[str] = None
    email: Optional[str] = None
    login: str
    id: int
    node_id: str
    avatar_url: HttpUrl  # has "format": "uri"
    gravatar_id: Optional[str]  # can be null but required
    url: HttpUrl  # has "format": "uri"
    html_url: HttpUrl  # has "format": "uri"
    followers_url: HttpUrl  # has "format": "uri"
    following_url: str  # no format specified (template URL)
    gists_url: str  # no format specified (template URL)
    starred_url: str  # no format specified (template URL)
    subscriptions_url: HttpUrl  # has "format": "uri"
    organizations_url: HttpUrl  # has "format": "uri"
    repos_url: HttpUrl  # has "format": "uri"
    events_url: str  # no format specified (template URL)
    received_events_url: HttpUrl  # has "format": "uri"
    type: str
    site_admin: bool
    starred_at: Optional[str] = None
    user_view_type: Optional[str] = None


HoverCardSchema = {
    "title": "Hovercard",
    "description": "Hovercard",
    "type": "object",
    "properties": {
        "contexts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"},
                    "octicon": {"type": "string"},
                },
                "required": ["message", "octicon"],
            },
        }
    },
    "required": ["contexts"],
}


class HoverCardContextJSON(TypedDict):
    """
    A context for a GitHub Hovercard.
    """

    message: str
    octicon: str


class HoverCardContext(BaseModel):
    """
    A context for a GitHub Hovercard.
    """

    message: str
    octicon: str


class HoverCardJSON(TypedDict):
    """
    A GitHub Hovercard.
    """

    contexts: list[HoverCardContextJSON]


class HoverCard(BaseModel):
    """
    A GitHub Hovercard.
    """

    contexts: list[HoverCardContext]


class Contributor(BaseModel):
    """
    A GitHub contributor.
    """

    contributions: int
    type: str
    login: Optional[str] = None
    id: Optional[int] = None
    node_id: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None
    gravatar_id: Optional[str] = None
    url: Optional[HttpUrl] = None
    html_url: Optional[HttpUrl] = None
    followers_url: Optional[HttpUrl] = None
    following_url: Optional[str] = None
    gists_url: Optional[str] = None
    starred_url: Optional[str] = None
    subscriptions_url: Optional[HttpUrl] = None
    organizations_url: Optional[HttpUrl] = None
    repos_url: Optional[HttpUrl] = None
    events_url: Optional[str] = None
    received_events_url: Optional[HttpUrl] = None
    site_admin: Optional[bool] = False
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    user_view_type: Optional[str] = None
