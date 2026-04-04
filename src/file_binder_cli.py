import typer
from typing import List
from src.FileBinder import FileBinder

app = typer.Typer(name="filebinder", help="Utility for merging files", add_completion=False)

@app.command(name="list", help="Show list of files to be processed")
def cmd_list(
        root: str = typer.Option(".", "--root", "-r", help="Project root directory"),
        exclude_file: List[str] = typer.Option([], "--ef", help="Exclude files (can be specified multiple times)"),
        exclude_dir: List[str] = typer.Option([], "--ed", help="Exclude directories (can be specified multiple times)"),
        dotfiles: bool = typer.Option(False, "--dotfiles", "-d", help="Include hidden files (starting with a dot)"),
):
    binder = FileBinder(
        root_dir=root,
        exclude_files=set(exclude_file),
        exclude_dirs=set(exclude_dir),
        dotfiles=dotfiles
    )
    files = binder.collect_files()
    typer.echo(f"Found {len(files)} files:")
    for f in files:
        typer.echo(f"  - {f}")


@app.command(name="bind", help="Merge files into a single output file")
def cmd_bind(
        root: str = typer.Option(".", "--root", "-r", help="Project root directory"),
        output: str = typer.Option("filebinder.txt", "--output", "-o", help="Output file name"),
        exclude_file: List[str] = typer.Option([], "--ef", help="Exclude files"),
        exclude_dir: List[str] = typer.Option([], "--ed", help="Exclude directories"),
        dotfiles: bool = typer.Option(False, "--dotfiles", "-d", help="Include hidden files"),
        encoding: str = typer.Option("utf-8", "--encoding", "-e", help="File encoding"),
):
    binder = FileBinder(
        root_dir=root,
        target_file=output,
        exclude_files=set(exclude_file),
        exclude_dirs=set(exclude_dir),
        dotfiles=dotfiles,
        encoding=encoding
    )
    typer.echo("Starting merge...")
    binder.bind()
    typer.echo(f"Done! Result saved to: {output}")

if __name__ == "__main__":
    app()