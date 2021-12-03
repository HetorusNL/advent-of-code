def part_1(lines, cross_points):
    nearest_cross_points = [
        *filter(
            lambda b: b[0] + b[1]
            == min(map(lambda a: abs(a[0]) + abs(a[1]), cross_points)),
            cross_points,
        )
    ]

    print("part_1:")
    print(f"nearest cross point: {nearest_cross_points}")
    print(f"with distance {sum(map(abs,*nearest_cross_points))}")


def part_2(lines, cross_points):
    # note, index is 0-based, so add 1
    fewest_wire_steps = min(
        sum(line.index(cross_point) + 1 for line in lines)
        for cross_point in cross_points
    )
    print("part_2:")
    print(f"fewest wire steps: {fewest_wire_steps}")


def get_lines_and_cross_points(input_lines):
    lines = []
    for i in range(len(input_lines)):
        lines.append([])
    for i in range(len(input_lines)):
        point = (0, 0)
        # lines[i].append(point)  # don't insert the origin
        for entry in input_lines[i].split(","):
            if entry[0] == "U":
                list(
                    map(
                        lines[i].append,
                        map(
                            lambda a: (point[0], point[1] + a),
                            range(1, int(entry[1:]) + 1),
                        ),
                    )
                )
                point = (point[0], point[1] + int(entry[1:]))
            elif entry[0] == "L":
                list(
                    map(
                        lines[i].append,
                        map(
                            lambda a: (point[0] - a, point[1]),
                            range(1, int(entry[1:]) + 1),
                        ),
                    )
                )
                point = (point[0] - int(entry[1:]), point[1])
            elif entry[0] == "D":
                list(
                    map(
                        lines[i].append,
                        map(
                            lambda a: (point[0], point[1] - a),
                            range(1, int(entry[1:]) + 1),
                        ),
                    )
                )
                point = (point[0], point[1] - int(entry[1:]))
            elif entry[0] == "R":
                list(
                    map(
                        lines[i].append,
                        map(
                            lambda a: (point[0] + a, point[1]),
                            range(1, int(entry[1:]) + 1),
                        ),
                    )
                )
                point = (point[0] + int(entry[1:]), point[1])
            else:
                print(f"Unknown direction: {entry[0]}")

    # perform set intersection between lines[0] and lines[1:]
    cross_points = set(lines[0]).intersection(*lines[1:])

    return lines, cross_points


if __name__ == "__main__":
    with open("input.txt") as f:
        input_lines = f.readlines()
        lines, cross_points = get_lines_and_cross_points(input_lines)

        part_1(lines, cross_points)

        part_2(lines, cross_points)
