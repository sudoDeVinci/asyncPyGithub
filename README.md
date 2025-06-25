# asyncPyGithub

An asynchronous Python library for interacting with the GitHub API, built with modern Python features and type safety.

- 🚀 Fully Asynchronous: Built with asyncio for high-performance API interactions
- 🔒 Type Annotations: Complete type annotations using TypedDict for GitHub API responses - easily configurable/extendable
- 📊 Extended Repository Data: QOL additions such as automatically fetching programming languages for repositories
- 🛠️ Caching Support: Built-in JSON caching for API responses
- 📝 Comprehensive Logging: Detailed logging for debugging and monitoring

## Installation

Relies on `requests` and `python-dotenv`

```bash
pip install python-dotenv requests
```

## Quick Start

Create an `.env` file with your github token

```bash
GITHUB_TOKEN=your_github_token_here
```

### Basic Usage

```py
import asyncio
from asyncpygithub import get_authenticated_user

async def main():
    # Get authenticated user info
    status, user = await get_authenticated_user()
    print(f"Hello, {user['login']}!")

if __name__ == "__main__":
    asyncio.run(main())
```

### Multiple method calling

Calling multiple methods with little to no overlap benefit greatly from concurrency.
For example, we can call these (3) methods one by one:

```py
async def one_by_one_example() ->None:
    status, user = await get_authenticated_user()
        ...
    
    status, repos = await get_repos_authenticated(per_page=10)
        ...

    slice = await get_repos_authenticated_extended(per_page=10)
        ...

```

However, this would not be much faster than the synchronous equivalent.
To get the full benefits, we can use `asyncio.gather` like so:

```py
async def async_gathered_example() -> None:
    funcs:tuple[callable] = (
        get_authenticated_user(),
        get_repos_authenticated(per_page=15),
        get_repos_authenticated_extended(per_page=15),
    )
    results = await asyncio.gather(*funcs)
```

This example on average will grant us at least a 3x speedup, not allowing the waiting time of each API call to block the others on which it does not rely.
The gap between the synchronous and async time taken for independent function calls grows basocally exponentially (assumind the same time for pos/pre-processing of your data).
