from solution.multi_state import MultiState
from solution.tunnel import Tunnel
from solution.valve import Valve


class VolcanoElephant:
    def __init__(self, lines: list[str]):
        self._valves: list[Valve] = []
        # construct the valves from the input lines
        for line in lines:
            self._valves.append(Valve(line))
        # link the valves and tunnels together
        for valve in self._valves:
            for tunnel_name in valve.original_tunnel_names:
                valve.add_tunnel(Tunnel([valve.name, tunnel_name], self._get_valve(tunnel_name)))

        self._num_valves_to_open = len([valve for valve in self._valves if valve.flow_rate > 0])
        state = MultiState(0, (self._get_valve("AA"), self._get_valve("AA")), [], 0)
        self._states: dict[int, dict[str, MultiState]] = {0: {state.hash(): state}}
        self._cache_hits: int = 0
        self._estimated_min_pressure: float = -100

        # prune parameters
        self._prune_offset: float = -100
        self._prune_factor: float = 1.01
        self._pre_prune_factor: float = 1.0

    def run_for_minutes(self, minutes: int):
        for minute in range(minutes):
            self._run_minute(minute, minutes)
            self._do_prune(minute + 1)
            # remove the past minute results
            del self._states[minute]

    def max_pressure_released_for_minute(self, minute: int):
        pressures = [state.pressure for state in self._states.get(minute, {}).values()] or [0]
        max_pressure = max(pressures)
        return max_pressure

    def _run_minute(self, minute: int, minutes: int):
        # print(
        #     f"running minute: {minute} with states: {len(self._states.get(minute,{}))} "
        #     f"[ cache hits: {self._cache_hits} ]"
        # )
        for state in self._states.get(minute, {}).values():
            # check if all valves are open, then we can jump to max minutes
            if len(state.open_valves) == self._num_valves_to_open:
                new_pressure = state.pressure_after(minutes - minute)
                self._add_state(minutes, MultiState(new_pressure, state.valves, state.open_valves, state.flow_rate))
                continue

            # first process all possibilites to open the valves
            if state.can_open_valve(0):
                if state.can_open_valve(1) and state.valves[0] != state.valves[1]:
                    # open both valves
                    new_pressure = state.pressure_after(1)
                    new_open_valves = [*state.open_valves, *state.valves]
                    new_state = MultiState(
                        new_pressure,
                        state.valves,
                        new_open_valves,
                        state.flow_rate + state.valves[0].flow_rate + state.valves[1].flow_rate,
                    )
                    self._add_state(minute + 1, new_state)
                else:
                    # open only valve 0 and traverse all valve 1 tunnels
                    for tunnel in state.valves[1].tunnels:
                        new_pressure = state.pressure_after(1)
                        new_open_valves = [*state.open_valves, state.valves[0]]
                        new_state = MultiState(
                            new_pressure,
                            (state.valves[0], tunnel.valve),
                            new_open_valves,
                            state.flow_rate + state.valves[0].flow_rate,
                        )
                        self._add_state(minute + 1, new_state)
            else:
                if state.can_open_valve(1):
                    # open only valve 1 and traverse all valve 0 tunnels
                    for tunnel in state.valves[0].tunnels:
                        new_pressure = state.pressure_after(1)
                        new_open_valves = [*state.open_valves, state.valves[1]]
                        new_state = MultiState(
                            new_pressure,
                            (state.valves[1], tunnel.valve),
                            new_open_valves,
                            state.flow_rate + state.valves[1].flow_rate,
                        )
                        self._add_state(minute + 1, new_state)

            for tunnel0 in state.valves[0].tunnels:
                for tunnel1 in state.valves[1].tunnels:
                    new_pressure = state.pressure_after(1)
                    new_state = MultiState(
                        new_pressure, (tunnel0.valve, tunnel1.valve), state.open_valves, state.flow_rate
                    )
                    self._add_state(minute + 1, new_state)

    def _do_prune(self, minute):
        current_max_pressure = max(state.pressure for state in self._states[minute].values())
        # keep the top-most states (with starting-offset)
        minimal_pressure = current_max_pressure * self._prune_factor + self._prune_offset
        len_before = len(self._states[minute])
        self._states[minute] = {k: v for k, v in self._states[minute].items() if v.pressure >= minimal_pressure}
        len_after = len(self._states[minute])
        self._cache_hits += len_before - len_after

        # pre-prune for the next minute
        estimated_flow_rate = max(state.flow_rate for state in self._states[minute].values())
        self._estimated_min_pressure = minimal_pressure + estimated_flow_rate * self._pre_prune_factor

    def _add_state(self, minute: int, state: MultiState):
        # pre-prune check
        if state.pressure < self._estimated_min_pressure:
            self._cache_hits += 1
            return

        state_hash = state.hash()

        # if all valves are open, don't store copies anymore, only store highest pressure
        if len(state.open_valves) == self._num_valves_to_open:
            state_hash = "all"

        try:
            if state_hash in self._states[minute]:
                # test if we have a lesser state
                if state <= self._states[minute][state_hash]:
                    # found an equal state or lesser state, cache hit
                    self._cache_hits += 1
                    return
            self._states[minute][state_hash] = state
        except KeyError:
            self._states[minute] = {state_hash: state}

    def _get_valve(self, name: str) -> Valve:
        for valve in self._valves:
            if valve.name == name:
                return valve
        raise AssertionError(f"valve with name {name} is unknown!")
