from pathlib import Path


class Part1:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]
        self.cubes = {"red": 12, "green": 13, "blue": 14}

    def solve(self) -> None:
        print("solving...")
        self.possible_games = 0
        for line in self.lines:
            game_id, games = line.split(":")
            game_id = int(game_id.split(" ")[1].strip())
            game_list = games.split(";")
            if self.game_list_possible(game_list):
                self.possible_games += game_id

    def game_list_possible(self, game_list: list[str]) -> bool:
        for game in game_list:
            cubes_list = [cube.strip() for cube in game.split(",")]
            for cube in cubes_list:
                num_cubes, cube_type = cube.split(" ")
                if int(num_cubes) > self.cubes[cube_type]:
                    return False
        return True

    def get_result(self) -> str:
        return f"the result of part 1 is: {self.possible_games}"
