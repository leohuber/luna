from pathlib import Path

from xdg_base_dirs import xdg_config_home, xdg_data_home


def _luna_directory(root: Path) -> Path:
    directory = root / "luna"
    directory.mkdir(exist_ok=True, parents=True)
    return directory


def data_directory() -> Path:
    """Return (possibly creating) the application data directory."""
    return _luna_directory(xdg_data_home())


def config_directory() -> Path:
    """Return (possibly creating) the application config directory."""
    return _luna_directory(xdg_config_home())


def config_file() -> Path:
    return config_directory() / "config.toml"
