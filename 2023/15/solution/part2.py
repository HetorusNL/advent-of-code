from pathlib import Path

from solution.lens import Lens


class Part2:
    def __init__(self, file: Path):
        with open(file) as f:
            self.lines = [line.strip() for line in f.readlines()]

    def solve(self) -> None:
        print("solving...")
        self.result = 0
        initialization_sequence = [step.strip() for step in self.lines[0].split(",")]
        boxes: dict[int, list[Lens]] = {value: [] for value in range(256)}
        for step in initialization_sequence:
            if "=" in step:
                label, focal_length_str = step.split("=")
                focal_length: int = int(focal_length_str) if focal_length_str else 0
                hash_value = self.hash_label(label)
                try:
                    index = [lens.label for lens in boxes[hash_value]].index(label)
                    boxes[hash_value][index] = Lens(label, focal_length)
                except:
                    boxes[hash_value].append(Lens(label, focal_length))
            elif "-" in step:
                label = step[:-1]
                hash_value = self.hash_label(label)
                try:
                    index = [lens.label for lens in boxes[hash_value]].index(label)
                    del boxes[hash_value][index]
                except:
                    pass
            else:
                assert False
        for box_idx, box in boxes.items():
            for index, lens in enumerate(box):
                focussing_power = (box_idx + 1) * (index + 1) * lens.focal_length
                self.result += focussing_power

    def hash_label(self, label: str):
        current_value = 0
        for c in label:
            current_value += ord(c)
            current_value *= 17
            current_value %= 256
        return current_value

    def get_result(self) -> str:
        return f"the result of part 2 is: {self.result}"
