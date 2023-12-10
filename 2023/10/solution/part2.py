from pathlib import Path

from solution.connection import Connection
from solution.pos import Pos


class Part2:
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
        pos_list_dict = {str(pos): pos for pos in pos_list}
        left_pos_list, right_pos_list = self.find_left_right_pos(pos_list)
        left_empty_pos_list = self.get_empty_pos_list(left_pos_list, pos_list_dict)
        right_empty_pos_list = self.get_empty_pos_list(right_pos_list, pos_list_dict)
        assert len(left_empty_pos_list) == 0 or len(right_empty_pos_list) == 0
        self.result = len(left_empty_pos_list) + len(right_empty_pos_list)

    def get_empty_pos_list(self, in_pos_list: dict[str, Pos], pos_list: dict[str, Pos]) -> dict[str, Pos]:
        empty_pos_list: dict[str, Pos] = {}
        for pos_str, pos in in_pos_list.items():
            if pos_str not in pos_list:
                empty_pos_list[pos_str] = pos
        grown_empty_pos_dict = {}
        for empty_pos in empty_pos_list.values():
            grown_pos_list = self.grow_pos(empty_pos, pos_list)
            if not grown_pos_list:
                return {}
            grown_empty_pos_dict = {**grown_empty_pos_dict, **grown_pos_list}
        return grown_empty_pos_dict

    def grow_pos(self, pos: Pos, pos_list: dict[str, Pos]) -> dict[str, Pos]:
        grown_pos_dict = {str(pos): pos}
        next_pos_dict = {str(pos): pos}
        while next_pos_dict:
            new_next_pos_dict = {}
            for pos in next_pos_dict.values():
                potential_next_pos_list = [
                    pos.move(Connection(1, 0)),
                    pos.move(Connection(0, -1)),
                    pos.move(Connection(-1, 0)),
                    pos.move(Connection(0, 1)),
                ]
                for next_pos in potential_next_pos_list:
                    if (
                        next_pos.y < 0
                        or next_pos.x < 0
                        or next_pos.y >= len(self.lines)
                        or next_pos.x >= len(self.lines[0])
                    ):
                        # outside of the map, stop growing
                        return {}
                    next_pos_str = str(next_pos)
                    if next_pos_str not in grown_pos_dict and next_pos_str not in pos_list:
                        new_next_pos_dict[next_pos_str] = next_pos
                        grown_pos_dict[next_pos_str] = next_pos
            next_pos_dict = new_next_pos_dict
        return grown_pos_dict

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

    def find_left_right_pos(self, pos_list: list[Pos]) -> tuple[dict[str, Pos], dict[str, Pos]]:
        left_pos: list[Pos] = []
        right_pos: list[Pos] = []
        for move_idx in range(len(pos_list) - 1):
            start_pos = pos_list[move_idx]
            end_pos = pos_list[move_idx + 1]
            if start_pos.move(Connection(1, 0)) == end_pos:
                # move right
                left_pos.append(start_pos.move(Connection(0, -1)))
                left_pos.append(end_pos.move(Connection(0, -1)))
                right_pos.append(start_pos.move(Connection(0, 1)))
                right_pos.append(end_pos.move(Connection(0, 1)))
            elif start_pos.move(Connection(-1, 0)) == end_pos:
                # move left
                left_pos.append(start_pos.move(Connection(0, 1)))
                left_pos.append(end_pos.move(Connection(0, 1)))
                right_pos.append(start_pos.move(Connection(0, -1)))
                right_pos.append(end_pos.move(Connection(0, -1)))
            elif start_pos.move(Connection(0, -1)) == end_pos:
                # move up
                left_pos.append(start_pos.move(Connection(-1, 0)))
                left_pos.append(end_pos.move(Connection(-1, 0)))
                right_pos.append(start_pos.move(Connection(1, 0)))
                right_pos.append(end_pos.move(Connection(1, 0)))
            elif start_pos.move(Connection(0, 1)) == end_pos:
                # move down
                left_pos.append(start_pos.move(Connection(1, 0)))
                left_pos.append(end_pos.move(Connection(1, 0)))
                right_pos.append(start_pos.move(Connection(-1, 0)))
                right_pos.append(end_pos.move(Connection(-1, 0)))
            else:
                assert False
        left_pos_dict = {str(pos): pos for pos in left_pos}
        right_pos_dict = {str(pos): pos for pos in right_pos}
        return left_pos_dict, right_pos_dict

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
        return f"the result of part 2 is: {self.result}"
