from pathlib import Path

from solution.connection import Connection
from solution.pos import Pos


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.height = len(self.lines)
        self.width = len(self.lines[0])
        self.connections = {
            "|": [Connection(0, -1), Connection(0, 1)],
            "-": [Connection(1, 0), Connection(-1, 0)],
            "L": [Connection(0, -1), Connection(1, 0)],
            "J": [Connection(0, -1), Connection(-1, 0)],
            "7": [Connection(0, 1), Connection(-1, 0)],
            "F": [Connection(0, 1), Connection(1, 0)],
            ".": [],
        }

    def solve(self) -> None:
        print("solving...")
        pos_list = self.find_tube()
        self.result = len(pos_list) // 2

    def find_tube(self):
        pos_list: list[Pos] = self.get_start_pos()
        first_pos = pos_list[0]
        while True:
            cur_pos = pos_list[-1]
            connections = self.connections[self.get_pos_char(cur_pos)]
            for connection in connections:
                if cur_pos.move(connection) == first_pos and len(pos_list) > 2:
                    return pos_list
            if cur_pos.move(connections[0]) == pos_list[-2]:
                pos_list.append(cur_pos.move(connections[1]))
            else:
                pos_list.append(cur_pos.move(connections[0]))

    def get_start_pos(self) -> list[Pos]:
        s_pos = None
        for line_idx, line in enumerate(self.lines):
            if "S" in line:
                s_pos = Pos(line.index("S"), line_idx)
                break
        assert s_pos

        if self.get_pos_char(Pos(s_pos.x, s_pos.y - 1)) in "|7F":
            return [s_pos, Pos(s_pos.x, s_pos.y - 1)]
        if self.get_pos_char(Pos(s_pos.x, s_pos.y + 1)) in "|LJ":
            return [s_pos, Pos(s_pos.x, s_pos.y + 1)]
        if self.get_pos_char(Pos(s_pos.x - 1, s_pos.y)) in "-LF":
            return [s_pos, Pos(s_pos.x - 1, s_pos.y)]
        if self.get_pos_char(Pos(s_pos.x + 1, s_pos.y)) in "-J7":
            return [s_pos, Pos(s_pos.x + 1, s_pos.y)]
        assert False

    def get_pos_char(self, pos: Pos) -> str:
        if pos.y < 0 or pos.x < 0 or pos.y >= len(self.lines) or pos.x >= len(self.lines[0]):
            return "."
        return self.lines[pos.y][pos.x]

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.result}"
