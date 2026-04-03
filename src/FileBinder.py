import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

Formatter = Callable[[Path, str], str]

@dataclass(slots=True)
class FileBinderConfig:
    exclude_files: set[str] = field(default_factory=set)
    exclude_dirs: set[str] = field(default_factory=set)
    dotfiles: bool = False
    root_dir: Path | str = "glub"
    target_file: Path | str = "filebinder.txt"
    encoding: str = "utf-8"

    def __post_init__(self) -> None:
        self.root_dir = Path(self.root_dir).resolve()
        self.target_file = Path(self.target_file).resolve()


class DefaultFormatter:
    def __call__(self, rel_path: Path, content: str) -> str:
        return f"---\n{rel_path}\n---\n{content}\n---\n"


class FileExclusionPolicy:
    def __init__(self, config: FileBinderConfig) -> None:
        self.root_dir = config.root_dir
        self.target_resolved = config.target_file.resolve()
        self.exclude_files = config.exclude_files
        self.exclude_dirs = config.exclude_dirs
        self.dotfiles = config.dotfiles

    def is_excluded(self, path: Path) -> bool:
        if path.resolve() == self.target_resolved:
            return True
        try:
            rel_parts = path.relative_to(self.root_dir).parts
        except ValueError:
            return True
        if not self.dotfiles and any(part.startswith(".") for part in rel_parts):
            return True
        if self.exclude_dirs and any(part in self.exclude_dirs for part in rel_parts[:-1]):
            return True
        if path.name in self.exclude_files:
            return True
        return False


class ProjectFileCollector:
    def __init__(self, root_dir: Path, exclusion_policy: FileExclusionPolicy) -> None:
        self.root_dir = root_dir
        self.exclusion_policy = exclusion_policy

    def collect(self) -> list[Path]:
        collected: list[Path] = []

        for path in self.root_dir.rglob("*"):
            if not path.is_file():
                continue

            if self.exclusion_policy.is_excluded(path):
                continue

            collected.append(path.relative_to(self.root_dir))

        return sorted(collected)


class TextFileReader:
    def __init__(self, encoding: str = "utf-8") -> None:
        self.encoding = encoding

    def read(self, abs_path: Path) -> str | None:
        try:
            return abs_path.read_text(encoding=self.encoding)
        except UnicodeDecodeError as e:
            logger.warning("File decoding error %s: %s", abs_path, e)
        except PermissionError as e:
            logger.warning("No read permissions %s: %s", abs_path, e)
        except OSError as e:
            logger.warning("Reading error %s: %s", abs_path, e)
        return None


class BoundFileWriter:
    def __init__(self, target_file: Path, encoding: str, formatter: Formatter) -> None:
        self.target_file = target_file
        self.encoding = encoding
        self.formatter = formatter

    def write(self, files: Iterable[Path], root_dir: Path, reader: TextFileReader) -> None:
        self.target_file.parent.mkdir(parents=True, exist_ok=True)

        with self.target_file.open("w", encoding=self.encoding) as output:
            list_files: list[Path] = []
            for rel_path in files:
                abs_path = root_dir / rel_path
                content = reader.read(abs_path)
                if content is not None:
                    output.write(self.formatter(rel_path, content))
                    list_files.append(root_dir.name / rel_path)
                    logger.debug("Added: %s", rel_path)

            output.write(f"STRUCTURE:\n{[str(file) for file in sorted(list_files)]}")

class FileBinder:
    def __init__(
            self,
            exclude_files: set[str] | None = None,
            exclude_dirs: set[str] | None = None,
            dotfiles: bool = False,
            root_dir: str | Path = ".",
            target_file: str | Path = "filebinder.txt",
            encoding: str = "utf-8",
            formatter: Callable[[Path, str], str] | None = None,
    ) -> None:
        self.config = FileBinderConfig(
            exclude_files=exclude_files or set(),
            exclude_dirs=exclude_dirs or set(),
            dotfiles=dotfiles,
            root_dir=root_dir,
            target_file=target_file,
            encoding=encoding,
        )

        self.formatter = formatter or DefaultFormatter()
        self.exclusion_policy = FileExclusionPolicy(self.config)
        self.collector = ProjectFileCollector(Path(self.config.root_dir), self.exclusion_policy)
        self.reader = TextFileReader(self.config.encoding)
        self.writer = BoundFileWriter(
            target_file=Path(self.config.target_file),
            encoding=self.config.encoding,
            formatter=self.formatter,
        )

    def collect_files(self) -> list[Path]:
        return self.collector.collect()

    def bind(self) -> None:
        files = self.collect_files()
        logger.info("Found files to merge: %d", len(files))
        self.writer.write(files, Path(self.config.root_dir), self.reader)
