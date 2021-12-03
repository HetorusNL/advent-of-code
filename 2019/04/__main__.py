def part_1(start, end):
    num_passwords = 0
    for i in range(start, end + 1):
        password = str(i)
        double = False
        increasing = True
        for a, b in zip(password[0:-1], password[1:]):
            double = True if a == b else double
            increasing = False if int(a) > int(b) else increasing
        if double and increasing:
            num_passwords += 1

    print(f"part_1 num valid passwords: {num_passwords}")


def part_2(start, end):
    valid_part_1_passwords = []
    for i in range(start, end + 1):
        password = str(i)
        double = False
        increasing = True
        for a, b in zip(password[0:-1], password[1:]):
            double = True if a == b else double
            increasing = False if int(a) > int(b) else increasing
        if double and increasing:
            valid_part_1_passwords.append(password)

    num_passwords = 0
    for password in valid_part_1_passwords:
        for i in range(9, -1, -1):
            if password.count(str(i)) > 2:
                continue  # skip this one, more than 2 digits
            elif password.count(str(i)) == 2:
                num_passwords += 1
                break

    print(f"part_2 num valid passwords: {num_passwords}")


if __name__ == "__main__":
    start = 359282
    end = 820401
    part_1(start, end)

    part_2(start, end)
