class Cube:
    def __init__(self, x: int, y: int, z: int):
        self._x: int = x
        self._y: int = y
        self._z: int = z
        self._exposed_sides: int = -1

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def z(self) -> int:
        return self._z

    @property
    def pos(self) -> str:
        return f"[{self.x}, {self.y}, {self.z}]"

    @property
    def sides(self) -> list["Cube"]:
        return [
            Cube(self.x - 1, self.y, self.z),
            Cube(self.x + 1, self.y, self.z),
            Cube(self.x, self.y - 1, self.z),
            Cube(self.x, self.y + 1, self.z),
            Cube(self.x, self.y, self.z - 1),
            Cube(self.x, self.y, self.z + 1),
        ]

    @property
    def exposed_sides(self) -> int:
        assert self._exposed_sides != -1
        return self._exposed_sides

    @exposed_sides.setter
    def exposed_sides(self, _exposed_sides: int):
        self._exposed_sides = _exposed_sides
