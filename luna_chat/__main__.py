"""
Luna CLI
"""

import asyncio
import tomllib
from textwrap import dedent
from typing import Any

import click
from click_default_group import DefaultGroup
from dotenv import load_dotenv
from rich.console import Console

from luna_chat.app import Luna
from luna_chat.config import LaunchConfig
from luna_chat.database.database import create_database, sqlite_file_name
from luna_chat.locations import config_file

console = Console()


def create_db_if_not_exists() -> None:
    if not sqlite_file_name.exists():
        click.echo(f"Creating database at {sqlite_file_name!r}")
        asyncio.run(create_database())


def load_or_create_config_file() -> dict[str, Any]:
    config = config_file()

    try:
        file_config = tomllib.loads(config.read_text())
    except FileNotFoundError:
        file_config = {}
        try:
            config.touch()
        except OSError:
            pass

    return file_config


@click.group(cls=DefaultGroup, default="default", default_if_no_args=True)
def cli() -> None:
    """Interact with large language models using your terminal."""


@cli.command()
@click.option(
    "-i",
    "--inline",
    is_flag=True,
    help="Run in inline mode, without launching full GUI.",
    default=False,
)
def default(*, inline: bool) -> None:
    create_db_if_not_exists()

    launch_config: dict[str, Any] = load_or_create_config_file()
    app = Luna(LaunchConfig(**launch_config))
    app.run(inline=inline)


@cli.command()
def reset() -> None:
    """
    Reset the database

    This command will delete the database file and recreate it.
    Previously saved conversations and data will be lost.
    """
    from rich.padding import Padding
    from rich.text import Text

    console.print(
        Padding(
            Text.from_markup(
                dedent(
                    f"""\
[u b red]Warning![/]

[b red]This will delete all messages and chats.[/]

You may wish to create a backup of \
"[bold blue u]{sqlite_file_name.resolve().absolute()!s}[/]" before continuing.
            """,
                ),
            ),
            pad=(1, 2),
        ),
    )
    if click.confirm("Delete all chats?", abort=True):
        sqlite_file_name.unlink(missing_ok=True)
        asyncio.run(create_database())
        console.print(f"♻️  Database reset @ {sqlite_file_name}")


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    cli()
