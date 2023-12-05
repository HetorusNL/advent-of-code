class MapValue:
    def __init__(self, dst: int, src: int, length: int):
        self.dst = dst
        self.src = src
        self.length = length

    def is_in(self, value: int):
        return value >= self.src and value < self.src + self.length

    def get_mapped_value(self, value: int):
        if self.is_in(value):
            return self.dst + (value - self.src)
        else:
            return value

    def values_left(self, value: int):
        return self.length - (value - self.src)
