<div align="center">

# asyncPyGithub

[![Testing](https://github.com/sudoDeVinci/asyncPyGithub/actions/workflows/testing.yml/badge.svg?branch=main)](https://github.com/sudoDeVinci/asyncPyGithub/actions/workflows/testing.yml)
[![Linting](https://github.com/sudoDeVinci/asyncPyGithub/actions/workflows/linting.yml/badge.svg?branch=main)](https://github.com/sudoDeVinci/asyncPyGithub/actions/workflows/linting.yml)
[![Type-Check](https://github.com/sudoDeVinci/asyncPyGithub/actions/workflows/mypy.yml/badge.svg?branch=main)](https://github.com/sudoDeVinci/asyncPyGithub/actions/workflows/mypy.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Validation: Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)

**A fully asynchronous Python library for the GitHub API with comprehensive type safety.**

</div>

---

## **Key Features**

<table>
  <tr>
    <td><strong>Fully Asynchronous</strong></td>
    <td>Built from the ground up with asyncio for maximum performance</td>
  </tr>

  <tr>
    <td><strong>Comprehensive Typing</strong></td>
    <td>Comprehensive type definitions to get the most out of your LSP.</td>
  </tr>

  <tr>
    <td><strong>Type-Safety</strong></td>
    <td>Pydantic v2 models with runtime validation.</td>
  </tr>

  <tr>
    <td><strong>Developer-First Experience</strong></td>
    <td>Intuitive 'Portal' pattern with comprehensive error handling.</td>
  </tr>

  <tr>
    <td><strong>Smart Caching</strong></td>
    <td>Built-in JSON caching system for optimized API usage</td>
  </tr>
</table>

---

## **Quick Start**

### Installation

```bash
# Clone the repository
git clone https://github.com/sudoDeVinci/asyncPyGithub.git
cd asyncPyGithub

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in your project root:

```bash
GITHUB_TOKEN=your_personal_access_token_here
```

### Basic Usage

```python
import asyncio
from asyncPyGithub import GitHubUserPortal

async def main():
    # Authenticate with GitHub
    status, user = await GitHubUserPortal.authenticate()
    
    if status == 200:
        print(f"Hello, {user.login}! You have {user.public_repos} public repos.")
    else:
        print(f"Authentication failed: {user.message}")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## **Advanced Usage**

### Concurrent API Calls

Real-world use would require executing multiple API calls simultaneously:

```python
import asyncio
from typing import Any
from types import CoroutineType
from asyncPyGithub import (
GitHubUserPortal,
GitHubRepositoryPortal,
UserQueryReturnable
)

async def fetch_user_data_concurrently() -> None:

    # Authenticate first
    status, user = await GitHubUserPortal.authenticate()
    if status != 200:
        return
    
    # Define multiple operations to run concurrently
    operations: list[CoroutineType[Any, Any, UserQueryReturnable]] = [
        GitHubUserPortal.get_by_id(user.id),
        GitHubUserPortal.get_by_username(user.login),
        GitHubUserPortal.all(since=0, per_page=10),
        GitHubUserPortal.get_hovercard(user.login),
        GitHubRepositoryPortal.get_organization_repos(
            organization="LEGO",
            type="all",
            sort="full_name",
            direction="asc",
            per_page=5,
            page=1,
        )
    ]
    
    # Execute all operations concurrently
    results = await asyncio.gather(*operations)
    
    # Check results
    for i, (status_code, data) in enumerate(results):
        print(f"Operation {i+1}: Status {status_code}")
        if status_code == 200:
            print(f"Success: {type(data).__name__}")
        else:
            print(f"Error: {data.message}")

if __name__ == "__main__":
    asyncio.run(fetch_user_data_concurrently())

```

---

## **API Reference**

### GitHubUserPortal

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `authenticate()` | Authenticate user and get profile | None | `tuple[int, PrivateUser \| ErrorMessage]` |
| `update(changes)` | Update authenticated user's profile | `SimpleUserJSON` | `tuple[int, PrivateUser \| ErrorMessage]` |
| `get_by_id(uid)` | Get user by ID | `int` | `tuple[int, PrivateUser \| ErrorMessage]` |
| `get_by_username(username)` | Get user by username | `str` | `tuple[int, PrivateUser \| ErrorMessage]` |
| `all(since, per_page)` | List all users | `int, int` | `tuple[int, list[SimpleUser] \| ErrorMessage]` |
| `get_hovercard(username)` | Get user hovercard | `str` | `tuple[int, HoverCard \| ErrorMessage]` |

### GitHubRepositoryPortal

| Method | Description | Parameters | Returns |
|--------|-------------|------------|---------|
| `get_organization_repos(organization, type, sort, direction, per_page, page)` | List organization repositories | `str, RepositoryType, RepoSortCriterion, RepoSortDirection` | `tuple[int, list[MinimalRepository] \| ErrorMessage]` |
| ``

---

## 🏗️ **Architecture**

### Portal Pattern

asyncPyGithub uses the idea of  **Portals** for clean, organized API access:

```
GitHubUserPortal ──────► User-related operations
GitHubRepositoryPortal ──► Repository operations  
GitHubPortal (Base) ────► Shared authentication & utilities
```

### Type System

**Comprehensive type coverage** with Pydantic v2:

- **Models**: `PrivateUser`, `SimpleUser`, `MinimalRepository`
- **TypedDicts**: JSON-compatible interfaces for all GitHub responses
- **Validation**: Runtime type checking and data validation
- **IDE Support**: Full IntelliSense and error detection

### Error Handling

**Consistent error patterns**:

```python
status_code, result = await GitHubUserPortal.some_operation()

if status_code == 200:
    # Success: result is the expected data type
    print(f"Success: {result.login}")
else:
    # Error: result is an ErrorMessage object
    print(f"Error {result.code}: {result.message}")
```

---


## 🤝 **Contributing**

We welcome contributions! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/asyncPyGithub.git
cd asyncPyGithub

# Install development dependencies
pip install -r reqs.txt

# Run type checking
mypy .

# Run linting
ruff check .

# Format code
black .
```

---

## 📖 **Examples**

Check out `example.py` for comprehensive usage examples including:

- Authentication workflows
- Concurrent API operations
- Data caching and serialization
- Error handling patterns
- Real-world use cases

---

## 🐛 **Known Issues & Limitations**

- **Rate Limiting**: No built-in rate limiting (implement your own delays)
- **Pagination**: Manual pagination handling required for large datasets
- **Webhooks**: No webhook handling capabilities (API-only)

---

