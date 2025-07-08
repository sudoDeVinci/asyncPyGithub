[![Linting](https://github.com/sudoDeVinci/asyncPyGithub/actions/workflows/linting.yml/badge.svg?branch=main)](https://github.com/sudoDeVinci/asyncPyGithub/actions/workflows/linting.yml)

# asyncPyGithub

An asynchronous Python library for interacting with the GitHub API, built with modern Python features and type safety.

- 🚀 Fully Asynchronous
- 🔒 Type Checking and Validation
- 📊 Minimalistic Interaction Interface
- 🛠️ Caching Support
- 📝 Logging and Easy Debugging

## Installation

Relies on `requests`, `python-dotenv` and `Pydanticv2`.

```bash
pip install -r reqs.txt
```

## Quick Start

Create an `.env` file with your github token

```bash
GITHUB_TOKEN=your_github_token_here
```

### Basic Usage

```py
import asyncio
from asyncpygithub import User

async def main():
    status, user = await User.authenticate()
    if status == 200:
        print(f"Hello, {user.login}!")
    else:
        ...

if __name__ == "__main__":
    asyncio.run(main())
```

### Multiple method calling

Calling multiple methods with little to no overlap benefit greatly from concurrency.
For example, we can call these (3) methods one by one:

```py
from asyncpygithub import User

async def one_by_one_example() ->None:
    await User.get_by_id( ... )
    await User.get_by_username( ... )
    await User.all( ... )
        
        ...
```

However, this is no better than the synchronous equivalent.
To get the full benefits, we can use `asyncio.gather` like so:

```py
async def async_gathered_example() -> None:
    awaitables:list[CoroutineType[UserQueryReturnable, Any, Any]] = (
        User.get_by_id( ... )
        User.get_by_username( ... )
        User.all( ... )
    )
    results = await asyncio.gather(*awaitables)
```
