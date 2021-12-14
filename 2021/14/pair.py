class Pair:
    def __init__(self, pair, result):
        self.pair = pair
        self.output = [self.pair[0] + result, result + self.pair[1]]
        self.counter = 0

    def step(self):
        return {o: self.counter for o in self.output}

    def add(self, value):
        self.counter += value
