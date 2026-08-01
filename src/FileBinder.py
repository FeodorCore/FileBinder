from pathlib import Path


class FileBinder:
    def __init__(
        self,
        ignore_file: bool = False,
        hidden_files: bool = False,
        name_file_ignore: str = "filebinderignore.txt",
        name_file_binder: str = "filebinder.txt",
    ) -> None:
        self.ignore_file: bool = ignore_file
        self.hidden_files: bool = hidden_files
        self.name_file_ignore: str = name_file_ignore
        self.name_file_binder: str = name_file_binder

    def bind(self) -> dict[Path, str]:
        filebinder = FileBinderFilter(
            self.ignore_file,
            self.hidden_files,
            self.name_file_ignore,
            self.name_file_binder,
        )
        filter = filebinder.filters()
        return FileBinderOperationIO.write(filter, self.name_file_binder)

    def read(self) -> dict[Path, str]:
        filebinder = FileBinderFilter(
            self.ignore_file,
            self.hidden_files,
            self.name_file_ignore,
            self.name_file_binder,
        )
        filter = filebinder.filters()
        return FileBinderOperationIO.read(filter)


class FileBinderOperationIO:
    @staticmethod
    def write(filter_list: list[Path], name_file_binder: str) -> dict[Path, str]:
        with open(name_file_binder, "w", encoding="utf-8") as w_file:
            report_dict: dict[Path, str] = dict()
            for i in filter_list:
                try:
                    with open(i, "r", encoding="utf-8") as r_file:
                        read_file = r_file.read()
                        _ = w_file.write(f"\n\n-----{i}-----\n\n")
                        _ = w_file.write(read_file)
                    report_dict[i] = "recorded"
                except FileNotFoundError:
                    report_dict[i] = "not found"
                except PermissionError:
                    report_dict[i] = "permission error"
                except UnicodeDecodeError:
                    report_dict[i] = "unicode decode error"
            return report_dict

    @staticmethod
    def read(filter_list: list[Path]) -> dict[Path, str]:
        report_dict: dict[Path, str] = dict()
        for i in filter_list:
            try:
                with open(i, "r", encoding="utf-8") as file:
                    _ = file.read(1)
                    report_dict[i] = "read"
            except FileNotFoundError:
                report_dict[i] = "not found"
            except PermissionError:
                report_dict[i] = "permission error"
            except UnicodeDecodeError:
                report_dict[i] = "unicode decode error"
        return report_dict


class FileBinderFilter:
    def __init__(
        self,
        ignore_file: bool,
        hidden_files: bool,
        name_file_ignore: str,
        name_file_binder: str,
    ):
        self.ignore_file: bool = ignore_file
        self.hidden_files: bool = hidden_files
        self.name_file_ignore: str = name_file_ignore
        self.name_file_binder: str = name_file_binder
        self.ignore_patterns = None
        self.list_return_files: list[Path] = list()
        self.current_dir: Path = Path.cwd()

    def filters(self) -> list[Path]:
        if not self.ignore_file:
            self.ignore_patterns: list[str] | None = self._conversion()
        for file in self.current_dir.rglob("*"):
            if file.is_file():
                if not self.hidden_files and any(
                    part.startswith(".") for part in file.parts
                ):
                    continue
                if self.ignore_patterns is not None and any(
                    i == str(file.relative_to(self.current_dir))
                    for i in self.ignore_patterns
                ):
                    continue
                if self.ignore_patterns is not None and any(
                    str(file.relative_to(self.current_dir)).startswith(i + "/")
                    for i in self.ignore_patterns
                ):
                    continue
                if (
                    file.name == self.name_file_binder
                    or file.name == self.name_file_ignore
                ):
                    continue
                self.list_return_files.append(file.relative_to(self.current_dir))
        return self.list_return_files

    def _conversion(self) -> list[str] | None:
        try:
            with open(self.name_file_ignore, "r", encoding="utf-8") as file:
                lines = [line.strip().strip("/") for line in file if line.strip()]
                return lines
        except FileNotFoundError:
            return None
        except PermissionError:
            return None
        except UnicodeDecodeError:
            return None
