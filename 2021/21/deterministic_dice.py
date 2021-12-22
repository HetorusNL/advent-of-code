class DeterministicDice:
    def __init__(self):
        self.next_value = 1
        self.rolls = 0

    def get(self):
        value = self.next_value
        self.rolls += 1
        self.next_value = ((self.next_value) % 100) + 1
        return value
