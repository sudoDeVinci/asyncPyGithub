import string
from datetime import datetime
from typing import (
    Any,
    Dict,
    List,
    Literal,
    NotRequired,
    Optional,
    TypedDict,
)

from pydantic import BaseModel, HttpUrl


class ContentLinkJSON(TypedDict):
    git: Optional[HttpUrl]
    html: Optional[HttpUrl]
    self: HttpUrl


class ContentLink(BaseModel):
    git: Optional[HttpUrl]
    html: Optional[HttpUrl]
    self: HttpUrl


class ContentNodeJSON(TypedDict):
    type: str
    size: str
    name: str
    path: str
    sha: str
    content: NotRequired[str]
    url: HttpUrl
    git_url: HttpUrl
    html_url: HttpUrl
    download_url: Optional[HttpUrl]
    _links: ContentLinkJSON


class ContentNode(BaseModel):
    type: str
    size: str
    name: str
    path: str
    sha: str
    content: Optional[str] = None
    url: HttpUrl
    git_url: HttpUrl
    html_url: HttpUrl
    download_url: Optional[HttpUrl] = None
    _links: ContentLink


class ContentTreeJSON(ContentNodeJSON):
    entries: List[ContentNodeJSON]
    encoding: NotRequired[str]


class ContentTree(ContentNode):
    entries: List[ContentNode]
    encoding: Optional[str] = None
