def part_1(modules):
    print("fuel requirement part_1:")
    print(sum(module // 3 - 2 for module in modules))


def part_2(modules):
    # perform exhaustive calculation
    print("fuel requirement part_2:")
    total = 0
    for module in modules:
        while (module // 3 - 2) > 0:
            fuel = module // 3 - 2
            total += fuel
            module = fuel
    print(total)


if __name__ == "__main__":
    with open("input.txt") as f:
        lines = [*map(int, f.readlines())]
        part_1(lines)

        part_2(lines)
