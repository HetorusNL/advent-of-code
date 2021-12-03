def part_1(orbits):
    num_orbits = 0
    for orbit in list(orbits.keys()):
        while orbits.get(orbit):
            orbit = orbits.get(orbit)
            num_orbits += 1

    print(f"part_1 num orbits: {num_orbits}")


def part_2(orbits):
    orbits_you = []
    orbits_san = []

    orbit_you = "YOU"
    orbit_san = "SAN"

    while orbits.get(orbit_you):
        orbits_you.append(orbits.get(orbit_you))
        orbit_you = orbits.get(orbit_you)

    while orbits.get(orbit_san):
        orbits_san.append(orbits.get(orbit_san))
        orbit_san = orbits.get(orbit_san)

    orbital_transfers = 0
    for i, o in enumerate(orbits_you):
        if o in orbits_san:
            orbital_transfers = i + orbits_san.index(o)
            break

    print(f"part_2: orbital transfers: {orbital_transfers}")


if __name__ == "__main__":
    with open("input.txt") as f:
        orbits = {}
        orbits_input = f.readlines()

        for orbit in orbits_input:
            a, b = orbit.split(")")
            orbits[b.strip()] = a.strip()

        part_1(orbits)

        part_2(orbits)
