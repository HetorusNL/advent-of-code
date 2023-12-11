from pathlib import Path


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        # expand columns
        expanded_cols: list[int] = []
        for col_idx in reversed(range(len(self.lines[0]))):
            if all(self.lines[row][col_idx] == "." for row in range(len(self.lines))):
                expanded_cols.append(col_idx)

        # expand rows
        expanded_rows: list[int] = []
        width = len(self.lines[0])
        for row_idx in reversed(range(len(self.lines))):
            if self.lines[row_idx].count(".") == width:
                expanded_rows.append(row_idx)

        # find galaxies
        galaxies: dict[int, list[int]] = {}
        for row_idx, row in enumerate(self.lines):
            for col_idx, col in enumerate(row):
                if col == "#":
                    galaxies[len(galaxies)] = [row_idx, col_idx]

        # iterate galaxies
        EXPAND_FACTOR = 1000000
        shortest_paths: list[int] = []
        for start_galaxy_idx in range(len(galaxies)):
            for end_galaxy_idx in range(start_galaxy_idx + 1, len(galaxies)):
                delta_row = abs(galaxies[start_galaxy_idx][0] - galaxies[end_galaxy_idx][0])
                delta_col = abs(galaxies[start_galaxy_idx][1] - galaxies[end_galaxy_idx][1])
                expanded_rows_cols = 0
                # get expanded rows between galaxies
                lowest_row_idx = min(galaxies[start_galaxy_idx][0], galaxies[end_galaxy_idx][0])
                heighest_row_idx = max(galaxies[start_galaxy_idx][0], galaxies[end_galaxy_idx][0])
                expanded_rows_cols += len(
                    list(
                        filter(lambda row_idx: row_idx > lowest_row_idx and row_idx < heighest_row_idx, expanded_rows)
                    )
                )
                # get expanded rows between galaxies
                lowest_col_idx = min(galaxies[start_galaxy_idx][1], galaxies[end_galaxy_idx][1])
                heighest_col_idx = max(galaxies[start_galaxy_idx][1], galaxies[end_galaxy_idx][1])
                expanded_rows_cols += len(
                    list(
                        filter(lambda col_idx: col_idx > lowest_col_idx and col_idx < heighest_col_idx, expanded_cols)
                    )
                )
                shortest_paths.append(delta_row + delta_col + expanded_rows_cols * EXPAND_FACTOR - expanded_rows_cols)
        self.result = sum(shortest_paths)

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
