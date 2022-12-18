from solution.valve import Valve


class Volcano:
    def __init__(self, lines: list[str]):
        self._valves: list[Valve] = []
        # construct the valves from the input lines
        for line in lines:
            self._valves.append(Valve(line))
        # link the valves and tunnels together
        for valve in self._valves:
            for tunnel_name in valve.tunnel_names:
                valve.add_tunnel(self.get_valve(tunnel_name))
        self._cache: dict[str, dict[int, int]] = {}
        self._valves_to_open: int = len([valve for valve in self._valves if valve.flow_rate])

    def get_valve(self, name: str) -> Valve:
        for valve in self._valves:
            if valve.name == name:
                return valve
        raise AssertionError(f"valve with name {name} is unknown!")

    def run_for_minutes(self, minutes: int) -> int:
        self._num_minutes: int = minutes
        self._run_minute(1, "AA", 0, [])
        return max(max(minute.values()) for minute in self._cache.values())

    def run_with_elephant(self, minutes: int) -> int:
        self._num_minutes: int = minutes
        self._run_elephant_minute(1, ["AA", "AA"], 0, [])
        return max(max(minute.values()) for minute in self._cache.values())

    def _run_minute(self, minute: int, location: str, pressure_released: int, open_valves: list["Valve"]) -> None:
        # check cache
        cache_key = f"[{location}, {[open_valve.name for open_valve in open_valves]}]"
        if cache_key in self._cache:
            minute_entry = self._cache[cache_key].get(minute)
            if minute_entry:
                if minute_entry > pressure_released:
                    return
            if any(value == pressure_released for value in self._cache[cache_key].values()):
                return
            for cache_minute in self._cache[cache_key]:
                if cache_minute < minute:
                    if self._cache[cache_key][cache_minute] > pressure_released:
                        return
        else:
            self._cache[cache_key] = {}
        self._cache[cache_key][minute] = pressure_released

        # stop after num minutes
        if minute > self._num_minutes:
            return

        # calculate pressure_released when all valves are open
        if len([open_valve.name for open_valve in open_valves]) == self._valves_to_open:
            step_flow_rate = sum(open_valve.flow_rate for open_valve in open_valves)
            num_minutes_left = self._num_minutes - minute + 1
            pressure_after_num_minutes = pressure_released + num_minutes_left * step_flow_rate
            self._cache[cache_key][self._num_minutes] = pressure_after_num_minutes
            return

        # process the current state for this minute
        step_flow_rate = sum(open_valve.flow_rate for open_valve in open_valves)
        pressure_released_after_this_minute = pressure_released + step_flow_rate
        # open a valve if the valve is not yet opened
        valve = self.get_valve(location)
        if valve not in open_valves and valve.flow_rate:
            self._run_minute(minute + 1, location, pressure_released_after_this_minute, [*open_valves, valve])

        # for all tunnels travel through them
        for tunnel in valve.tunnels:
            self._run_minute(minute + 1, tunnel.name, pressure_released_after_this_minute, open_valves)

    def _run_elephant_minute(
        self, minute: int, locations: list[str], pressure_released: int, open_valves: list["Valve"]
    ) -> None:
        if minute > 3 and pressure_released == 0:
            return
        assert len(set(open_valves)) == len(open_valves), [valve.name for valve in open_valves]
        # check cache
        cache_key = f"[{locations}, {[open_valve.name for open_valve in open_valves]}]"
        if cache_key in self._cache:
            minute_entry = self._cache[cache_key].get(minute)
            if minute_entry:
                if minute_entry > pressure_released:
                    return
            for _minute, value in enumerate(self._cache[cache_key]):
                if value == pressure_released and _minute < minute:
                    return
            for cache_minute in self._cache[cache_key]:
                if cache_minute < minute:
                    if self._cache[cache_key][cache_minute] > pressure_released:
                        return
        else:
            self._cache[cache_key] = {}
        self._cache[cache_key][minute] = pressure_released

        # stop after num minutes
        if minute > self._num_minutes:
            return

        # calculate pressure_released when all valves are open
        if len([open_valve.name for open_valve in open_valves]) == self._valves_to_open:
            step_flow_rate = sum(open_valve.flow_rate for open_valve in open_valves)
            num_minutes_left = self._num_minutes - minute + 1
            pressure_after_num_minutes = pressure_released + num_minutes_left * step_flow_rate
            self._cache[cache_key][self._num_minutes] = pressure_after_num_minutes
            return
        elif minute > 12:
            # all valves should be open after 14 minutes, stop otherwise
            return

        # process the current state for this minute
        step_flow_rate = sum(open_valve.flow_rate for open_valve in open_valves)
        pressure_released_after_this_minute = pressure_released + step_flow_rate
        # check if both can open the valve
        valve0 = self.get_valve(locations[0])
        valve1 = self.get_valve(locations[1])
        if valve0 not in open_valves and valve0.flow_rate:
            if valve1 not in open_valves and valve1.flow_rate:
                if valve0.name != valve1.name:
                    valves = [*open_valves, valve0, valve1]
                    assert len(set(valves)) == len(valves), [valve.name for valve in valves]
                    self._run_elephant_minute(
                        minute + 1,
                        [locations[0], locations[1]],
                        pressure_released_after_this_minute,
                        [*open_valves, valve0, valve1],
                    )
                else:
                    for tunnel in valve1.tunnels:
                        valves = [*open_valves, valve0]
                        assert len(set(valves)) == len(valves), [valve.name for valve in valves]
                        self._run_elephant_minute(
                            minute + 1,
                            sorted([tunnel.name, locations[0]]),
                            pressure_released_after_this_minute,
                            [*open_valves, valve0],
                        )
            else:
                for tunnel in valve1.tunnels:
                    valves = [*open_valves, valve0]
                    assert len(set(valves)) == len(valves), [valve.name for valve in valves]
                    self._run_elephant_minute(
                        minute + 1,
                        sorted([tunnel.name, locations[0]]),
                        pressure_released_after_this_minute,
                        [*open_valves, valve0],
                    )
        if valve1 not in open_valves and valve1.flow_rate:
            if valve0 in open_valves or not valve0.flow_rate:
                for tunnel in valve0.tunnels:
                    valves = [*open_valves, valve1]
                    assert len(set(valves)) == len(valves), [valve.name for valve in valves]
                    self._run_elephant_minute(
                        minute + 1,
                        sorted([tunnel.name, locations[1]]),
                        pressure_released_after_this_minute,
                        [*open_valves, valve1],
                    )
        for tunnel0 in valve0.tunnels:
            for tunnel1 in valve1.tunnels:
                valves = [*open_valves]
                assert len(set(valves)) == len(valves), [valve.name for valve in valves]
                self._run_elephant_minute(
                    minute + 1,
                    sorted([tunnel0.name, tunnel1.name]),
                    pressure_released_after_this_minute,
                    open_valves,
                )
