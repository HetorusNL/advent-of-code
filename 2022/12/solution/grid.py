import string

from solution.grid_pos import GridPos


class Grid:
    def __init__(self, lines: list[str]):
        self._grid_pos_cache: dict[str, GridPos] = {}
        for line_idx, line in enumerate(lines):
            for pos_idx, pos in enumerate(line):
                grid_pos = GridPos(pos_idx, line_idx)
                try:
                    grid_pos.height = string.ascii_lowercase.index(pos)
                except ValueError:
                    if pos == "S":
                        grid_pos.height = string.ascii_lowercase.index("a")
                        self._start_pos: GridPos = grid_pos
                    elif pos == "E":
                        grid_pos.height = string.ascii_lowercase.index("z")
                        self._end_pos: GridPos = grid_pos
                    else:
                        raise AssertionError(f"invalid char {pos} at pos: [{pos_idx}, {line_idx}]")
                self._grid_pos_cache[grid_pos.pos] = grid_pos
        self._width = max(grid_pos.x for grid_pos in self._grid_pos_cache.values()) + 1
        self._height = max(grid_pos.y for grid_pos in self._grid_pos_cache.values()) + 1
        assert self._start_pos, f"start pos not found!"
        assert self._end_pos, f"end pos not found!"

    def num_steps_till_end(self) -> int:
        return self._solve_grid([self._start_pos])

    def num_steps_till_end_and_find_start_pos(self) -> int:
        start_locations = [grid_pos for grid_pos in self._grid_pos_cache.values() if grid_pos.height == 0]
        return self._solve_grid(start_locations)

    def _solve_grid(self, pos_to_check: list[GridPos]) -> int:
        for pos in pos_to_check:
            pos.num_steps = 0
        while pos_to_check:
            new_pos_to_check: list[GridPos] = []
            for pos in pos_to_check:
                new_pos_to_check.extend(self._check_pos(pos))
            pos_to_check = new_pos_to_check
        # make sure that we found our end
        assert self._end_pos.num_steps != -1, f"failed to find end pos!"
        return self._end_pos.num_steps

    def _check_pos(self, grid_pos: GridPos) -> list[GridPos]:
        new_grid_pos: list[GridPos] = []
        if grid_pos.x > 0:
            grid_pos_left = self._grid_pos_cache[GridPos(grid_pos.x - 1, grid_pos.y).pos]
            if self._check_height_num_steps(grid_pos, grid_pos_left, grid_pos.num_steps + 1):
                new_grid_pos.append(grid_pos_left)
        if grid_pos.x < self._width - 1:
            grid_pos_right = self._grid_pos_cache[GridPos(grid_pos.x + 1, grid_pos.y).pos]
            if self._check_height_num_steps(grid_pos, grid_pos_right, grid_pos.num_steps + 1):
                new_grid_pos.append(grid_pos_right)
        if grid_pos.y > 0:
            grid_pos_up = self._grid_pos_cache[GridPos(grid_pos.x, grid_pos.y - 1).pos]
            if self._check_height_num_steps(grid_pos, grid_pos_up, grid_pos.num_steps + 1):
                new_grid_pos.append(grid_pos_up)
        if grid_pos.y < self._height - 1:
            grid_pos_down = self._grid_pos_cache[GridPos(grid_pos.x, grid_pos.y + 1).pos]
            if self._check_height_num_steps(grid_pos, grid_pos_down, grid_pos.num_steps + 1):
                new_grid_pos.append(grid_pos_down)
        return new_grid_pos

    def _check_height_num_steps(self, grid_pos: GridPos, new_grid_pos: GridPos, num_steps: int):
        if (grid_pos.height + 1) >= new_grid_pos.height:
            if new_grid_pos.num_steps == -1 or num_steps < new_grid_pos.num_steps:
                new_grid_pos.num_steps = num_steps
                return True
        return False
