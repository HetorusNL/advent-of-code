from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def parse_input(self):
        self.sorting_order: dict[int, list[int]] = {}
        self.update_row: list[list[int]] = []
        # first create a list of sortable numbers, sorting order and the update rows
        for line in self.lines:
            if "|" in line:
                # add the sorting order to the dict
                left, right = list(map(int, line.split("|")))
                if left not in self.sorting_order:
                    self.sorting_order[left] = [right]
                else:
                    self.sorting_order[left].append(right)
            elif "," in line:
                # add the update row to the list
                self.update_row.append(list(map(int, line.split(","))))

    def solve(self) -> None:
        print("solving...")
        self.parse_input()
        self.result = 0
        for row in self.update_row:
            in_order = True
            for index in range(len(row) - 1):
                for entry_index in range(len(row)):
                    if entry_index < index:
                        # entry_index may not be in the sorting order of index
                        if row[index] in self.sorting_order:
                            if row[entry_index] in self.sorting_order[row[index]]:
                                in_order = False
                    elif entry_index > index:
                        # index may not be in the sorting order of entry_index
                        if row[entry_index] in self.sorting_order:
                            if row[index] in self.sorting_order[row[entry_index]]:
                                in_order = False
            if in_order:
                # row in order, add the center element to the result
                self.result += row[len(row) // 2]

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
