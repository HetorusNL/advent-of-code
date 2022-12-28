class GridPos:
    def __init__(self, x: int, y: int):
        self._x: int = x
        self._y: int = y

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, _x: int) -> None:
        self._x = _x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, _y: int) -> None:
        self._y = _y

    @property
    def pos(self) -> str:
        return f"[{self.x}, {self.y}]"

    def __eq__(self, other: "GridPos"):
        return self.x == other.x and self.y == other.y
