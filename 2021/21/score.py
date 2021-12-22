class Score:
    def __init__(self, score):
        self.score = score
        self.count = 0

    def add_count(self, count):
        self.count += count
        return self

    def with_hash(self):
        return hash(f"{self.score}"), self
