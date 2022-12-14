from solution.grid_pos import GridPos
from solution.grid_pos import Tile


class Grid:
    def __init__(self, lines: list[str]):
        self._grid: dict[str, GridPos] = {}
        for line in lines:
            self._process_input_line(line)
        self._depth: int = max(grid_pos.y for grid_pos in self._grid.values())
        self._floor = self._depth + 1

    def do_sand_part_1(self):
        sand = GridPos(500, 0)
        while sand.y <= self._depth:
            # check if sand can fall 1 tile down
            if self._get_pos(sand.x, sand.y + 1).tile == Tile.EMPTY:
                sand.y += 1
            # check if sand can fall 1 tile down and 1 to the left
            elif self._get_pos(sand.x - 1, sand.y + 1).tile == Tile.EMPTY:
                sand.x -= 1
                sand.y += 1
            # check if sand can fall 1 tile down and 1 to the right
            elif self._get_pos(sand.x + 1, sand.y + 1).tile == Tile.EMPTY:
                sand.x += 1
                sand.y += 1
            # otherwise it's blocked, add sand to the grid and start a new sand
            else:
                self._get_pos(sand.x, sand.y).tile = Tile.SAND
                sand = GridPos(500, 0)

    def do_sand_part_2(self):
        sand = GridPos(500, 0)
        while True:
            # if we're at the floor, add sand to the grid and start a new sand
            if sand.y == self._floor:
                self._get_pos(sand.x, sand.y).tile = Tile.SAND
                sand = GridPos(500, 0)
            # check if sand can fall 1 tile down
            if self._get_pos(sand.x, sand.y + 1).tile == Tile.EMPTY:
                sand.y += 1
            # check if sand can fall 1 tile down and 1 to the left
            elif self._get_pos(sand.x - 1, sand.y + 1).tile == Tile.EMPTY:
                sand.x -= 1
                sand.y += 1
            # check if sand can fall 1 tile down and 1 to the right
            elif self._get_pos(sand.x + 1, sand.y + 1).tile == Tile.EMPTY:
                sand.x += 1
                sand.y += 1
            # otherwise it's blocked, add sand
            else:
                self._get_pos(sand.x, sand.y).tile = Tile.SAND
                # if we're blocked at the sand generator pos, stop generating
                if sand.y == 0:
                    break
                # if we're blocked at a different location, start a new sand
                sand = GridPos(500, 0)

    def get_num_sand_units(self) -> int:
        return sum(grid_pos.tile == Tile.SAND for grid_pos in self._grid.values())

    def _process_input_line(self, line: str):
        coords = [coord.strip().split(",") for coord in line.split("->")]
        coords = [list(map(int, coord)) for coord in coords]
        for start_idx in range(len(coords) - 1):
            end_idx = start_idx + 1
            self._create_rock_line(coords[start_idx], coords[end_idx])

    def _create_rock_line(self, start_coord: list[int], end_coord: list[int]):
        startx, starty = start_coord
        endx, endy = end_coord
        # assert that one and only one of the x and y values is different
        assert startx == endx or starty == endy, f"invalid input {start_coord} and {end_coord}"
        assert startx != endx or starty != endy, f"invalid input {start_coord} and {end_coord}"
        # check if a horizontal line should be made
        if startx != endx:
            for x in range(min(startx, endx), max(startx, endx) + 1):
                self._get_pos(x, starty).tile = Tile.ROCK
        if starty != endy:
            for y in range(min(starty, endy), max(starty, endy) + 1):
                self._get_pos(startx, y).tile = Tile.ROCK

    def _get_pos(self, x: int, y: int) -> GridPos:
        try:
            return self._grid[GridPos(x, y).pos]
        except:
            grid_pos = GridPos(x, y)
            self._grid[grid_pos.pos] = grid_pos
            return self._grid[grid_pos.pos]
