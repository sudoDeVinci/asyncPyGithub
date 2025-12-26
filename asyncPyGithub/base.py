from json import JSONDecodeError, dump, load
from logging import Logger, getLogger
from os import makedirs
from pathlib import Path
from threading import Lock
from typing import Any, Final

from dotenv import load_dotenv  # type: ignore

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
