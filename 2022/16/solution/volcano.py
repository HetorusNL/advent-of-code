from solution.state import State
from solution.tunnel import Tunnel
from solution.valve import Valve


class Volcano:
    def __init__(self, lines: list[str]):
        self._valves: list[Valve] = []
        # construct the valves from the input lines
        for line in lines:
            self._valves.append(Valve(line))
        # link the valves and tunnels together
        for valve in self._valves:
            for tunnel_name in valve.original_tunnel_names:
                valve.add_tunnel(Tunnel([valve.name, tunnel_name], self._get_valve(tunnel_name)))
        self._optimize_tunnels()

        self._num_valves_to_open = len([valve for valve in self._valves if valve.flow_rate > 0])
        state = State(0, self._get_valve("AA"), [])
        self._states: dict[int, dict[str, State]] = {0: {state.hash(): state}}
        self._cache_hits: int = 0

        # prune parameters
        self._prune_offset: float = -100
        self._prune_factor: float = 1.0

    def run_for_minutes(self, minutes: int):
        for minute in range(minutes):
            self._run_minute(minute, minutes)
            self._do_prune(minute + 1)
            # remove the past minute results
            if minute in self._states:
                del self._states[minute]

    def max_pressure_released_for_minute(self, minute: int):
        pressures = [state.pressure for state in self._states.get(minute, {}).values()] or [0]
        return max(pressures)

    def _run_minute(self, minute: int, minutes: int):
        # print(
        #     f"running minute: {minute} with states: {len(self._states.get(minute,{}))} "
        #     f"[ cache hits: {self._cache_hits} ]"
        # )
        for state in self._states.get(minute, {}).values():
            # check if all valves are open, then we can jump to max minutes
            if len(state.open_valves) == self._num_valves_to_open:
                new_pressure = state.pressure_after(minutes - minute)
                self._add_state(minutes, State(new_pressure, state.valve, state.open_valves))
                continue

            # see if we can open the valve
            if state.can_open_valve:
                new_pressure = state.pressure_after(1)
                new_open_valves = [*state.open_valves, state.valve]
                new_state = State(new_pressure, state.valve, new_open_valves)
                self._add_state(minute + 1, new_state)

            # traverse to all tunnels we can
            for tunnel in state.valve.tunnels:
                if minute + tunnel.length > minutes:
                    # we can't reach the end of the tunnel in time, wait here and calculate pressure
                    new_pressure = state.pressure_after(minutes - minute)
                    self._add_state(minutes, State(new_pressure, state.valve, state.open_valves))
                else:
                    # we can reach the end of the tunnel in time, add new state for the end of the tunnel
                    new_pressure = state.pressure_after(tunnel.length)
                    new_state = State(new_pressure, tunnel.valve, state.open_valves)
                    self._add_state(minute + tunnel.length, new_state)

    def _do_prune(self, minute):
        if minute not in self._states:
            return
        current_max_pressure = max(state.pressure for state in self._states[minute].values())
        # keep the top-most states (with starting-offset)
        minimal_pressure = current_max_pressure * self._prune_factor + self._prune_offset
        len_before = len(self._states[minute])
        self._states[minute] = {k: v for k, v in self._states[minute].items() if v.pressure >= minimal_pressure}
        len_after = len(self._states[minute])
        self._cache_hits += len_before - len_after

    def _add_state(self, minute: int, state: State):
        state_hash = state.hash()
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

    def _optimize_tunnels(self) -> None:
        while True:
            # don't optimize the first valve away as it's the start point
            zero_flow_valves = [valve for valve in self._valves[1:] if valve.flow_rate == 0]
            two_connection_valves = [valve for valve in zero_flow_valves if len(valve.tunnels) == 2]
            if not two_connection_valves:
                break
            # optimize one at a time, as other valves change when optimized
            self._optimize_valve_away(two_connection_valves[0])

    def _optimize_valve_away(self, valve_to_remove: Valve):
        connected_valves = [valve for valve in self._valves if valve.name in valve_to_remove.tunnel_names]
        assert len(connected_valves) == 2, [valve.name for valve in connected_valves]
        valves_0_valves: list[str] = connected_valves[0].tunnel(valve_to_remove.name).valves_in_tunnel
        valves_1_valves: list[str] = connected_valves[1].tunnel(valve_to_remove.name).valves_in_tunnel
        total_valves: list[str] = [*valves_0_valves, *valves_1_valves]
        connected_valves[0].add_tunnel(Tunnel(total_valves, connected_valves[1]))
        connected_valves[0].remove_tunnel(valve_to_remove.name)
        connected_valves[1].add_tunnel(Tunnel(total_valves, connected_valves[0]))
        connected_valves[1].remove_tunnel(valve_to_remove.name)
        self._valves.remove(valve_to_remove)
