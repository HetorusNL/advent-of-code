class SeedRange:
    def __init__(self, start: int, length: int):
        self.start = start
        self.length = length
        self.value = start

    def next(self):
        return self.value

    def skip_to_after(self, value):
        self.value = value + 1

    def is_done(self):
        return self.value >= self.start + self.length

    def values_left(self):
        return self.length - (self.value - self.start)
