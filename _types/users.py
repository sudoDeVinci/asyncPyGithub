from typing_extensions import (
    TypedDict,
    NotRequired,
    Optional,
)

from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    HttpUrl,
    PastDatetime
)

UserJSONSchema = {
  "oneOf": [
    {
      "title": "Private User",
      "description": "Private User",
      "type": "object",
      "properties": {
        "login": {
          "type": "string",
          "examples": [
            "octocat"
          ]
        },
        "id": {
          "type": "integer",
          "format": "int64",
          "examples": [
            1
          ]
        },
        "user_view_type": {
          "type": "string"
        },
        "node_id": {
          "type": "string",
          "examples": [
            "MDQ6VXNlcjE="
          ]
        },
        "avatar_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/images/error/octocat_happy.gif"
          ]
        },
        "gravatar_id": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "41d064eb2195891e12d0413f63227ea7"
          ]
        },
        "url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/users/octocat"
          ]
        },
        "html_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://github.com/octocat"
          ]
        },
        "followers_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/users/octocat/followers"
          ]
        },
        "following_url": {
          "type": "string",
          "examples": [
            "https://api.github.com/users/octocat/following{/other_user}"
          ]
        },
        "gists_url": {
          "type": "string",
          "examples": [
            "https://api.github.com/users/octocat/gists{/gist_id}"
          ]
        },
        "starred_url": {
          "type": "string",
          "examples": [
            "https://api.github.com/users/octocat/starred{/owner}{/repo}"
          ]
        },
        "subscriptions_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/users/octocat/subscriptions"
          ]
        },
        "organizations_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/users/octocat/orgs"
          ]
        },
        "repos_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/users/octocat/repos"
          ]
        },
        "events_url": {
          "type": "string",
          "examples": [
            "https://api.github.com/users/octocat/events{/privacy}"
          ]
        },
        "received_events_url": {
          "type": "string",
          "format": "uri",
          "examples": [
            "https://api.github.com/users/octocat/received_events"
          ]
        },
        "type": {
          "type": "string",
          "examples": [
            "User"
          ]
        },
        "site_admin": {
          "type": "boolean"
        },
        "name": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "monalisa octocat"
          ]
        },
        "company": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "GitHub"
          ]
        },
        "blog": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "https://github.com/blog"
          ]
        },
        "location": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "San Francisco"
          ]
        },
        "email": {
          "type": [
            "string",
            "null"
          ],
          "format": "email",
          "examples": [
            "octocat@github.com"
          ]
        },
        "notification_email": {
          "type": [
            "string",
            "null"
          ],
          "format": "email",
          "examples": [
            "octocat@github.com"
          ]
        },
        "hireable": {
          "type": [
            "boolean",
            "null"
          ]
        },
        "bio": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "There once was..."
          ]
        },
        "twitter_username": {
          "type": [
            "string",
            "null"
          ],
          "examples": [
            "monalisa"
          ]
        },
        "public_repos": {
          "type": "integer",
          "examples": [
            2
          ]
        },
        "public_gists": {
          "type": "integer",
          "examples": [
            1
          ]
        },
        "followers": {
          "type": "integer",
          "examples": [
            20
          ]
        },
        "following": {
          "type": "integer",
          "examples": [
            0
          ]
        },
        "created_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2008-01-14T04:33:35Z"
          ]
        },
        "updated_at": {
          "type": "string",
          "format": "date-time",
          "examples": [
            "2008-01-14T04:33:35Z"
          ]
        },
        "private_gists": {
          "type": "integer",
          "examples": [
            81
          ]
        },
        "total_private_repos": {
          "type": "integer",
          "examples": [
            100
          ]
        },
        "owned_private_repos": {
          "type": "integer",
          "examples": [
            100
          ]
        },
        "disk_usage": {
          "type": "integer",
          "examples": [
            10000
          ]
        },
        "collaborators": {
          "type": "integer",
          "examples": [
            8
          ]
        },
        "two_factor_authentication": {
          "type": "boolean",
          "examples": [
            True
          ]
        },
        "plan": {
          "type": "object",
          "properties": {
            "collaborators": {
              "type": "integer"
            },
            "name": {
              "type": "string"
            },
            "space": {
              "type": "integer"
            },
            "private_repos": {
              "type": "integer"
            }
          },
          "required": [
            "collaborators",
            "name",
            "space",
            "private_repos"
          ]
        },
        "business_plus": {
          "type": "boolean"
        },
        "ldap_dn": {
          "type": "string"
        }
      },
      "required": [
        "avatar_url",
        "events_url",
        "followers_url",
        "following_url",
        "gists_url",
        "gravatar_id",
        "html_url",
        "id",
        "node_id",
        "login",
        "organizations_url",
        "received_events_url",
        "repos_url",
        "site_admin",
        "starred_url",
        "subscriptions_url",
        "type",
        "url",
        "bio",
        "blog",
        "company",
        "email",
        "followers",
        "following",
        "hireable",
        "location",
        "name",
        "public_gists",
        "public_repos",
        "created_at",
        "updated_at",
        "collaborators",
        "disk_usage",
        "owned_private_repos",
        "private_gists",
        "total_private_repos",
        "two_factor_authentication"
      ]
    },
    {
      "title": "Public User",
      "description": "Public User",
      "type": "object",
      "properties": {
        "login": {
          "type": "string"
        },
        "id": {
          "type": "integer",
          "format": "int64"
        },
        "user_view_type": {
          "type": "string"
        },
        "node_id": {
          "type": "string"
        },
        "avatar_url": {
          "type": "string",
          "format": "uri"
        },
        "gravatar_id": {
          "type": [
            "string",
            "null"
          ]
        },
        "url": {
          "type": "string",
          "format": "uri"
        },
        "html_url": {
          "type": "string",
          "format": "uri"
        },
        "followers_url": {
          "type": "string",
          "format": "uri"
        },
        "following_url": {
          "type": "string"
        },
        "gists_url": {
          "type": "string"
        },
        "starred_url": {
          "type": "string"
        },
        "subscriptions_url": {
          "type": "string",
          "format": "uri"
        },
        "organizations_url": {
          "type": "string",
          "format": "uri"
        },
        "repos_url": {
          "type": "string",
          "format": "uri"
        },
        "events_url": {
          "type": "string"
        },
        "received_events_url": {
          "type": "string",
          "format": "uri"
        },
        "type": {
          "type": "string"
        },
        "site_admin": {
          "type": "boolean"
        },
        "name": {
          "type": [
            "string",
            "null"
          ]
        },
        "company": {
          "type": [
            "string",
            "null"
          ]
        },
        "blog": {
          "type": [
            "string",
            "null"
          ]
        },
        "location": {
          "type": [
            "string",
            "null"
          ]
        },
        "email": {
          "type": [
            "string",
            "null"
          ],
          "format": "email"
        },
        "notification_email": {
          "type": [
            "string",
            "null"
          ],
          "format": "email"
        },
        "hireable": {
          "type": [
            "boolean",
            "null"
          ]
        },
        "bio": {
          "type": [
            "string",
            "null"
          ]
        },
        "twitter_username": {
          "type": [
            "string",
            "null"
          ]
        },
        "public_repos": {
          "type": "integer"
        },
        "public_gists": {
          "type": "integer"
        },
        "followers": {
          "type": "integer"
        },
        "following": {
          "type": "integer"
        },
        "created_at": {
          "type": "string",
          "format": "date-time"
        },
        "updated_at": {
          "type": "string",
          "format": "date-time"
        },
        "plan": {
          "type": "object",
          "properties": {
            "collaborators": {
              "type": "integer"
            },
            "name": {
              "type": "string"
            },
            "space": {
              "type": "integer"
            },
            "private_repos": {
              "type": "integer"
            }
          },
          "required": [
            "collaborators",
            "name",
            "space",
            "private_repos"
          ]
        },
        "private_gists": {
          "type": "integer",
          "examples": [
            1
          ]
        },
        "total_private_repos": {
          "type": "integer",
          "examples": [
            2
          ]
        },
        "owned_private_repos": {
          "type": "integer",
          "examples": [
            2
          ]
        },
        "disk_usage": {
          "type": "integer",
          "examples": [
            1
          ]
        },
        "collaborators": {
          "type": "integer",
          "examples": [
            3
          ]
        }
      },
      "required": [
        "avatar_url",
        "events_url",
        "followers_url",
        "following_url",
        "gists_url",
        "gravatar_id",
        "html_url",
        "id",
        "node_id",
        "login",
        "organizations_url",
        "received_events_url",
        "repos_url",
        "site_admin",
        "starred_url",
        "subscriptions_url",
        "type",
        "url",
        "bio",
        "blog",
        "company",
        "email",
        "followers",
        "following",
        "hireable",
        "location",
        "name",
        "public_gists",
        "public_repos",
        "created_at",
        "updated_at"
      ],
      "additionalProperties": False
    }
  ]
}

class UserPlanJSON(TypedDict):
    """
    A GitHub authenticated User's plan.
    """
    collaborators: int
    name: str
    space: int
    private_repos: int

class UserJSON(TypedDict, total=False):
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

class User(BaseModel):
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

SimpleUserJSONSchema = {
  "type": "array",
  "items": {
    "title": "Simple User",
    "description": "A GitHub user.",
    "type": "object",
    "properties": {
      "name": {
        "type": [
          "string",
          "null"
        ]
      },
      "email": {
        "type": [
          "string",
          "null"
        ]
      },
      "login": {
        "type": "string",
        "examples": [
          "octocat"
        ]
      },
      "id": {
        "type": "integer",
        "format": "int64",
        "examples": [
          1
        ]
      },
      "node_id": {
        "type": "string",
        "examples": [
          "MDQ6VXNlcjE="
        ]
      },
      "avatar_url": {
        "type": "string",
        "format": "uri",
        "examples": [
          "https://github.com/images/error/octocat_happy.gif"
        ]
      },
      "gravatar_id": {
        "type": [
          "string",
          "null"
        ],
        "examples": [
          "41d064eb2195891e12d0413f63227ea7"
        ]
      },
      "url": {
        "type": "string",
        "format": "uri",
        "examples": [
          "https://api.github.com/users/octocat"
        ]
      },
      "html_url": {
        "type": "string",
        "format": "uri",
        "examples": [
          "https://github.com/octocat"
        ]
      },
      "followers_url": {
        "type": "string",
        "format": "uri",
        "examples": [
          "https://api.github.com/users/octocat/followers"
        ]
      },
      "following_url": {
        "type": "string",
        "examples": [
          "https://api.github.com/users/octocat/following{/other_user}"
        ]
      },
      "gists_url": {
        "type": "string",
        "examples": [
          "https://api.github.com/users/octocat/gists{/gist_id}"
        ]
      },
      "starred_url": {
        "type": "string",
        "examples": [
          "https://api.github.com/users/octocat/starred{/owner}{/repo}"
        ]
      },
      "subscriptions_url": {
        "type": "string",
        "format": "uri",
        "examples": [
          "https://api.github.com/users/octocat/subscriptions"
        ]
      },
      "organizations_url": {
        "type": "string",
        "format": "uri",
        "examples": [
          "https://api.github.com/users/octocat/orgs"
        ]
      },
      "repos_url": {
        "type": "string",
        "format": "uri",
        "examples": [
          "https://api.github.com/users/octocat/repos"
        ]
      },
      "events_url": {
        "type": "string",
        "examples": [
          "https://api.github.com/users/octocat/events{/privacy}"
        ]
      },
      "received_events_url": {
        "type": "string",
        "format": "uri",
        "examples": [
          "https://api.github.com/users/octocat/received_events"
        ]
      },
      "type": {
        "type": "string",
        "examples": [
          "User"
        ]
      },
      "site_admin": {
        "type": "boolean"
      },
      "starred_at": {
        "type": "string",
        "examples": [
          "\"2020-07-09T00:17:55Z\""
        ]
      },
      "user_view_type": {
        "type": "string",
        "examples": [
          "public"
        ]
      }
    },
    "required": [
      "avatar_url",
      "events_url",
      "followers_url",
      "following_url",
      "gists_url",
      "gravatar_id",
      "html_url",
      "id",
      "node_id",
      "login",
      "organizations_url",
      "received_events_url",
      "repos_url",
      "site_admin",
      "starred_url",
      "subscriptions_url",
      "type",
      "url"
    ]
  }
}

class SimpleUserJSON(TypedDict):
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
