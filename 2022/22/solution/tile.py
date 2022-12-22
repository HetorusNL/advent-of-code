class Tile:
    def __init__(self, char: str, row: int, col: int):
        self._char: str = char
        self._row: int = row
        self._col: int = col

    @property
    def char(self) -> str:
        return self._char

    @property
    def is_open(self) -> bool:
        return self.char == "."

    @property
    def is_wall(self) -> bool:
        return self.char == "#"

    @property
    def is_present(self) -> bool:
        return self.is_open or self.is_wall

    @property
    def row(self) -> int:
        return self._row

    @row.setter
    def row(self, _row) -> None:
        self._row = _row

    @property
    def col(self) -> int:
        return self._col

    @col.setter
    def col(self, _col) -> None:
        self._col = _col
