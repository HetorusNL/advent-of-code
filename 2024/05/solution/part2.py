from pathlib import Path


class Part2:
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

            # skip the rows already in order for this part
            if in_order:
                continue

            # this row is not in order, order the list
            has_ordered = True
            # use a loop for potential multi-pass ordering
            while has_ordered:
                has_ordered = False
                # loop through all positions in the row
                for index in range(len(row)):
                    # loop through all numbers before the index
                    for before in row[:index]:
                        # if the index position is in the sorting order
                        if row[index] in self.sorting_order:
                            # if the before number is in the sorting order
                            if before in self.sorting_order[row[index]]:
                                # insert before at the index position
                                row.insert(row.index(before), row.pop(index))
                                has_ordered = True
            # row in order, add the center element to the result
            self.result += row[len(row) // 2]

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
