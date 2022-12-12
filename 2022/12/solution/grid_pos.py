class GridPos:
    def __init__(self, x: int, y: int):
        self._x: int = x
        self._y: int = y
        self._height: int = -1
        self._num_steps: int = -1

    def __eq__(self, other: "GridPos"):
        """calculate whether the coordinates of the grid pos are equal"""
        return self._x == other._x and self._y == other._y

    def __gt__(self, other: "GridPos"):
        """return whether the num_steps of self is greater then other"""
        return self._num_steps > other._num_steps

    def __lt__(self, other: "GridPos"):
        """return whether the num_steps of self is less then other"""
        return self._num_steps < other._num_steps

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def pos(self) -> str:
        return f"[{self._x}, {self._y}]"

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, _height) -> None:
        self._height: int = _height

    @property
    def num_steps(self) -> int:
        return self._num_steps

    @num_steps.setter
    def num_steps(self, _num_steps) -> None:
        self._num_steps = _num_steps
