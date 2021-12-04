class Board:
    def __init__(self, board_list):
        self._board = board_list
        self._board_marked = []
        for line in self._board:
            d = {val: False for val in line}
            self._board_marked.append(d)

    def mark_number(self, number):
        for line in self._board_marked:
            if number in line.keys():
                line[number] = True

    def has_bingo(self):
        # check for line bingo
        for line_idx in range(len(self._board)):
            numbers_marked = sum(
                self._board_marked[line_idx][num]
                for num in self._board[line_idx]
            )
            if numbers_marked == len(self._board[0]):
                return True
        # check for row bingo
        for row_idx in range(len(self._board[0])):
            numbers_marked = 0
            for line_idx in range(len(self._board)):
                numbers_marked += self._board_marked[line_idx][
                    self._board[line_idx][row_idx]
                ]
            if numbers_marked == len(self._board[0]):
                return True
        # no horizontal and vertical bingo
        return False

    def get_score(self, called_number):
        unmarked_numbers_sum = 0
        for line_idx in range(len(self._board)):
            unmarked_numbers_sum += sum(
                int(num) if self._board_marked[line_idx][num] == False else 0
                for num in self._board[line_idx]
            )
        return unmarked_numbers_sum * int(called_number)
