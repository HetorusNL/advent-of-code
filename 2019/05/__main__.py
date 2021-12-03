class Instruction(object):
    def __init__(self, computer, opcode):
        self.operations = {
            "01": computer.add,
            "02": computer.mul,
            "03": computer.inp,
            "04": computer.otp,
            "05": computer.jmpt,
            "06": computer.jmpf,
            "07": computer.lt,
            "08": computer.eq,
            "99": computer.term,
        }

        opcode = opcode.zfill(5)
        # print(opcode)  # uncomment this for opcode debug purposes
        self.operation = self.operations[opcode[3:5]]
        self.param1 = opcode[2] != "0"
        self.param2 = opcode[1] != "0"
        self.param3 = opcode[0] != "0"


class Computer(object):
    def __init__(self):
        self.IP = 0

    def run(self, program):
        self.IP = 0  # reset the instruction pointer
        self.program = program  # store the program in the class
        while self.IP < len(self.program):
            # run the instruction at the current IP position
            instruction = Instruction(self, str(self.ld_addr(self.IP)))
            instruction.operation(instruction)

    # execute IP+3 = IP+1 + IP+2
    def add(self, ins):
        param1 = self.ld_addr if ins.param1 else self.ld
        param2 = self.ld_addr if ins.param2 else self.ld
        param3 = self.st_addr if ins.param3 else self.st
        param3(self.IP + 3, param1(self.IP + 1) + param2(self.IP + 2))
        self.IP += 4

    # execute IP+3 = IP+1 * IP+2
    def mul(self, ins):
        param1 = self.ld_addr if ins.param1 else self.ld
        param2 = self.ld_addr if ins.param2 else self.ld
        param3 = self.st_addr if ins.param3 else self.st
        param3(self.IP + 3, param1(self.IP + 1) * param2(self.IP + 2))
        self.IP += 4

    # terminate
    def term(self, ins):
        # terminate by setting the IP to the size of the program
        self.IP = len(self.program)

    # input instruction, st_addr(IP+1, input())
    def inp(self, ins):
        self.st_addr(self.ld_addr(self.IP + 1), int(input(">>> ")))
        self.IP += 2

    # output instruction, print(ld_addr(addr))
    def otp(self, ins):
        param1 = self.ld_addr if ins.param1 else self.ld
        print(param1(self.IP + 1))
        self.IP += 2

    # jump-if-true
    def jmpt(self, ins):
        param1 = self.ld_addr if ins.param1 else self.ld
        param2 = self.ld_addr if ins.param2 else self.ld
        if param1(self.IP + 1):
            self.IP = param2(self.IP + 2)
        else:  # false => no jump
            self.IP += 3

    # jump-if-false
    def jmpf(self, ins):
        param1 = self.ld_addr if ins.param1 else self.ld
        param2 = self.ld_addr if ins.param2 else self.ld
        if not param1(self.IP + 1):
            self.IP = param2(self.IP + 2)
        else:  # true => no jump
            self.IP += 3

    # less than, execute IP+3 = IP+1 < IP+2 ? 1 : 0
    def lt(self, ins):
        param1 = self.ld_addr if ins.param1 else self.ld
        param2 = self.ld_addr if ins.param2 else self.ld
        param3 = self.st_addr if ins.param3 else self.st
        param3(
            self.IP + 3, 1 if param1(self.IP + 1) < param2(self.IP + 2) else 0
        )
        self.IP += 4

    # equals, execute IP+3 = IP+1 == IP+2 ? 1 : 0
    def eq(self, ins):
        param1 = self.ld_addr if ins.param1 else self.ld
        param2 = self.ld_addr if ins.param2 else self.ld
        param3 = self.st_addr if ins.param3 else self.st
        param3(
            self.IP + 3, 1 if param1(self.IP + 1) == param2(self.IP + 2) else 0
        )
        self.IP += 4

    # load the value of the address where addr points to
    def ld(self, addr):
        return self.ld_addr(self.program[addr])

    # load the value of addr
    def ld_addr(self, addr):
        return self.program[addr]

    # store the val in the address where addr points to
    def st(self, addr, val):
        self.st_addr(self.program[addr], val)

    # store the value in addr
    def st_addr(self, addr, val):
        self.program[addr] = val

    # return the value itself
    def val(self, val):
        return val


def part_1(program):
    computer = Computer()
    # make a copy so we don't alter the original program
    part_1_program = program.copy()

    # run the program
    print("beginning part_1 program, input 1:")
    computer.run(part_1_program)

    print("end of part_1 program")


def part_2(program):
    computer = Computer()
    # make a copy so we don't alter the original program
    part_2_program = program.copy()

    # run the program
    print("beginning part_2 program, input 5:")
    computer.run(part_2_program)

    print("end of part_2 program")


if __name__ == "__main__":
    with open("input.txt") as f:
        program = list(map(int, f.readline().split(",")))
        part_1(program)

        part_2(program)
