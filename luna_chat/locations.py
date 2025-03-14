"""This module provides functions to manage the application's data and configuration directories."""

from pathlib import Path

# The application data and config directories are stored in the user's home directory.
__data_home: Path = Path.home() / ".local" / "share"
__config_home: Path = Path.home() / ".config"


def _luna_directory(root: Path) -> Path:
    directory = root / "luna"
    directory.mkdir(exist_ok=True, parents=True)
    return directory


def data_directory() -> Path:
    """Return (possibly creating) the application data directory."""
    return _luna_directory(__data_home)


def config_directory() -> Path:
    """Return (possibly creating) the application config directory."""
    return _luna_directory(__config_home)


def config_file() -> Path:
    return config_directory() / "config.toml"
