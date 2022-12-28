from solution.elf import Elf


class Grid:
    def __init__(self, lines: list[str]):
        self._grid: dict[str, Elf] = {}
        for y, line in enumerate(lines):
            for x, pos in enumerate(line):
                if pos == "#":
                    elf = Elf(x, y)
                    self._grid[elf.pos] = elf

        # _proposed_moves[pos] = [[old_elf, new_elf], ...]
        self._proposed_moves: dict[str, list[list[Elf]]] = {}
        self._direction_list = ["north", "south", "west", "east"]
        self._performed_move: bool = False

    def do_round(self) -> bool:
        self._performed_move = False
        self._propose_moves()
        self._do_moves()
        self._update_direction_list()
        return self._performed_move

    def num_elves(self) -> int:
        min_x = min(elf.x for elf in self._grid.values())
        max_x = max(elf.x for elf in self._grid.values())
        min_y = min(elf.y for elf in self._grid.values())
        max_y = max(elf.y for elf in self._grid.values())
        _num_elves = len(self._grid.values())
        return (max_x + 1 - min_x) * (max_y + 1 - min_y) - _num_elves

    def _propose_moves(self):
        for elf in self._grid.values():
            if all(pos not in self._grid for pos in elf.pos_surrounds):
                self._add_proposed_move(elf.pos, elf, elf)
                continue
            for direction in self._direction_list:
                match direction:
                    case "north":
                        if all(pos not in self._grid for pos in elf.pos_north):
                            new_elf = Elf(elf.x, elf.y - 1)
                            self._add_proposed_move(new_elf.pos, elf, new_elf)
                            break
                    case "south":
                        if all(pos not in self._grid for pos in elf.pos_south):
                            new_elf = Elf(elf.x, elf.y + 1)
                            self._add_proposed_move(new_elf.pos, elf, new_elf)
                            break
                    case "west":
                        if all(pos not in self._grid for pos in elf.pos_west):
                            new_elf = Elf(elf.x - 1, elf.y)
                            self._add_proposed_move(new_elf.pos, elf, new_elf)
                            break
                    case "east":
                        if all(pos not in self._grid for pos in elf.pos_east):
                            new_elf = Elf(elf.x + 1, elf.y)
                            self._add_proposed_move(new_elf.pos, elf, new_elf)
                            break
            else:
                self._add_proposed_move(elf.pos, elf, elf)

    def _add_proposed_move(self, pos: str, elf: Elf, new_elf: Elf):
        if elf != new_elf:
            self._performed_move = True
        if pos not in self._proposed_moves:
            self._proposed_moves[pos] = []
        self._proposed_moves[pos].append([elf, new_elf])

    def _do_moves(self):
        new_grid: dict[str, Elf] = {}
        for elves in self._proposed_moves.values():
            if len(elves) == 1:
                # valid move, as only 1 elf wants to move to this position
                _, new_elf = elves[0]
                new_grid[new_elf.pos] = new_elf
            else:
                # more elves want to move here, leave all elves at their initial position
                for old_elf, _ in elves:
                    new_grid[old_elf.pos] = old_elf
        self._grid = new_grid
        self._proposed_moves = {}

    def _update_direction_list(self):
        # remove first direction and append at the end of the list
        self._direction_list.append(self._direction_list.pop(0))

    def print(self):
        min_x = min(elf.x for elf in self._grid.values())
        max_x = max(elf.x for elf in self._grid.values())
        min_y = min(elf.y for elf in self._grid.values())
        max_y = max(elf.y for elf in self._grid.values())
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                print("#" if self._grid.get(f"[{x}, {y}]") else ".", end="")
            print()
