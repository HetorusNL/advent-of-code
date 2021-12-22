class DiracDice:
    def __init__(self):
        self.dice_results = {}
        for d1 in range(1, 4):
            for d2 in range(1, 4):
                for d3 in range(1, 4):
                    dr = d1 + d2 + d3
                    if dr not in self.dice_results:
                        self.dice_results[dr] = 0
                    self.dice_results[dr] += 1

    def get(self):
        return self.dice_results
