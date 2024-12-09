from pathlib import Path


class Part2:
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
        last_file_pos: int = len(self.disk_space) - 1
        # get the highest file_id
        offset = 0
        while self.disk_space[last_file_pos - offset] == -1:
            offset += 1
        file_id_to_move = self.disk_space[last_file_pos - offset]
        # loop to move all files
        while True:
            # skip to the file we need to move
            while self.disk_space[last_file_pos] != file_id_to_move:
                last_file_pos -= 1
            # check file size
            file_size: int = 0
            while self.disk_space[last_file_pos - file_size] == file_id_to_move:
                file_size += 1

            # loop through the disk_space and find continuous free space blocks
            insert_pos: int = 0
            file_processed: bool = False
            file_moved: bool = False
            while True:
                # skip files at the insert_pos
                while self.disk_space[insert_pos] != -1:
                    insert_pos += 1
                    # also check if we have reached last_file_pos
                    if insert_pos >= last_file_pos:
                        # break from the inner loop to try and move the next file
                        file_processed = True
                        break
                if file_processed:
                    break
                # check free space
                free_space: int = 0
                while self.disk_space[insert_pos + free_space] == -1:
                    free_space += 1
                    # also check if we have reached last_file_pos
                    if insert_pos >= last_file_pos:
                        # break from the inner loop to try and move the next file
                        file_processed = True
                        break
                if file_processed:
                    break
                # check that we can move
                if file_size <= free_space:
                    # we can move the file! move file_size blocks
                    for i in range(file_size):
                        # add file to the insert position
                        self.disk_space[insert_pos + i] = file_id_to_move
                        # remove file at the last_file_pos
                        self.disk_space[last_file_pos - i] = -1
                    # decrement last_file_pos
                    last_file_pos -= file_size
                    file_id_to_move -= 1
                    file_moved = True
                    if file_id_to_move == 0:
                        return
                # when moved, continue the outer loop try and move the next file
                if file_moved:
                    break
                # increment insert_pos
                insert_pos += free_space
            # check that the file is moved, then we successfully move the file
            if file_moved:
                continue
            # failed to move this file, go to the next file
            last_file_pos -= file_size
            file_id_to_move -= 1
            if file_id_to_move == 0:
                return

    def calculate_checksum(self) -> int:
        checksum: int = 0
        for index, file_id in enumerate(self.disk_space):
            if file_id != -1:
                checksum += index * file_id
        return checksum

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
