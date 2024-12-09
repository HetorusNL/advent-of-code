from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        assert len(self.lines) == 1

    def solve(self) -> None:
        print("solving...")
        self.allocate_disk_space()
        self.compact_disk_space()
        self.result = self.calculate_checksum()

    def allocate_disk_space(self):
        self.disk_space: list[int] = []
        is_file: bool = True
        file_id: int = 0
        for char in self.lines[0]:
            if is_file:
                # when we have a file, add file_id a number of times
                entry = file_id
                file_id += 1
            else:
                # when we don't have a file, add -1 to indicate empty space
                entry = -1
            for _ in range(int(char)):
                self.disk_space.append(entry)
            is_file = not is_file

    def compact_disk_space(self):
        insert_pos: int = 0
        while True:
            # update insert_pos
            while self.disk_space[insert_pos] != -1:
                insert_pos += 1
                # also check if we have reached EOD (end-of-diskspace)
                if insert_pos >= len(self.disk_space):
                    return
            # add file at insert pos
            while self.disk_space[-1] == -1:
                self.disk_space.pop()
                # also check if we have reached EOD (end-of-diskspace)
                if insert_pos >= len(self.disk_space):
                    return
            self.disk_space[insert_pos] = self.disk_space.pop()
            # increment insert_pos
            insert_pos += 1
            # check if we have reached EOD (end-of-diskspace)
            if insert_pos >= len(self.disk_space):
                return

    def calculate_checksum(self) -> int:
        checksum: int = 0
        for index, file_id in enumerate(self.disk_space):
            checksum += index * file_id
        return checksum

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
