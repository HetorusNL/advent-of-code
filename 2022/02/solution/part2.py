from pathlib import Path


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.total_score: int = 0
        for line in self.lines:
            opponent, target_match_result = line.split(" ")
            own: str = self.get_own_play(target_match_result, opponent)
            score: int = self.get_self_play_points(own) + self.get_match_points(target_match_result)
            self.total_score += score

    def get_match_points(self, target_match_result: str) -> int:
        match target_match_result:
            case "X":
                return 0
            case "Y":
                return 3
            case "Z":
                return 6

    def get_own_play(self, target_match_result: str, opponent: str) -> str:
        match target_match_result:
            case "X":
                match opponent:
                    case "A":
                        return "Z"
                    case "B":
                        return "X"
                    case "C":
                        return "Y"
            case "Y":
                match opponent:
                    case "A":
                        return "X"
                    case "B":
                        return "Y"
                    case "C":
                        return "Z"
            case "Z":
                match opponent:
                    case "A":
                        return "Y"
                    case "B":
                        return "Z"
                    case "C":
                        return "X"
        raise ValueError(f"invalid input target_match_result {target_match_result} and opponent {opponent}")

    def get_self_play_points(self, own) -> int:
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
