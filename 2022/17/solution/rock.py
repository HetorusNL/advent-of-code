class Rock:
    def __init__(self, rock_pos: list[list[int]]):
        self._rock_pos: list[list[int]] = rock_pos
        self._x_offset: int = 2  # the x-offset is always 2 from the left side

    def set_offset(self, offset) -> None:
        for pos in self._rock_pos:
            # add the x offset to the rock x-coordinate
            pos[0] += self._x_offset
            # add the offset to the y-coordinate of the rock
            pos[1] += offset

    @property
    def rock_pos(self) -> list[list[int]]:
        return self._rock_pos

    def move_left(self) -> None:
        for pos in self._rock_pos:
            # moving left means subtracting 1 from the x-coordinate
            pos[0] -= 1

    def move_right(self) -> None:
        for pos in self._rock_pos:
            # moving right means adding 1 to the x-coordinate
            pos[0] += 1

    def move_down(self) -> None:
        for pos in self._rock_pos:
            # moving down means subtracting 1 from the y-coordinate
            pos[1] -= 1
