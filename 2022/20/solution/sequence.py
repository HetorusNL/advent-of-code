from solution.number import Number


class Sequence:
    def __init__(self, lines: list[str]):
        self._sequence: dict[int, Number] = {}
        size: int = len(lines)
        for idx, line in enumerate(lines):
            self._sequence[idx] = Number(int(line), idx, size)

    def decrypted_mixing(self) -> None:
        decryption_key = 811589153
        num_mixings = 10
        for _, number in self._sequence.items():
            number.value *= decryption_key

        for mixing_num in range(num_mixings):
            print(f"running mixing [ {mixing_num + 1} / {num_mixings} ]")
            self.mixing()

    def mixing(self) -> None:
        for idx in range(len(self._sequence)):
            if idx % 1000 == 0:
                print(f"decrypting [ {idx + 1} / {len(self._sequence)} ]")
            # calculate what the move of this number means for the other numbers in the sequence
            direction, positions_to_move = self._sequence[idx].calculate_move()
            direction: str
            positions_to_move: dict[int, bool]
            # convert to dict for a major speedup
            sequence_numbers: list[Number] = [
                number for number in self._sequence.values() if number.pos in positions_to_move
            ]
            # perform the up/down move of the other numbers
            match direction:
                case "up":
                    for sequence_number in sequence_numbers:
                        sequence_number.pos_up()
                case "down":
                    for sequence_number in sequence_numbers:
                        sequence_number.pos_down()
            # finally perform the move of this number
            self._sequence[idx].do_move()

    def get_grove_coordinates(self) -> int:
        grove_coordinates: int = 0
        # get the position of the '0'
        _values: list[int] = [number.pos for number in self._sequence.values() if number.value == 0]
        assert len(_values) == 1
        pos_of_0 = _values[0]
        # for all numbers after 0, get the value at target_pos handling overflow if needed
        for number_after_0 in [1000, 2000, 3000]:
            target_pos = (pos_of_0 + number_after_0) % len(self._sequence)
            _values: list[int] = [number.value for number in self._sequence.values() if number.pos == target_pos]
            assert len(_values) == 1
            # grove coordinates is the sum of the numbers after 0
            grove_coordinates += _values[0]
        return grove_coordinates
