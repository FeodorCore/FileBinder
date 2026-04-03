# FileBinder

A command-line utility and Python library for collecting, filtering, and bundling text files from a project directory into a single document. Ideal for feeding codebases to LLMs, archiving, or quick project analysis.

## 🔹 Requirements
- Python **3.10+** (uses modern type hints: `list[str]`, `Path | str`, `@dataclass(slots=True)`)
- Dependencies: `typer==0.24.1`

## 📦 Installation
```bash
pip install -r requirements.txt
```

## 🖥️ CLI Usage
Run from the project root:
```bash
python src/file_binder_cli.py <command> [options]
```

### Commands
| Command | Description |
|---------|-------------|
| `list`  | Preview the list of files that will be processed |
| `bind`  | Merge files into a single output document |

### Options
| Flag | Description | Default |
|------|-------------|---------|
| `-r, --root` | Project root directory | `.` |
| `-o, --output` | Output file path (`bind` only) | `filebinder.txt` |
| `--ef` | File names to exclude (repeatable) | `[]` |
| `--ed` | Directory names to exclude (repeatable) | `[]` |
| `-d, --dotfiles` | Include hidden files/folders (`.` prefix) | `False` |
| `-e, --encoding` | Text encoding | `utf-8` |

### Examples
```bash
# Preview files, excluding Git and cache directories
python src/file_binder_cli.py list --root . --ed .git --ed __pycache__ --ef .gitignore

# Bundle the project into bundle.txt
python src/file_binder_cli.py bind --root . --output bundle.txt --ed .git --ed .venv --ed __pycache__
```

## 💻 Programmatic Usage
```python
from src.FileBinder import FileBinder

binder = FileBinder(
    root_dir="path/to/project",
    target_file="output.txt",
    exclude_dirs={".git", "__pycache__", ".venv"},
    exclude_files={"README.md"},
    dotfiles=False,
    encoding="utf-8"
)

binder.bind()  # Execute the bundling process
```

## 📄 Output Format
Each file is wrapped with clear delimiters:
```
---
relative/path/to/file.py
---
file contents...
---
```
The document ends with an auto-generated `STRUCTURE:` section containing a sorted Python list of all successfully included files.

## 📁 Project Structure
```
FileBinder/
├── requirements.txt
└── src/
    ├── FileBinder.py          # Core logic: config, collection, filtering, I/O
    └── file_binder_cli.py     # CLI interface powered by typer
```

> 💡 **Note:** Only text files are processed. Binary files, unreadable files, or files that fail decoding are safely skipped with a warning logged to the console. Custom formatters can be passed via the `formatter` parameter in the Python API.