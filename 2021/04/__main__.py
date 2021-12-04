import copy
from board import Board


class Solution:
    def __init__(self):
        with open("input.txt") as f:
            _input = [a.strip() for a in f.readlines()]
        self._bingo_numbers = _input[0].split(",")
        self._boards = []
        current_board = []
        for line in _input[2:]:
            if line == "":
                if current_board:
                    self._boards.append(Board(current_board))
                current_board = []
            else:
                current_board.append(line.split())

        if current_board:
            self._boards.append(Board(current_board))

    def solve(self):
        self.part_1(copy.deepcopy(self._boards))
        self.part_2(copy.deepcopy(self._boards))

    def part_1(self, boards):
        for number in self._bingo_numbers:
            for board in boards:
                board.mark_number(number)
                if board.has_bingo():
                    print(f"bingo board score: {board.get_score(number)}")
                    return

    def part_2(self, boards):
        boards_left = boards
        last_board = boards_left[-1]
        for number in self._bingo_numbers:
            for board in boards_left:
                board.mark_number(number)
                if not board.has_bingo():
                    last_board = board
            boards_left = [
                board for board in boards_left if not board.has_bingo()
            ]

            if len(boards_left) == 0:
                break
        print(f"last bingo board score: {last_board.get_score(number)}")


if __name__ == "__main__":
    Solution().solve()
