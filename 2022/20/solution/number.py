class Number:
    def __init__(self, value: int, pos: int, size: int):
        self._value: int = value
        self._pos: int = pos
        self._size: int = size

    @property
    def pos(self) -> int:
        return self._pos

    @pos.setter
    def pos(self, _pos: int):
        self._pos: int = _pos

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, _value: int):
        self._value: int = _value

    def pos_up(self) -> None:
        # push the value 1 position further in the list
        self.pos += 1
        # handle overflow at the end if moved
        if self.pos >= self._size:
            self.pos -= self._size

    def pos_down(self) -> None:
        # pull the value 1 position closer in the list
        self.pos -= 1
        # handle overflow at the beginning if moved
        if self.pos < 0:
            self.pos += self._size

    def calculate_move(self) -> tuple[str, dict[int, bool]]:
        """returns direction the _other_ numbers should be moved in, inverse of the move this number will make
        and the list of positions that should move"""
        distance = self.distance
        if distance > 0:
            # check for overflow
            if self.pos + distance >= self._size:
                overflow = self.pos + distance - self._size
                # return from 1 pos further until the end, and the overflow (range=end+1)
                return (
                    "down",
                    {pos: True for pos in range(self.pos + 1, self._size)}
                    | {pos: True for pos in range(overflow + 1)},
                )
            else:
                # return from 1 pos further until the distance (range=end+1)
                return ("down", {pos: True for pos in range(self.pos + 1, self.pos + 1 + distance)})
        else:  # distance is negative
            # we can _add_ the distance, as the distance is negative
            # check for overflow
            if self.pos + distance < 0:
                start_pos = self.pos + distance + self._size
                # return from 0 to 1 pos lower, and the overflow (range=end+1)
                return (
                    "up",
                    {pos: True for pos in range(self.pos)} | {pos: True for pos in range(start_pos, self._size)},
                )
            else:
                # return from 1 pos lower (range=lower+1) till distance lower
                return ("up", {pos: True for pos in range(self.pos + distance, self.pos)})

    def do_move(self) -> None:
        distance = self.distance
        if distance > 0:
            # update own pos with distance
            self.pos += distance
            if self.pos >= self._size:
                self.pos -= self._size
        else:  # distance is negative
            # we can _add_ the distance, as the distance is negative
            # update own pos with distance
            self.pos += distance
            if self.pos < 0:
                self.pos += self._size

    @property
    def distance(self) -> int:
        sign = 1 if self._value >= 0 else -1
        # make sure to do modulo of size-1 as number itself shouldn't be accounted for
        abs_distance = abs(self._value) % (self._size - 1)
        return abs_distance * sign
