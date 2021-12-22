from score import Score
from typing import Dict


class Universe:
    def __init__(self, pos):
        self.pos = pos
        self.scores: Dict[int, Score] = {}

    def with_hash(self):
        return hash(f"{self.pos}"), self
