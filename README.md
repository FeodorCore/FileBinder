# FileBinder
[🇷🇺 Русский](README.ru.md) | [🇬🇧 English](README.md)

Console utility for merging project files into one text file.

## Installation

```bash
pip install .
```

Requirements: Python 3.10+, `typer==0.24.1`.

## Usage

```
filebinder [COMMAND] [OPTIONS]
```

## Commands

### `bind`
Bundle files into one output file.

```
filebinder bind [OPTIONS]
```

Options:
- `--ignore` / `-i` – Bypass the ignore file (ignore rules are not applied).
- `--hidden` / `-s` – Include hidden files and directories.
- `--nignore` / `-ni` TEXT – Custom name for the ignore file (default: `filebinderignore.txt`).
- `--nbinder` / `-nb` TEXT – Name of the output bundle file (default: `filebinder.txt`).

### `read`
List files that will be included (dry-run, no file written).

```
filebinder read [OPTIONS]
```

Options:
- `--ignore` / `-i`
- `--hidden` / `-s`
- `--nignore` / `-ni` TEXT

### `info`
Show program version, author, and description.

## Ignore file (`filebinderignore.txt`)
A plain text file with one relative path or directory prefix per line. Directories must end with `/` or be used as a prefix. Lines can be trimmed; empty lines are ignored.

Example:
```
.git/
node_modules/
temp.txt
dist/main.js
```

- Trailing slashes are stripped automatically.
- Matching logic: exact relative path match **or** file path starts with a listed directory prefix.

## Output format
The bundle file (`filebinder.txt` by default) contains:

```
-----relative/path/to/file.ext-----

<file content>

-----another/file.ext-----

<file content>
```

A status report is printed to the terminal:
- ✓ file recorded / read successfully
- ✗ file not found / permission error / unicode decode error

## Notes
- Always runs in the current working directory.
- The output file and the ignore file themselves are never included.
- Unicode decode errors are skipped and reported.