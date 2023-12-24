from solution.cube import Cube


class Brick:
    def __init__(
        self,
        line: str,
        bricks: list["Brick"],
        space: dict[int, dict[int, dict[int, "Brick"]]],
        fallen_space: dict[int, dict[int, dict[int, "Brick"]]],
    ) -> None:
        self.bricks: list[Brick] = bricks
        self.space: dict[int, dict[int, dict[int, Brick]]] = space
        self.fallen_space: dict[int, dict[int, dict[int, Brick]]] = fallen_space
        self.brick_id = len(self.bricks)
        self.has_fallen = False
        end_1, end_2 = line.split("~")
        x1, y1, z1 = map(int, end_1.split(","))
        x2, y2, z2 = map(int, end_2.split(","))
        self.cubes: list[Cube] = []
        self.bricks_above_cache: None | list[Brick] = None
        self.bricks_below_cache: None | list[Brick] = None
        if x1 != x2:
            assert y1 == y2 and z1 == z2
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.cubes.append(Cube(x, y1, z1))
        elif y1 != y2:
            assert x1 == x2 and z1 == z2
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.cubes.append(Cube(x1, y, z1))
        elif z1 != z2:
            assert x1 == x2 and y1 == y2
            for z in range(min(z1, z2), max(z1, z2) + 1):
                self.cubes.append(Cube(x1, y1, z))
        else:
            assert x1 == x2 and y1 == y2 and z1 == z2
            self.cubes.append(Cube(x1, y1, z1))
        for cube in self.cubes:
            if cube.x not in self.space:
                self.space[cube.x] = {}
            if cube.y not in self.space[cube.x]:
                self.space[cube.x][cube.y] = {}
            assert cube.z not in self.space[cube.x][cube.y]
            self.space[cube.x][cube.y][cube.z] = self
        assert self.cubes

    def fall(self):
        if self.has_fallen:
            return

        for brick_below in self.bricks_below():
            assert brick_below != self
            brick_below.fall()

        # all bricks below have fallen, fall to the lowest position possible
        new_cubes: list[Cube] = []
        # if brick is horizontal (single z layer)
        if len(set(cube.z for cube in self.cubes)) == 1:
            highest_z = -1  # no brick below
            for z in range(self.cubes[0].z - 1, -1, -1):
                for cube in self.cubes:
                    if self.fallen_space.get(cube.x, {}).get(cube.y, {}).get(z):
                        highest_z = z
                        break
                if highest_z > 0:
                    break
            for cube in self.cubes:
                new_cube_z = highest_z + 1
                if cube.x not in self.fallen_space:
                    self.fallen_space[cube.x] = {}
                if cube.y not in self.fallen_space[cube.x]:
                    self.fallen_space[cube.x][cube.y] = {}
                assert (
                    self.fallen_space[cube.x][cube.y].get(cube.z) is None
                    or self.fallen_space[cube.x][cube.y][cube.z] == self
                )
                self.fallen_space[cube.x][cube.y][new_cube_z] = self
                new_cubes.append(Cube(cube.x, cube.y, new_cube_z))
        # otherwise the brick is vertical
        else:
            x = self.cubes[0].x
            y = self.cubes[0].y
            min_z = min(cube.z for cube in self.cubes)
            for z in range(min_z - 1, -2, -1):  # iterate till z=-1 and place on z=0 then
                if self.fallen_space.get(x, {}).get(y, {}).get(z) is not None or z < 0:
                    for brick_num in range(len(self.cubes)):
                        new_cube_z = z + brick_num + 1
                        if x not in self.fallen_space:
                            self.fallen_space[x] = {}
                        if y not in self.fallen_space[x]:
                            self.fallen_space[x][y] = {}
                        assert (
                            self.fallen_space[x][y].get(new_cube_z) is None
                            or self.fallen_space[x][y][new_cube_z] == self
                        )
                        self.fallen_space[x][y][new_cube_z] = self
                        new_cubes.append(Cube(x, y, new_cube_z))
                    break
        assert len(new_cubes) == len(self.cubes)
        self.cubes = new_cubes
        self.has_fallen = True

    def bricks_below(self) -> list["Brick"]:
        _bricks_below: list[Brick] = []
        # if brick is horizontal (single z layer)
        if len(set(cube.z for cube in self.cubes)) == 1:
            for z in range(self.cubes[0].z - 1, -1, -1):
                for cube in self.cubes:
                    if brick := self.space.get(cube.x, {}).get(cube.y, {}).get(z):
                        _bricks_below.append(brick)
        # otherwise the brick is vertical
        else:
            x = self.cubes[0].x
            y = self.cubes[0].y
            min_z = min(cube.z for cube in self.cubes)
            for z in range(min_z - 1, -1, -1):
                if brick := self.space.get(x, {}).get(y, {}).get(z):
                    _bricks_below.append(brick)
        return _bricks_below

    def bricks_that_fall_on_disintegration(self) -> int:
        self.fallen_bricks: dict[int, Brick] = {self.brick_id: self}
        self.brick_recurse(self)
        return len(self.fallen_bricks) - 1  # ignore the brick that is disintegrated

    def brick_recurse(self, brick: "Brick"):
        bricks_to_recurse_into: dict[int, Brick] = {}
        for brick_directly_above in brick.bricks_directly_above():
            if all(brick.brick_id in self.fallen_bricks for brick in brick_directly_above.bricks_directly_below()):
                self.fallen_bricks[brick_directly_above.brick_id] = brick_directly_above
                bricks_to_recurse_into[brick_directly_above.brick_id] = brick_directly_above
        for _, new_brick in bricks_to_recurse_into.items():
            self.brick_recurse(new_brick)

    def can_disintegrate(self) -> bool:
        bricks_directly_below = len(self.bricks_directly_below())
        assert bricks_directly_below > 0 or min(cube.z for cube in self.cubes) == 0
        _bricks_directly_above = self.bricks_directly_above()
        if len(_bricks_directly_above) == 0:
            return True
        for brick in _bricks_directly_above:
            if len(brick.bricks_directly_below()) < 2:
                return False
        return True

    def bricks_directly_above(self) -> list["Brick"]:
        if self.bricks_above_cache is None:
            # if brick is horizontal (single z layer)
            if len(set(cube.z for cube in self.cubes)) == 1:
                _bricks_directly_above: list[Brick] = []
                for cube in self.cubes:
                    if brick := self.fallen_space.get(cube.x, {}).get(cube.y, {}).get(cube.z + 1):
                        _bricks_directly_above.append(brick)
                self.bricks_above_cache = list(set(_bricks_directly_above))
            else:
                # otherwise the brick is vertical
                x = self.cubes[0].x
                y = self.cubes[0].y
                max_z = max(cube.z for cube in self.cubes)
                if brick := self.fallen_space.get(x, {}).get(y, {}).get(max_z + 1):
                    self.bricks_above_cache = [brick]
                else:
                    self.bricks_above_cache = []
        return self.bricks_above_cache

    def bricks_directly_below(self) -> list["Brick"]:
        if self.bricks_below_cache is None:
            # if brick is horizontal (single z layer)
            if len(set(cube.z for cube in self.cubes)) == 1:
                _bricks_directly_below: list[Brick] = []
                for cube in self.cubes:
                    if brick := self.fallen_space.get(cube.x, {}).get(cube.y, {}).get(cube.z - 1):
                        _bricks_directly_below.append(brick)
                self.bricks_below_cache = list(set(_bricks_directly_below))
            else:
                # otherwise the brick is vertical
                x = self.cubes[0].x
                y = self.cubes[0].y
                min_z = min(cube.z for cube in self.cubes)
                if brick := self.fallen_space.get(x, {}).get(y, {}).get(min_z - 1):
                    self.bricks_below_cache = [brick]
                else:
                    self.bricks_below_cache = []
        return self.bricks_below_cache

    def __repr__(self) -> str:
        return str(self.cubes)

    def __eq__(self, other: "Brick"):
        return self.brick_id == other.brick_id

    def __hash__(self) -> int:
        return self.brick_id
