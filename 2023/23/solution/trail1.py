from solution.pos import Pos


class Trail:
    def __init__(self, initial_pos: Pos, grid: dict[int, dict[int, str]]):
        self.current_pos: Pos = initial_pos
        self.grid: dict[int, dict[int, str]] = grid
        self.max_steps = 0
        self.current_steps = 0

    def run(self, initial_pos: Pos, end_pos: Pos):
        self.end_pos = end_pos
        self.pos_cache: dict[str, bool] = {}
        self.run_move_recurse(initial_pos)
        return self.max_steps

    def run_move_recurse(self, current_pos: Pos):
        pos_to_move_to: list[tuple[int, Pos]] = []
        result = self.can_reach_pos(current_pos.row + 1, current_pos.col)
        if result[1]:
            pos_to_move_to.append(result)  # type:ignore
        result = self.can_reach_pos(current_pos.row - 1, current_pos.col)
        if result[1]:
            pos_to_move_to.append(result)  # type:ignore
        result = self.can_reach_pos(current_pos.row, current_pos.col + 1)
        if result[1]:
            pos_to_move_to.append(result)  # type:ignore
        result = self.can_reach_pos(current_pos.row, current_pos.col - 1)
        if result[1]:
            pos_to_move_to.append(result)  # type:ignore

        for steps, pos in pos_to_move_to:
            # ignore moves to positions we've already been to
            if self.pos_cache.get(pos.hash()):
                continue
            # if the end_pos is found, stop this recursion
            if pos == self.end_pos:
                steps_till_end_pos = self.current_steps + steps
                self.max_steps = max(self.max_steps, steps_till_end_pos)
                continue
            # otherwise recurse into the next move
            self.pos_cache[pos.hash()] = True
            self.current_steps += steps
            self.run_move_recurse(pos)
            self.current_steps -= steps
            self.pos_cache[pos.hash()] = False

    def can_reach_pos(self, row: int, col: int) -> tuple[int, Pos | None]:
        char = self.grid.get(row, {}).get(col)
        steps = 1
        match char:
            case "v":
                row += 1
                steps += 1
            case "^":
                row -= 1
                steps += 1
            case "<":
                col -= 1
                steps += 1
            case ">":
                col += 1
                steps += 1
            case "#":
                return 1, None
            case None:
                return 1, None
        return steps, Pos(row, col)

    def __repr__(self):
        return str(self.grid)
