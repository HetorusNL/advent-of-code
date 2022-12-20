from solution.blueprint import Blueprint


class RobotFactory:
    def __init__(self, lines: list[str]):
        self._blueprints: list[Blueprint] = []
        for line in lines:
            self._blueprints.append(Blueprint(line))

    def run_for_minutes(self, minutes: int) -> int:
        quality_level: int = 0
        for blueprint in self._blueprints:
            print(f"running blueprint {blueprint._id}")
            quality_level += blueprint._id * self._run_blueprint_for_minutes(blueprint, minutes)
        return quality_level

    def _run_blueprint_for_minutes(self, blueprint: Blueprint, minutes: int) -> int:
        cache: dict[str, bool] = {}
        cache_hits = 0
        parallel_runs: list[Blueprint] = [blueprint]
        for minute in range(minutes):
            new_runs: list[Blueprint] = []
            print(f"minute: {minute}")
            for run in parallel_runs:
                for new_run in self._run_minute(run):
                    if new_run.hash() in cache:
                        cache_hits += 1
                    else:
                        cache[new_run.hash()] = True
                        new_runs.append(new_run)
            parallel_runs = new_runs
            print(f"new blueprints: {len(parallel_runs)} [cache hits: {cache_hits}]")
        return max(blueprint._geode for blueprint in parallel_runs)

    def _run_minute(self, blueprint: Blueprint) -> list[Blueprint]:
        new_blueprints: list[Blueprint] = blueprint.run_minute()
        return new_blueprints
