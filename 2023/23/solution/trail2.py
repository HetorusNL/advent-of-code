import sys

from solution.pos import Pos
from solution.move import Move

sys.setrecursionlimit(10000)


class Trail:
    def __init__(self, initial_pos: Pos, grid: dict[int, dict[int, str]]):
        self.grid: dict[int, dict[int, str]] = grid
        self.max_steps = 0
        # precalculate the grid with valid moves
        self.grid_valid_moves: dict[int, dict[int, list[Pos]]] = {}
        for row in self.grid:
            self.grid_valid_moves[row] = {}
            for col in self.grid[row]:
                self.grid_valid_moves[row][col] = []
                if pos := self.can_reach_pos(row + 1, col):
                    self.grid_valid_moves[row][col].append(pos)
                if pos := self.can_reach_pos(row - 1, col):
                    self.grid_valid_moves[row][col].append(pos)
                if pos := self.can_reach_pos(row, col + 1):
                    self.grid_valid_moves[row][col].append(pos)
                if pos := self.can_reach_pos(row, col - 1):
                    self.grid_valid_moves[row][col].append(pos)

        self.grid_moves: dict[str, list[Move]] = {}
        self.calculate_grid_move(initial_pos)

    def can_reach_pos(self, row: int, col: int) -> Pos | None:
        char = self.grid.get(row, {}).get(col)
        if char is None:
            return None
        if char == "#":
            return None
        return Pos(row, col)

    def calculate_grid_move(self, initial_pos: Pos):
        pos_to_calculate: list[Pos] = [initial_pos]
        calculated_positions: dict[str, bool] = {}
        while pos_to_calculate:
            new_pos_to_calculate: list[Pos] = []
            for pos in pos_to_calculate:
                if pos.hash() in calculated_positions:
                    continue
                calculated_positions[pos.hash()] = True
                cache: dict[str, bool] = {pos.hash(): True}
                current_pos = pos
                for start_pos in self.grid_valid_moves[current_pos.row][current_pos.col]:
                    steps = 0
                    cache[start_pos.hash()] = True
                    current_pos = start_pos
                    while True:
                        steps += 1
                        moves_from_current_pos = self.grid_valid_moves[current_pos.row][current_pos.col]
                        moves_from_current_pos = [move for move in moves_from_current_pos if move.hash() not in cache]
                        if len(moves_from_current_pos) == 0:
                            # found a start or end
                            move = Move(current_pos, steps)
                            if pos.hash() not in self.grid_moves:
                                self.grid_moves[pos.hash()] = []
                            self.grid_moves[pos.hash()].append(move)
                            break
                        elif len(moves_from_current_pos) == 1:
                            # 2 connecting steps, we can move one step further
                            new_pos = moves_from_current_pos[0]
                            if new_pos.hash() not in cache:
                                cache[new_pos.hash()] = True
                                current_pos = new_pos
                            continue
                        elif len(moves_from_current_pos) > 1:
                            # cross section found, create a grid move
                            move = Move(current_pos, steps)
                            if pos.hash() not in self.grid_moves:
                                self.grid_moves[pos.hash()] = []
                            self.grid_moves[pos.hash()].append(move)
                            new_pos_to_calculate.append(current_pos)
                            break
                        assert False
            pos_to_calculate = new_pos_to_calculate

    def run(self, initial_pos: Pos, end_pos: Pos):
        self.end_pos = end_pos
        self.move_cache: dict[str, Move | None] = {initial_pos.hash(): Move(initial_pos, 0)}
        self.run_move_recurse(initial_pos)
        return self.max_steps

    def run_move_recurse(self, current_pos: Pos):
        for move in self.grid_moves[current_pos.hash()]:
            # ignore moves to positions we've already been to
            if self.move_cache.get(move.to_pos.hash()):
                continue
            # if the end_pos is found, stop this recursion
            if move.to_pos == self.end_pos:
                steps = 0
                for cache_entry in self.move_cache.values():
                    if cache_entry:
                        steps += cache_entry.length
                steps += move.length
                self.max_steps = max(self.max_steps, steps)
                continue
            # otherwise recurse into the next move
            self.move_cache[move.to_pos.hash()] = move
            self.run_move_recurse(move.to_pos)
            self.move_cache[move.to_pos.hash()] = None
