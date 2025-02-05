## Introduction

For more details, you can refer to the [pyproject.toml](https://github.com/darrenburns/elia/blob/main/pyproject.toml) file.

## Installation

Install Luna with [pipx](https://github.com/pypa/pipx):

```bash
pipx install --python 3.11 luna-chat
```

Depending on the model you wish to use, you may need to set one or more environment variables (e.g. `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY` etc).

## Quickstart

Launch Luna from the command line:

```bash
luna
```

Launch a new chat inline (under your prompt) with `-i`/`--inline`:

```bash
luna -i "What is the Zen of Python?"
```

Launch a new chat in full-screen mode:

```bash
luna "Tell me a cool fact about lizards!"
```

Specify a model via the command line using `-m`/`--model`:

```bash
luna -m gpt-4o
```

Options can be combined - here's how you launch a chat with Gemini 1.5 Flash in inline mode (requires `GEMINI_API_KEY` environment variable).

```bash
luna -i -m gemini/gemini-1.5-flash-latest "How do I call Rust code from Python?"
```

## Uninstalling

```bash
pipx uninstall luna-chat
```

## Setting Up the Python Environment

To initialize the Python environment using the `uv` tool, follow these steps:

1. **Install `rustc`, `cargo` and `rustup`**: Install (if not done already) the standalone installer from [https://www.rust-lang.org](https://www.rust-lang.org/tools/install)

2. **Install `uv`**: Install (if not done already) the standalone installer from [https://docs.astral.sh](https://docs.astral.sh/uv/getting-started/installation/)

3. **Initialize or Syncronize the environment**:
    ```sh
    uv sync
    ```

4. **Activate the environment**:
    ```sh
    source .venv/bin/activate
    ```

## Install pre-commit

todo

These commands will set up and activate a new Python environment using `uv`.

## Third Party Libraries Used in Runtime

| Title       | Description                                        | Weblink                                                                    |
|-------------|----------------------------------------------------|----------------------------------------------------------------------------|
| Textual     | For building the terminal user interface           | [https://textual.textualize.io](https://textual.textualize.io)             |
| Pydantic    | For data validation and settings management        | [https://docs.pydantic.dev/latest/](https://docs.pydantic.dev/latest/)     |
| LiteLLM     | For interacting with various language models       | [https://docs.litellm.ai](https://docs.litellm.ai)                         |
| SQLAlchemy  | For database interactions                          | [https://www.sqlalchemy.org](https://www.sqlalchemy.org)                   |
| Click       | For creating command line interfaces               | [https://click.palletsprojects.com](https://click.palletsprojects.com)     |

## Third Party Libraries Used in Development Environment

| Title       | Description                                        | Weblink                                                                    |
|-------------|----------------------------------------------------|----------------------------------------------------------------------------|
| UV          | Python package and project manager                 | [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)                   |
| Pre-commit  | For managing and maintaining pre-commit hooks      | [https://pre-commit.com](https://pre-commit.com)                           |
| Black       | For code formatting                                | [https://black.readthedocs.io](https://black.readthedocs.io)               |
| MyPy        | For optional static typing for Python              | [https://mypy-lang.org](https://mypy-lang.org)                             |
| PyInstrument | For profiling Python code                         | [https://pyinstrument.readthedocs.io](https://pyinstrument.readthedocs.io) |


## Schemas and Concepts Used

| Title       | Description                                        | Weblink                                                                    |
|-------------|----------------------------------------------------|----------------------------------------------------------------------------|
| TOML        | For configuration files                            | [https://toml.io/en/](https://toml.io/en/)                                 |
