from deterministic_dice import DeterministicDice
from dirac_dice import DiracDice
from universe import Universe
from score import Score
from player import Player
import re
from typing import Dict
from typing import List


class Solution:
    def __init__(self):
        self._reset_input()

    def _reset_input(self):
        with open("input.txt") as f:
            lines = [line.strip() for line in f.readlines()]

        self.players: List[Player] = []

        for line in lines:
            regexp = (
                r"Player (?P<num>[0-9]*) starting position:"
                r" (?P<pos>[0-9]*)"
            )
            match = re.match(regexp, line).groupdict()
            self.players.append(Player(int(match["num"]), int(match["pos"])))

    def solve(self):
        self.part_1()
        self._reset_input()
        self.part_2()

    def part_1(self):
        dice = DeterministicDice()
        num_players = len(self.players)
        current_player = 0
        while True:
            player = self.players[current_player % num_players]
            score = sum(dice.get() for _ in range(3))
            player.move(score)
            if player.score >= 1000:
                loser = self.players[(current_player + 1) % num_players]
                final_score = loser.score * dice.rolls
                print(f"loser score time number of dice rolls: {final_score}")
                return
            current_player += 1

    def part_2(self):
        dice = DiracDice()
        universe_h, universe = Universe([8, 6]).with_hash()
        score_h, score = Score([0, 0]).add_count(1).with_hash()
        universe.scores[score_h] = score
        universes = {universe_h: universe}

        total_wins = [0, 0]
        player = 0
        while len(universes):
            opponent = abs(1 - player)
            new_univs: Dict[int, Universe] = {}
            for dice_result, dice_count in dice.get().items():
                for universe in universes.values():
                    pos = [0, 0]
                    pos[player] = (
                        universe.pos[player] + dice_result - 1
                    ) % 10 + 1
                    pos[opponent] = universe.pos[opponent]
                    n_univ_h, new_universe = Universe(pos).with_hash()
                    for pos_score in universe.scores.values():
                        wins = pos_score.count * dice_count
                        score = [0, 0]
                        score[player] = pos_score.score[player] + pos[player]
                        score[opponent] = pos_score.score[opponent]
                        if score[player] > 20:
                            total_wins[player] += wins
                            continue
                        if n_univ_h not in new_univs:
                            new_univs[n_univ_h] = new_universe
                        n_score_h, new_score = Score(score).with_hash()
                        if n_score_h not in new_univs[n_univ_h].scores:
                            new_univs[n_univ_h].scores[n_score_h] = new_score
                        new_univs[n_univ_h].scores[n_score_h].add_count(wins)
            player = opponent
            universes = new_univs

        univs = max(total_wins)
        print(f"number of universes won by the the winning player: {univs}")


if __name__ == "__main__":
    Solution().solve()
