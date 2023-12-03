class Number:
    def __init__(self, value: int, height: int, start: int, length: int):
        self.value = value
        self.height = height
        self.start = start
        self.length = length
        assert self.start != -1
