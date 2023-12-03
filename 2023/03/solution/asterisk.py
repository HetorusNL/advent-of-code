class Asterisk:
    def __init__(self, height: int, pos: int):
        self.height = height
        self.pos = pos
        self.adjecent_numbers: list[int] = []

    def value(self) -> int:
        result = 1
        for number in self.adjecent_numbers:
            result *= number
        return result
