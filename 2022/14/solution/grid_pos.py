from enum import Enum


class Tile(Enum):
    EMPTY = 1
    ROCK = 2
    SAND = 3


class GridPos:
    def __init__(self, x: int, y: int):
        self._x: int = x
        self._y: int = y
        self._tile: Tile = Tile.EMPTY

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, _x: int):
        self._x: int = _x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, _y: int):
        self._y: int = _y

    @property
    def pos(self) -> str:
        return f"[{self._x}, {self._y}]"

    @property
    def tile(self) -> Tile:
        return self._tile

    @tile.setter
    def tile(self, _tile: Tile) -> None:
        self._tile: Tile = _tile
