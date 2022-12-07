from pathlib import Path

from solution.log_interpreter import LogInterpreter


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        log_interpreter = LogInterpreter()
        for line in self.lines:
            log_interpreter.interpret_line(line)

        # the constants and total disk usage and space needed for this part
        total_disk_space = 70_000_000
        unused_required = 30_000_000
        total_disk_usage = log_interpreter.filesystem_size["/"]
        space_needed = total_disk_usage - (total_disk_space - unused_required)

        # find the suitable folders that are larger (or equal to) the space needed
        file_sizes = log_interpreter.filesystem_size.values()
        suitable_folders_sizes = {value for value in file_sizes if value >= space_needed}
        # find the folder with the least amount of space usage, satisfying the space needed
        self.directory_to_delete = min(suitable_folders_sizes)

    def get_result(self) -> str:
        return f"the smallest directory to delete to satisfy space needs: {self.directory_to_delete}"
