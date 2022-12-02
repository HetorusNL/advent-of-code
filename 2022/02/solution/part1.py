from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.total_score = 0
        for line in self.lines:
            opponent, own = line.split(" ")
            score = self.get_self_play_points(own) + self.get_match_points(own, opponent)
            self.total_score += score

    def get_match_points(self, own, opponent):
        loss = 0
        draw = 3
        win = 6
        match own:
            case "X":
                match opponent:
                    case "A":
                        return draw
                    case "B":
                        return loss
                    case "C":
                        return win
            case "Y":
                match opponent:
                    case "A":
                        return win
                    case "B":
                        return draw
                    case "C":
                        return loss
            case "Z":
                match opponent:
                    case "A":
                        return loss
                    case "B":
                        return win
                    case "C":
                        return draw
        raise ValueError(f"invalid input own {own} and opponent {opponent}")

    def get_self_play_points(self, own):
        match own:
            case "X":
                return 1
            case "Y":
                return 2
            case "Z":
                return 3
        raise ValueError(f"invalid input own {own}")

    def get_result(self) -> str:
        return f"the score of the rock paper scissors playthrough is: {self.total_score}"
