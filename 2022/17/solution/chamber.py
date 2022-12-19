from solution.rocks import Rocks
from solution.rock import Rock


class Chamber:
    def __init__(self, wind: str):
        self._wind: str = wind
        self._wind_index: int = 0
        # self._grid: dict[str, bool] = {f"[{x},-1]": True for x in range(7)}
        self._grid: dict[int, dict[int, bool]] = {-1: {x: True for x in range(7)}}
        self._rocks: Rocks = Rocks()
        self._highest_rock: int = -1
        self._rock_offset: int = 4  # 3 spacing thus 1 higher = 4
        self._most_left_pos: int = 0
        self._most_right_pos: int = 6

    def fall_rock(self) -> Rock:
        rock: Rock = self._rocks.get_rock()
        rock.set_offset(self._highest_rock + self._rock_offset)
        while True:
            # process the jet of hot gass
            match self._wind[self._wind_index]:
                case ">":
                    # verify that we can move the rock to the right
                    for pos in rock.rock_pos:
                        # if it moves into a wall, don't move
                        if pos[0] + 1 > self._most_right_pos:
                            break
                        # if it moves into a rock, don't move
                        if self._pos_has_rock(pos[0] + 1, pos[1]):
                            break
                    else:
                        # if all checks above succeeded, move right
                        rock.move_right()
                case "<":
                    # verify that we can move the rock to the left
                    for pos in rock.rock_pos:
                        # if it moves into a wall, don't move
                        if pos[0] - 1 < self._most_left_pos:
                            break
                        # if it moves into a rock, don't move
                        if self._pos_has_rock(pos[0] - 1, pos[1]):
                            break
                    else:
                        # if all checks above succeeded, move left
                        rock.move_left()
            # increment the wind index with overflow
            self._wind_index = (self._wind_index + 1) % len(self._wind)

            # process the falling down
            # verify that we can move the rock down
            for pos in rock.rock_pos:
                # if it moves into a rock, add to grid and return
                if self._pos_has_rock(pos[0], pos[1] - 1):
                    self._add_rock_to_grid(rock)
                    return rock
            # if all checks above succeeded, move down
            rock.move_down()

    @property
    def num_different_rocks(self) -> int:
        return self._rocks.num_different_rocks

    @property
    def tower_height(self) -> int:
        # return the highest rock index +1 (as a 0-based index is used)
        return self._highest_rock + 1

    def _pos_has_rock(self, x, y) -> bool:
        return bool(self._grid.get(y, {}).get(x))

    def _add_rock_to_grid(self, rock: Rock) -> None:
        for pos in rock.rock_pos:
            if pos[1] not in self._grid:
                self._grid[pos[1]] = {}
            self._grid[pos[1]][pos[0]] = True
            self._highest_rock = max(self._highest_rock, pos[1])

    def print(self) -> None:
        for row in range(self._highest_rock, -1, -1):
            print("|", end="")
            for col in range(self._most_right_pos + 1):
                if self._grid.get(row, {}).get(col):
                    print("#", end="")
                else:
                    print(".", end="")
            print("|")
        print("+-------+")
