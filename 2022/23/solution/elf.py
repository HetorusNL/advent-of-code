class Elf:
    def __init__(self, x: int, y: int):
        self._x: int = x
        self._y: int = y

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, _x) -> None:
        self._x = _x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, _y) -> None:
        self._y = _y

    @property
    def pos(self) -> str:
        return f"[{self.x}, {self.y}]"

    @property
    def pos_north(self) -> list[str]:
        return [
            f"[{self.x}, {self.y-1}]",  # N
            f"[{self.x+1}, {self.y-1}]",  # NE
            f"[{self.x-1}, {self.y-1}]",  # NW
        ]

    @property
    def pos_south(self) -> list[str]:
        return [
            f"[{self.x}, {self.y+1}]",  # S
            f"[{self.x+1}, {self.y+1}]",  # SE
            f"[{self.x-1}, {self.y+1}]",  # SW
        ]

    @property
    def pos_west(self) -> list[str]:
        return [
            f"[{self.x-1}, {self.y}]",  # W
            f"[{self.x-1}, {self.y-1}]",  # NW
            f"[{self.x-1}, {self.y+1}]",  # SW
        ]

    @property
    def pos_east(self) -> list[str]:
        return [
            f"[{self.x+1}, {self.y}]",  # E
            f"[{self.x+1}, {self.y-1}]",  # NE
            f"[{self.x+1}, {self.y+1}]",  # SE
        ]

    @property
    def pos_surrounds(self) -> list[str]:
        return [
            f"[{self.x}, {self.y-1}]",  # N
            f"[{self.x+1}, {self.y-1}]",  # NE
            f"[{self.x+1}, {self.y}]",  # E
            f"[{self.x+1}, {self.y+1}]",  # SE
            f"[{self.x}, {self.y+1}]",  # S
            f"[{self.x-1}, {self.y+1}]",  # SW
            f"[{self.x-1}, {self.y}]",  # W
            f"[{self.x-1}, {self.y-1}]",  # NW
        ]
