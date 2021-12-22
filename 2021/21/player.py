class Player:
    def __init__(self, num: int, pos: int):
        self.num = num
        self.pos = pos
        self.score: int = 0

    def move(self, score: int):
        self.pos = (((self.pos + score) - 1) % 10) + 1
        self.score += self.pos
