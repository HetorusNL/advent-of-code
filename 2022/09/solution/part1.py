from pathlib import Path

from solution.playfield import Playfield


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.length = 2
        playfield = Playfield(self.length)
        playfield.simulate(self.lines)
        self.num_visited_tail_positions = playfield.get_num_visited_tail_positions()

    def get_result(self) -> str:
        result = f"the tail of the rope (length {self.length}) visited this num of positions: "
        result += f"{self.num_visited_tail_positions}"
        return result
