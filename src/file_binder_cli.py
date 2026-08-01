from pathlib import Path
from typing import Annotated
import typer
from src.FileBinder import FileBinder

app = typer.Typer(
    name="filebinder",
    help="A CLI utility for bundling project files",
    add_completion=False,
)


@app.command(help="Bundle files into a single output file")
def bind(
    ignore_file: Annotated[
        bool, typer.Option("--ignore", "-i", help="Bypass the ignore file")
    ] = False,
    hidden_files: Annotated[
        bool,
        typer.Option("--hidden", "-s", help="Include hidden files and directories"),
    ] = False,
    name_file_ignore: Annotated[
        str, typer.Option("--nignore", "-ni", help="Custom name for the ignore file")
    ] = "filebinderignore.txt",
    name_file_binder: Annotated[
        str, typer.Option("--nbinder", "-nb", help="Name of the output bundle file")
    ] = "filebinder.txt",
):
    filebinder = FileBinder(
        ignore_file=ignore_file,
        hidden_files=hidden_files,
        name_file_ignore=name_file_ignore,
        name_file_binder=name_file_binder,
    )
    show_bind = filebinder.bind()
    typer.secho(f"Files are written to: {name_file_binder}")
    show_files(show_bind, "recorded")


@app.command(help="List files that will be included")
def read(
    ignore_file: Annotated[
        bool, typer.Option("--ignore", "-i", help="Bypass the ignore file")
    ] = False,
    hidden_files: Annotated[
        bool,
        typer.Option("--hidden", "-s", help="Include hidden files and directories"),
    ] = False,
    name_file_ignore: Annotated[
        str,
        typer.Option(
            "--nignore",
            "-ni",
            help="Custom name for the ignore file",
        ),
    ] = "filebinderignore.txt",
):
    filebinder = FileBinder(
        ignore_file=ignore_file,
        hidden_files=hidden_files,
        name_file_ignore=name_file_ignore,
    )
    show_read = filebinder.read()
    show_files(show_read, "read")


@app.command(help="Show program information")
def info():
    typer.secho("FileBinder", bold=True)
    typer.echo("-------------------------------")
    typer.echo("Version:   1.0.1")
    typer.echo("Author:    FeodorCore")
    typer.echo("GitHub:    https://github.com/FeodorCore/FileBinder")
    typer.echo("Description: A utility for efficiently bundling and indexing files")
    typer.echo("-------------------------------")
    typer.secho("Thank you for using FileBinder!", fg=typer.colors.RED)


def show_files(files: dict[Path, str], successful_status: str):
    typer.secho("Files status:")
    for path, status in files.items():
        if status == successful_status:
            typer.secho(f" ✓ {str(path):<50}{status}")
        else:
            typer.secho(f" ✗ {str(path):<50}{status}", fg=typer.colors.RED)


if __name__ == "__main__":
    app()
