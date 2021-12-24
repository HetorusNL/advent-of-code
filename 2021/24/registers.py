from typing import List


class Registers:
    def __init__(self):
        reg_names = "wxyz"
        self.reg = {reg_names[index]: 0 for index in range(len(reg_names))}
        self.inputs: List[int] = []

    def get(self, reg_name: str):
        assert reg_name in self.reg
        return self.reg[reg_name]

    def set(self, reg_name: str, value: int):
        assert reg_name in self.reg
        self.reg[reg_name] = value

    def get_input(self):
        if self.inputs:
            return self.inputs.pop(0)
        else:
            print("no inputs left, enter manually")
            return int(input("> "))

    def add_input(self, value: int):
        assert value is not None
        self.inputs.append(value)
        return self
