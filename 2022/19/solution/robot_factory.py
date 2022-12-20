from solution.blueprint import Blueprint


class RobotFactory:
    def __init__(self, lines: list[str]):
        self._blueprints: list[Blueprint] = []
        for line in lines:
            self._blueprints.append(Blueprint(line))

    def run_for_minutes_part_1(self, minutes: int) -> int:
        results: dict[int, int] = {}
        quality_level: int = 0
        for blueprint in self._blueprints:
            print(f"running blueprint {blueprint._id}")
            result = blueprint.run_for_minutes(minutes)
            results[blueprint._id] = result
            quality_level += blueprint._id * result
        print(results)
        return quality_level

    def run_for_minutes_part_2(self, minutes: int) -> int:
        results: dict[int, int] = {}
        multiplied_geodes: int = 1
        for blueprint in self._blueprints:
            print(f"running blueprint {blueprint._id}")
            result = blueprint.run_for_minutes(minutes)
            results[blueprint._id] = result
            multiplied_geodes *= result
        print(results)
        return multiplied_geodes
