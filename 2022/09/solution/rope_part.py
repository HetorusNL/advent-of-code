class RopePart:
    def __init__(self):
        self._x: int = 0
        self._y: int = 0

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, _x: int):
        self._x = _x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, _y: int):
        self._y = _y

    @property
    def position(self) -> str:
        """returns its coordinate as a string"""
        return f"[{self.x}, {self.y}]"
