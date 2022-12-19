import sys

from solution.cube import Cube


class Grid:
    def __init__(self, lines: list[str]):
        self._grid: dict[str, Cube] = {}
        for line in lines:
            cube = Cube(*[int(pos) for pos in line.split(",")])
            self._grid[cube.pos] = cube
        self._min_x = min(cube.x for cube in self._grid.values())
        self._max_x = max(cube.x for cube in self._grid.values())
        self._min_y = min(cube.y for cube in self._grid.values())
        self._max_y = max(cube.y for cube in self._grid.values())
        self._min_z = min(cube.z for cube in self._grid.values())
        self._max_z = max(cube.z for cube in self._grid.values())
        # caches all known exterior cubes of the droplet
        self._outside_cache: dict[str, bool] = {}
        # caches all the known air pocket cubes inside of the droplet
        self._inside_cache: dict[str, bool] = {}
        # ensure that we can recurse the entire droplet surrounding cube
        sys.setrecursionlimit((self._max_x - self._min_x) * (self._max_y - self._min_y) * (self._max_z - self._min_z))

    def get_exposed_sides(self) -> int:
        for cube in self._grid.values():
            cube.exposed_sides = sum(side.pos not in self._grid for side in cube.sides)
        return sum(cube.exposed_sides for cube in self._grid.values())

    def get_exposed_exterior_sides(self) -> int:
        exposed_exterior_sides: int = 0
        for cube in self._grid.values():
            for side in cube.sides:
                if side.pos not in self._grid:
                    if side.pos in self._outside_cache:
                        exposed_exterior_sides += 1
                    elif side.pos not in self._inside_cache:
                        if self._recurse_cube(side, {side.pos: True}):
                            exposed_exterior_sides += 1
        return exposed_exterior_sides

    def _recurse_cube(self, cube: Cube, sides_checked: dict[str, bool] = {}):
        initial_call = len(sides_checked) == 1
        if cube.pos in self._outside_cache:
            self._add_to_outside_cache(sides_checked)
            return True
        for side in cube.sides:
            if side.pos not in self._grid:
                if side.pos not in sides_checked:
                    # check if the side is outside the droplet, then recursively return True
                    if self._outside_droplet(side):
                        self._add_to_outside_cache(sides_checked)
                        return True
                    sides_checked[side.pos] = True
                    # if a nested recurse returned True, cascade it further
                    if self._recurse_cube(side, sides_checked):
                        return True
        # if it's the initial call and we didn't find the outside of the cube, add to inside cache
        if initial_call:
            self._add_to_inside_cache(sides_checked)
        # if we didn't find a side outside the droplet, return False
        return False

    def _outside_droplet(self, cube: Cube) -> bool:
        return any(
            [
                cube.x <= self._min_x,
                cube.x >= self._max_x,
                cube.y <= self._min_y,
                cube.y >= self._max_y,
                cube.z <= self._min_z,
                cube.z >= self._max_z,
            ]
        )

    def _add_to_outside_cache(self, sides_checked: dict[str, bool]):
        for side_checked in sides_checked:
            self._outside_cache[side_checked] = True

    def _add_to_inside_cache(self, sides_checked: dict[str, bool]):
        for side_checked in sides_checked:
            self._inside_cache[side_checked] = True
