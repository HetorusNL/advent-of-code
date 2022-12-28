class Blizzard:
    def __init__(self, x: int, y: int, direction: str, width: int, height: int):
        self._x: int = x
        self._y: int = y
        self._direction: str = direction
        self._width: int = width
        self._height: int = height

    def update(self) -> None:
        match self._direction:
            case ">":
                self._x = (self._x + 1) % self._width
            case "<":
                self._x = (self._x - 1) % self._width
            case "^":
                self._y = (self._y - 1) % self._height
            case "v":
                self._y = (self._y + 1) % self._height

    @property
    def pos(self):
        return f"[{self._x}, {self._y}]"

    @property
    def direction(self):
        return self._direction
