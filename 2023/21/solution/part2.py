from pathlib import Path

from solution.pos import Pos


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.lines = [
            "...........",
            ".....###.#.",
            ".###.##..#.",
            "..#.#...#..",
            "....#.#....",
            ".##..S####.",
            ".##..#...#.",
            ".......##..",
            ".##.#.####.",
            ".##..##.##.",
            "...........",
        ]

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        self.start_pos: Pos | None = None
        self.walls: dict[str, bool] = {}
        self.width = len(self.lines)
        self.height = len(self.lines[0])
        for row_idx, row in enumerate(self.lines):
            for col_idx, col in enumerate(row):
                if col == "#":
                    self.walls[Pos(row_idx, col_idx).hash()] = True
                elif col == "S":
                    assert self.start_pos is None
                    self.start_pos = Pos(row_idx, col_idx)
        assert self.start_pos
        # add a wall all around the field
        for row_idx in range(-1, self.height + 1):
            self.walls[Pos(row_idx, -1).hash()] = True
            self.walls[Pos(row_idx, self.height).hash()] = True
        for col_idx in range(-1, self.width + 1):
            self.walls[Pos(-1, col_idx).hash()] = True
            self.walls[Pos(self.width, col_idx).hash()] = True
        for row_idx in range(-2, self.height + 2):
            for col_idx in range(-2, self.height + 2):
                if self.walls.get(Pos(row_idx, col_idx).hash()):
                    print("#", end="")
                else:
                    print(".", end="")
            print()
        self.process_for_pos(self.start_pos, 20)

    def process_for_pos(self, input_pos: Pos, steps_to_take: int):
        self.reachable_pos: dict[str, int] = {input_pos.hash(): 0}
        current_positions: dict[str, Pos] = {input_pos.hash(): input_pos}
        for step in range(1, steps_to_take + 1):
            self.new_positions: dict[str, Pos] = {}
            for pos in current_positions.values():
                self.process_pos(Pos(pos.row - 1, pos.col))
                self.process_pos(Pos(pos.row + 1, pos.col))
                self.process_pos(Pos(pos.row, pos.col - 1))
                self.process_pos(Pos(pos.row, pos.col + 1))
            # if step % 2 == 0:
            for new_pos_hash in self.new_positions:
                if not self.reachable_pos.get(new_pos_hash):
                    self.reachable_pos[new_pos_hash] = step
            current_positions = self.new_positions
        print(len(self.reachable_pos))
        for row_idx in range(-2, self.height + 2):
            for col_idx in range(-2, self.height + 2):
                pos_hash = Pos(row_idx, col_idx).hash()
                if self.walls.get(pos_hash):
                    print("###", end="")
                elif self.reachable_pos.get(pos_hash):
                    print(f"{self.reachable_pos[pos_hash]:3}", end="")
                else:
                    print("...", end="")
            print()

    def process_pos(self, pos: Pos):
        if self.walls.get(pos.hash()):
            return
        if self.reachable_pos.get(pos.hash()):
            return
        self.new_positions[pos.hash()] = pos

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
