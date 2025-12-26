<div align="center">

# asyncPyGithub

[![Testing](https://github.com/sudoDeVinci/asyncPyGithub/actions/workflows/testing.yml/badge.svg?branch=main)](https://github.com/sudoDeVinci/asyncPyGithub/actions/workflows/testing.yml)
[![Linting](https://github.com/sudoDeVinci/asyncPyGithub/actions/workflows/linting.yml/badge.svg?branch=main)](https://github.com/sudoDeVinci/asyncPyGithub/actions/workflows/linting.yml)
[![Type-Check](https://github.com/sudoDeVinci/asyncPyGithub/actions/workflows/mypy.yml/badge.svg?branch=main)](https://github.com/sudoDeVinci/asyncPyGithub/actions/workflows/mypy.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Validation: Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)

**A fully asynchronous Python library for the GitHub API.**

</div>

## Install

```bash
git clone https://github.com/sudoDeVinci/asyncPyGithub.git
cd asyncPyGithub
pip install -r requirements.txt
```

## Setup

Create a `.env` file:

```
GITHUB_TOKEN=your_token_here
```

## Client Lifecycle

The library uses a shared `httpx.AsyncClient` under the hood. You have two options for managing it:

### Option 1: Let it auto-start (simple)

The client starts automatically on first request. Just remember to close it when done:

```python
import asyncio
from asyncPyGithub import GitHubPortal, GitHubUserPortal

async def main():
    # Client starts automatically on first request
    status, user = await GitHubPortal.authenticate("your_token")
    if status != 200:
        print(f"Auth failed: {user.message}")
        return
    
    print(f"Logged in as {user.login}")
    
    # Do stuff...
    status, other = await GitHubUserPortal.get_by_username("torvalds")
    if status == 200:
        print(f"Found: {other.login}")
    
    # Clean up when done
    await GitHubPortal.close()

asyncio.run(main())
```

### Option 2: Use the context manager (scoped)

For scoped usage where you want automatic cleanup:

```python
import asyncio
from asyncPyGithub import GitHubPortal, GitHubUserPortal

async def main():
    async with GitHubPortal.scoped_client():
        status, user = await GitHubPortal.authenticate("your_token")
        if status != 200:
            return
        
        status, other = await GitHubUserPortal.get_by_username("torvalds")
        # Client closes automatically when exiting the context

asyncio.run(main())
```

## Concurrent Requests

The client uses connection pooling, so concurrent requests share connections efficiently:

```python
import asyncio
from asyncPyGithub import GitHubPortal, GitHubUserPortal, GitHubRepositoryPortal

async def main():
    status, user = await GitHubPortal.authenticate("your_token")
    if status != 200:
        return
    
    # All requests run concurrently over the shared client
    results = await asyncio.gather(
        GitHubUserPortal.get_by_id(user.id),
        GitHubUserPortal.get_by_username(user.login),
        GitHubUserPortal.all(since=0, per_page=5),
        GitHubRepositoryPortal.get_organization_repos("LEGO", per_page=5),
    )
    
    for status, data in results:
        if status == 200:
            print(f"OK: {type(data).__name__}")
        else:
            print(f"Error: {data.message}")
    
    await GitHubPortal.close()

asyncio.run(main())
```

## API

Every method returns `tuple[int, Result | ErrorMessage]`. Check the status code first.

### GitHubPortal

| Method | What it does |
|--------|--------------|
| `authenticate(token)` | Auth and get your user info. Starts client if needed. |
| `start()` | Manually start the HTTP client |
| `close()` | Close the HTTP client |
| `scoped_client()` | Context manager that auto-closes on exit |

### GitHubUserPortal

| Method | What it does |
|--------|--------------|
| `update(changes)` | Update your profile |
| `get_by_id(uid)` | Get user by ID |
| `get_by_username(username)` | Get user by username |
| `all(since, per_page)` | List users |
| `get_hovercard(username)` | Get hovercard info |

### GitHubRepositoryPortal

| Method | What it does |
|--------|--------------|
| `get_organization_repos(org, ...)` | List org repos |
| `create_organization_repo(org, name, ...)` | Create repo in org |
| `get_user_repo(owner, repo)` | Get a specific repo |
| `update_repository(owner, repo, ...)` | Update repo settings |
| `delete_repository(owner, repo)` | Delete a repo |
| `list_contributors(owner, repo)` | List contributors |
| `list_repository_languages(owner, repo)` | Get language breakdown |
| `list_repository_tags(owner, repo)` | List tags |
| `get_repository_topics(owner, repo)` | Get topics |

## Error Handling

```python
status, result = await GitHubUserPortal.get_by_username("doesnt-exist")

if status == 200:
    print(result.login)
else:
    # result is an ErrorMessage
    print(f"Error {result.code}: {result.message}")
```

## Structure

```
GitHubPortal              # Base - auth, client management
├── GitHubUserPortal      # /user and /users endpoints
└── GitHubRepositoryPortal # /repos and /orgs/.../repos endpoints
```

All responses are Pydantic models (`PrivateUser`, `SimpleUser`, `MinimalRepository`, etc.).

## Testing

```bash
pip install -r requirements-dev.txt
pytest
```

## Limitations

- No rate limit handling
- No pagination helpers
- No webhooks
