from typing import TypedDict

class User(TypedDict, total=False):
    """
    A GitHub authenticated User.

    Attributes:
        login (str): The username of the user.
        id (int): The unique identifier for the user.
        node_id (str): The node ID of the user.
        avatar_url (str): The URL to the user's avatar image.
        gravatar_id (str): The Gravatar ID of the user.
        url (str): The API URL for the user.
        html_url (str): The HTML URL for the user's profile.
        followers_url (str): The URL to fetch followers of the user.
        following_url (str): The URL to fetch users followed by this user.
        gists_url (str): The URL to fetch gists created by this user.
        starred_url (str): The URL to fetch starred repositories by this user.
        subscriptions_url (str): The URL to fetch subscriptions of this user.
        organizations_url (str): The URL to fetch organizations this user belongs to.
        repos_url (str): The URL to fetch repositories owned by this user.
        events_url (str): The URL to fetch public events for this user.
        received_events_url (str): The URL to fetch received events for this user.
        type (str): The type of the user, e.g., "User" or "Bot".
        site_admin (bool): Whether the user is a site administrator.
        name (str | None): The full name of the user, if available.
        company (str | None): The company associated with the user, if available.
        blog (str | None): The blog URL of the user, if available.
        location (str | None): The location of the user, if available.
        email (str | None): The email address of the user, if available.
        hireable (bool | None): Whether the user is hireable, if specified.
        bio (str | None): A short biography of the user, if available.
        twitter_username (str | None): The Twitter username of the user, if available.
        public_repos (int): Number of public repositories owned by the user.
        public_gists (int): Number of public gists created by the user.
        followers (int): Number of followers this user has.
        following (int): Number of users this user is following.
        created_at (str): Timestamp when the user's account was created.
        updated_at (str): Timestamp when the user's account was last updated.
        private_gists (int | None): Number of private gists created by the user, if available.
        total_private_repos (int | None): Total number of private repositories owned by the user, if available.
        owned_private_repos (int | None): Number of private repositories owned by the user, if available.
        disk_usage (int | None): Disk usage of the user's repositories, if available.
        collaborators (int | None): Number of collaborators in the user's private repositories, if available.
        two_factor_authentication (bool): Whether the user has two-factor authentication enabled.
        plan (dict[str, str | int | bool] | None): Information about the user's plan, if available.
    """
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    site_admin: bool
    name: str | None
    company: str | None
    blog: str | None
    location: str | None
    email: str | None
    hireable: bool | None
    bio: str | None
    twitter_username: str | None
    public_repos: int
    public_gists: int
    followers: int
    following: int
    created_at: str
    updated_at: str
    private_gists: int | None
    total_private_repos: int | None
    owned_private_repos: int | None
    disk_usage: int | None
    collaborators: int | None
    two_factor_authentication: bool
    plan: dict[str, str | int | bool] | None

