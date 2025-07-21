from typing import Final, Callable, Any
from os import environ, makedirs
from dotenv import load_dotenv  # type: ignore
from logging import getLogger, Logger
from requests import Response, get
from pathlib import Path
import asyncio
from threading import Lock
from json import dump, JSONDecodeError, load

LOGGER: Logger = getLogger(__name__)
LOGGER.setLevel("INFO")

load_dotenv()
CWD: Final[Path] = Path(__file__).parent.resolve()
CACHE_DIR: Final[Path] = CWD / "__github_cache__"
makedirs(CACHE_DIR, exist_ok=True)

REPOSLICE_JSON: Final[Path] = CACHE_DIR / "repos.json"
USER_JSON: Final[Path] = CACHE_DIR / "users.json"

REPO_CACHE_LOCK: Lock = Lock()
USER_CACHE_LOCK: Lock = Lock()
API_VERSION: Final[str] = "2022-11-28"
API_ENDPOINT: Final[str] = "https://api.github.com"
TOKEN: str | None = None

try:
    assert load_dotenv(
        verbose=True
    ), "Failed to load environment variables from .env file."
    TOKEN = environ.get("GITHUB_TOKEN", environ.get("TOKEN", None))

    assert TOKEN is not None, "GITHUB_TOKEN must be set in environment variables."
except (AssertionError, AttributeError, OSError) as err:
    LOGGER.error(f"Error during global configuration:::{err}")


def write_json(fp: Path, data: dict[str, Any] | None) -> bool:
    """
    Writes a dictionary to a JSON file at the specified path.
    Args:
        fp (Path): The file path where the JSON data should be written.
        data (dict[str, Any] | None): The data to write to the JSON file. If None, no action is taken.
    Returns:
        bool: True if the data was written successfully, False otherwise.
    """
    if not data:
        LOGGER.warning(f"write_json:::No data to write to {fp}")
        return False

    try:
        with open(fp, "w") as f:
            dump(data, f, indent=4, ensure_ascii=False)
            LOGGER.info(f"write_json:::{fp} written to successfully")
            return True
    except (IOError, OSError) as err:
        LOGGER.error(f"write_json:::Failed to write data {err} to file {fp}")
        return False


def read_json(fp: Path) -> dict[str, Any] | None:
    """
    Reads a JSON file from the specified path and returns its content as a dictionary.
    Args:
        fp (Path): The file path from which to read the JSON data.
    Returns:
        dict[str, Any] | None: The data read from the JSON file as a dictionary, or None if the file does not exist or an error occurs.
    """
    if not fp.exists():
        LOGGER.warning(f"read_json:::File {fp} does not exist.")
        return None

    try:
        with open(fp, "r", encoding="utf-8") as f:
            data = load(f)
            LOGGER.info(f"read_json:::{fp} read successfully")
            return data
    except (IOError, OSError, JSONDecodeError) as err:
        LOGGER.error(f"read_json:::Failed to read data from {fp} with error: {err}")
        return None


async def req(fn: Callable, url: str, **kwargs) -> Response:
    """
    Asynchronously makes a request to the GitHub API using the provided function and URL.
    Args:
        fn (Callable): The function to use for making the request (e.g., requests.get).
        url (str): The endpoint URL to which the request will be made.
        **kwargs: Additional keyword arguments to pass to the request function.
    Returns:
        Response: The response object returned by the request function.
    """
    kwargs["timeout"] = 30
    kwargs.setdefault("headers", {}).update(
        {
            "Authorization": f"Bearer {TOKEN}",
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": "asyncPyGithub/1.0.0",
            "Accept": "application/vnd.github.v3+json",
        }
    )
    r = await asyncio.to_thread(fn, f"{API_ENDPOINT}{url}", **kwargs)
    await asyncio.sleep(0.10)
    return r


async def get_file_details(
    username: str,
    repository: str,
    path: str,
) -> tuple[int, dict[str, Any] | None]:
    """
    Asynchronously retrieves the content of a file in a specific repository.
    Args:
        username (str): The GitHub username of the repository owner.
        repository (str): The name of the repository.
        path (str): The path to the file within the repository.

    Returns:
        tuple[int, str | None]: A tuple containing the HTTP status code and the content of the file as a string, or None if the file does not exist or an error occurs.
    """
    response = await req(
        fn=get,
        url=f"/repos/{username}/{repository}/contents/{path}",
    )

    return (response.status_code, response.json())
