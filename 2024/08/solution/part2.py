from pathlib import Path


class Pos:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}]"

    def __eq__(self, other: "object"):
        assert type(other) == Pos
        return self.x == other.x and self.y == other.y


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.width: int = len(self.lines[0])
        self.height: int = len(self.lines)

        self.antennas: dict[str, list[Pos]] = {}
        for row_idx, row in enumerate(self.lines):
            for col_idx, col in enumerate(row):
                if col != ".":
                    pos = Pos(col_idx, self.height - row_idx - 1)
                    if col not in self.antennas:
                        self.antennas[col] = []
                    self.antennas[col].append(pos)

    def is_outside(self, pos: Pos):
        # return whether we're outside of the antenna grid
        if pos.x < 0 or pos.x >= self.width:
            return True
        if pos.y < 0 or pos.y >= self.height:
            return True

    def add_antinode(self, char: str, antinode: Pos):
        # make sure the antinode is not ouside of the map
        if self.is_outside(antinode):
            return
        # otherwise, add the antinode to the collection
        if char not in self.antinodes:
            self.antinodes[char] = {}
        self.antinodes[char][str(antinode)] = antinode

    def solve(self) -> None:
        print("solving...")
        self.antinodes: dict[str, dict[str, Pos]] = {}
        for frequency_char, frequency_antennas in self.antennas.items():
            # iterate through all antennas
            for first_idx, first_pos in enumerate(frequency_antennas):
                # iterate from first_idx onward to find the second of the pair
                for second_pos in frequency_antennas[first_idx + 1 :]:
                    # calculate dx and dy to get to the antinodes
                    dx = second_pos.x - first_pos.x
                    dy = second_pos.y - first_pos.y
                    # add antinode on both antennas
                    self.add_antinode(frequency_char, first_pos)
                    self.add_antinode(frequency_char, second_pos)
                    # start creating resonant harmonics antinodes in one direction
                    _dx: int = 0
                    _dy: int = 0
                    while True:
                        _dx += dx
                        _dy += dy
                        antinode1 = Pos(second_pos.x + _dx, second_pos.y + _dy)
                        if self.is_outside(antinode1):
                            break
                        self.add_antinode(frequency_char, antinode1)
                    # start creating resonant harmonics antinodes in other direction
                    _dx: int = 0
                    _dy: int = 0
                    while True:
                        _dx -= dx
                        _dy -= dy
                        antinode2 = Pos(first_pos.x + _dx, first_pos.y + _dy)
                        if self.is_outside(antinode2):
                            break
                        self.add_antinode(frequency_char, antinode2)
        # extract a list of unique antinodes coords by taking a set of them
        antinodes_coord_list: list[str] = []
        for char_antinodes in self.antinodes.values():
            antinodes_coord_list.extend(char_antinodes.keys())
        self.result = len(set(antinodes_coord_list))
        # self.plot_antinodes_grid()

    def plot_antinodes_grid(self):
        # loop through the grid in left-bottom origin manner
        for row_idx in range(self.height - 1, -1, -1):
            for col_idx in range(self.width):
                # if there is an antinode, draw antinode
                for char, char_antinodes in self.antinodes.items():
                    if any(Pos(col_idx, row_idx) == node for node in char_antinodes.values()):
                        print("#", end="")
                        break
                else:
                    # if there is no antinode, but is an antenna, draw antenna
                    for char, antennas in self.antennas.items():
                        if any(Pos(col_idx, row_idx) == antenna for antenna in antennas):
                            print(char, end="")
                            break
                    else:
                        # if there is no antinode and antenna, draw dot
                        print(".", end="")
            print()

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
