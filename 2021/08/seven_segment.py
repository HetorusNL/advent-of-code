class SevenSegment:
    def __init__(self, pattern):
        self.pattern = pattern
        self.numbers = {}
        self._solve()

    def _solve(self):
        # solve for 1 4 7 and 8
        for digit in self.pattern:
            if len(digit) == 2:
                self.numbers[1] = digit
            if len(digit) == 4:
                self.numbers[4] = digit
            if len(digit) == 3:
                self.numbers[7] = digit
            if len(digit) == 7:
                self.numbers[8] = digit
        # solve for 6
        for digit in self.pattern:
            if len(digit) == 6:
                for segment in self.numbers[1]:
                    if segment not in digit:
                        self.numbers[6] = digit
        # solve for 5
        for digit in self.pattern:
            if len(digit) == 5:
                if all(segment in self.numbers[6] for segment in digit):
                    self.numbers[5] = digit
        # solve for 2
        for digit in self.pattern:
            if len(digit) == 5:
                if sum(segment in self.numbers[5] for segment in digit) == 3:
                    self.numbers[2] = digit
        # solve for 3
        for digit in self.pattern:
            if len(digit) == 5:
                if digit != self.numbers[2] and digit != self.numbers[5]:
                    self.numbers[3] = digit
        # solve for 0 and 9
        for digit in self.pattern:
            if len(digit) == 6 and digit != self.numbers[6]:
                if sum(segment in self.numbers[3] for segment in digit) == 5:
                    self.numbers[9] = digit
                else:  # sum(..) == 4
                    self.numbers[0] = digit

    def get_number(self, in_digit):
        for number, digit in self.numbers.items():
            if len(digit) == len(in_digit):  # equal length
                if all(id in digit for id in in_digit):  # all segments match
                    return number
        print(in_digit, self.numbers)
        assert False  # number not found!
