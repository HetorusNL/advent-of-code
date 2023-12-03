from solution.asterisk import Asterisk
from solution.number import Number


class Grid:
    def __init__(self, lines: list[str]):
        self.lines = lines
        self.numbers: list[Number] = []
        self.asterisks: list[Asterisk] = []
        self.width = len(lines[0])
        self.height = len(lines)
        for line_idx, line in enumerate(lines):
            is_number = False
            start = -1
            value = ""
            for pos_idx, pos in enumerate(line):
                if pos == "*":
                    self.asterisks.append(Asterisk(line_idx, pos_idx))
                if self.pos_is_number(pos):
                    if not is_number:
                        start = pos_idx
                    is_number = True
                    value += pos
                if not self.pos_is_number(pos):
                    if is_number:
                        self.numbers.append(Number(int(value), line_idx, start, len(value)))
                        is_number = False
                        value = ""
            if is_number:
                self.numbers.append(Number(int(value), line_idx, start, len(value)))

    def pos_is_number(self, pos):
        return pos in "0123456789"

    def numbers_adjecent_to_symbols(self) -> list[int]:
        adjecent_to_symbols = []
        for number in self.numbers:
            if self.is_adjecent_to_symbols(number):
                adjecent_to_symbols.append(number.value)
        return adjecent_to_symbols

    def is_adjecent_to_symbols(self, number: Number):
        number_height = number.height
        for pos in range(number.start, number.start + number.length):
            if self.pos_is_symbol(number_height - 1, pos):
                return True
            if self.pos_is_symbol(number_height - 1, pos - 1):
                return True
            if self.pos_is_symbol(number_height - 1, pos + 1):
                return True
            if self.pos_is_symbol(number_height + 1, pos):
                return True
            if self.pos_is_symbol(number_height + 1, pos - 1):
                return True
            if self.pos_is_symbol(number_height + 1, pos + 1):
                return True
            if self.pos_is_symbol(number_height, pos - 1):
                return True
            if self.pos_is_symbol(number_height, pos + 1):
                return True
        return False

    def pos_is_symbol(self, y, x):
        if y == -1:
            return False
        if y == self.height:
            return False
        if x == -1:
            return False
        if x == self.width:
            return False
        if self.lines[y][x] == ".":
            return False
        if self.pos_is_number(self.lines[y][x]):
            return False
        return True

    def get_gears(self):
        for number in self.numbers:
            self.check_number_with_asterisks(number)
        gears = filter(lambda asterisk: len(asterisk.adjecent_numbers) == 2, self.asterisks)
        return gears

    def check_number_with_asterisks(self, number: Number):
        number_height = number.height
        asterisks: list[Asterisk] = []
        for pos in range(number.start, number.start + number.length):
            asterisks.extend(self.check_pos_with_asterisks(number_height - 1, pos))
            asterisks.extend(self.check_pos_with_asterisks(number_height - 1, pos - 1))
            asterisks.extend(self.check_pos_with_asterisks(number_height - 1, pos + 1))
            asterisks.extend(self.check_pos_with_asterisks(number_height + 1, pos))
            asterisks.extend(self.check_pos_with_asterisks(number_height + 1, pos - 1))
            asterisks.extend(self.check_pos_with_asterisks(number_height + 1, pos + 1))
            asterisks.extend(self.check_pos_with_asterisks(number_height, pos - 1))
            asterisks.extend(self.check_pos_with_asterisks(number_height, pos + 1))
        for asterisk in set(asterisks):
            asterisk.adjecent_numbers.append(number.value)

    def check_pos_with_asterisks(self, y, x):
        asterisks: list[Asterisk] = list(
            filter(lambda asterisk: asterisk.height == y and asterisk.pos == x, self.asterisks)
        )
        assert len(asterisks) in [0, 1]
        return asterisks
