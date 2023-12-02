from pathlib import Path


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.game_power = 0
        for line in self.lines:
            game_id, games = line.split(":")
            game_id = int(game_id.split(" ")[1].strip())
            game_list = games.split(";")
            self.game_power += self.get_game_power(game_list)

    def get_game_power(self, game_list: list[str]) -> int:
        cubes_required = {"red": 0, "green": 0, "blue": 0}
        for game in game_list:
            cubes_list = [cube.strip() for cube in game.split(",")]
            for cube in cubes_list:
                num_cubes, cube_type = cube.split(" ")
                cubes_required[cube_type] = max(cubes_required[cube_type], int(num_cubes))
        game_power = 1
        for cube_required in cubes_required.values():
            game_power *= cube_required
        return game_power

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.game_power}"
