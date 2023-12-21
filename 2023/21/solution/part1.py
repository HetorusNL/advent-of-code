from pathlib import Path

from solution.pos import Pos


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        current_pos: Pos | None = None
        self.walls: dict[str, bool] = {}
        for row_idx, row in enumerate(self.lines):
            for col_idx, col in enumerate(row):
                if col == "#":
                    self.walls[Pos(row_idx, col_idx).hash()] = True
                elif col == "S":
                    assert current_pos is None
                    current_pos = Pos(row_idx, col_idx)
        assert current_pos is not None
        self.reachable_pos: dict[str, bool] = {current_pos.hash(): True}
        current_positions: dict[str, Pos] = {current_pos.hash(): current_pos}
        steps_to_take = 64
        for step in range(1, steps_to_take + 1):
            self.new_positions: dict[str, Pos] = {}
            for pos in current_positions.values():
                self.process_pos(Pos(pos.row - 1, pos.col))
                self.process_pos(Pos(pos.row + 1, pos.col))
                self.process_pos(Pos(pos.row, pos.col - 1))
                self.process_pos(Pos(pos.row, pos.col + 1))
            if step % 2 == 0:
                for new_pos_hash in self.new_positions:
                    if not self.reachable_pos.get(new_pos_hash):
                        self.reachable_pos[new_pos_hash] = True
            current_positions = self.new_positions
        self.result = len(self.reachable_pos)

    def process_pos(self, pos: Pos):
        if self.walls.get(pos.hash()):
            return
        if self.reachable_pos.get(pos.hash()):
            return
        self.new_positions[pos.hash()] = pos

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
