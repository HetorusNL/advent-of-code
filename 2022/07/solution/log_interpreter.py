from pathlib import Path
import re


class LogInterpreter:
    def __init__(self):
        # use a linux path and default to root: '/'
        self.path = Path("/")
        self.filesystem_size: dict[str, int] = {}
        # precompile all top level regex lines here
        self._re_cmnd = re.compile(r"^\$\s+(?P<command>.*)$")
        self._re_dir = re.compile(r"^dir\s+(?P<dir>[a-zA-Z0-9_.]*)$")
        self._re_file = re.compile(r"^(?P<size>[0-9]*)\s*(?P<name>[a-zA-Z0-9_.]*)$")
        # precompile all commands
        self._re_cmd_ls = re.compile(r"^ls\s*$")
        self._re_cmd_cd = re.compile(r"^cd\s+(?P<dir>[a-zA-Z0-9._/]*)\s*$")

    def interpret_line(self, line: str):
        if match := re.match(self._re_cmnd, line):
            self._interpret_command(match["command"])
        elif match := re.match(self._re_dir, line):
            self._interpret_dir(match["dir"])
        elif match := re.match(self._re_file, line):
            self._interpret_file(int(match["size"]), match["name"])
        else:
            raise ValueError(f"unknown line: '{line}'")

    def _interpret_command(self, command: str):
        if match := re.match(self._re_cmd_ls, command):
            pass  # nothing to do here
        elif match := re.match(self._re_cmd_cd, command):
            self._interpret_command_cd(match["dir"])
        else:
            raise ValueError(f"unknown command: '{command}'")

    def _interpret_command_cd(self, dir: str):
        self.path = self.path / dir
        unix_path = self._to_unix_path(self.path)
        if unix_path not in self.filesystem_size:
            self.filesystem_size[unix_path] = 0

    def _interpret_dir(self, dir: str):
        full_dir_path = self.path / dir
        unix_path = self._to_unix_path(full_dir_path)
        if unix_path not in self.filesystem_size:
            self.filesystem_size[unix_path] = 0

    def _interpret_file(self, size: int, name: str):
        # add file size to all parents of resolved path
        for parent in self.path.resolve().parents:
            unix_path = self._to_unix_path(parent)
            self.filesystem_size[unix_path] += size
        # add file size to folder itself
        unix_path = self._to_unix_path(self.path)
        self.filesystem_size[unix_path] += size

    def _to_unix_path(self, path: Path):
        # remove the 'C:' from the path as resolve adds it
        return str(path.resolve().as_posix())[2:]
