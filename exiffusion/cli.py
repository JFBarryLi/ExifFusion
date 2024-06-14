from typing import Optional

import typer

from importlib import metadata

APP_NAME = "ExifFusion"
APP_VERSION = metadata.version("exiffusion")

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{APP_NAME} v{APP_VERSION}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    return


def cli():
    app(prog_name=APP_NAME)
