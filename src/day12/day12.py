import sys, os, re, math
sys.path.insert(0, os.path.abspath('..'))
from common.DayBase import DayBase


class Moon:

    def __init__(self, coordinates):
        self._coordinates = coordinates
        self._velocity = [0, 0, 0]

    def apply_gravity(self, other_moon):
        for i, coordinate in enumerate(self._coordinates):
            if coordinate > other_moon._coordinates[i]:
                self._velocity[i] = self._velocity[i] - 1
                other_moon._velocity[i] = other_moon._velocity[i] + 1
            elif coordinate < other_moon._coordinates[i]:
                self._velocity[i] = self._velocity[i] + 1
                other_moon._velocity[i] = other_moon._velocity[i] - 1

    def apply_velocity(self):
        for i, velocity in enumerate(self._velocity):
            self._coordinates[i] = self._coordinates[i] + velocity

    def get_total_energy(self):
        kin_energy = 0
        pot_energy = 0

        for velocity in self._velocity:
            kin_energy = kin_energy + abs(velocity)
        for coord in self._coordinates:
            pot_energy = pot_energy + abs(coord)

        return pot_energy * kin_energy

    def get_state(self, i):
        return [self._coordinates[i], self._velocity[i]]


class Day12(DayBase):

    def __init__(self):
        super(Day12, self).__init__()
        self._moons = []
        self.coord_size = 0

    def process_input(self):
        for line in self._file.readlines():
            coordinates = re.findall("[-]?\d+", line)
            self._moons.append(Moon(list(map(int, coordinates))))
        self.coord_size = len(self._moons[0]._velocity)

    def get_moons_state(self, i):
        state = []
        for moon in self._moons:
            state.append(moon.get_state(i))
        return state

    def solve1(self):
        self.process_input()

        for i in range(0, 1000):
            for current_moon in range(len(self._moons)):
                for moon_to_compare in range(len(self._moons) - current_moon):
                    self._moons[current_moon].apply_gravity(self._moons[moon_to_compare + current_moon])
            for moon in self._moons:
                moon.apply_velocity()

        total_system_en = 0
        for moon in self._moons:
            total_system_en = total_system_en + moon.get_total_energy()

        print(f"part1: {total_system_en}")

    def solve2(self):
        self.process_input()

        initial_state = []

        for i in range(self.coord_size):
            initial_state.append(self.get_moons_state(i))

        i = 0
        x_repeat = -1
        y_repeat = -1
        z_repeat = -1
        while x_repeat == -1 or y_repeat == -1 or z_repeat == -1:
            i = i + 1
            for current_moon in range(len(self._moons)):
                for moon_to_compare in range(len(self._moons) - current_moon):
                    self._moons[current_moon].apply_gravity(self._moons[moon_to_compare + current_moon])
            for moon in self._moons:
                moon.apply_velocity()
            if self.get_moons_state(0) == initial_state[0]:
                x_repeat = i
            if self.get_moons_state(1) == initial_state[1]:
                y_repeat = i
            if self.get_moons_state(2) == initial_state[2]:
                z_repeat = i

        total_system_en = 0
        for moon in self._moons:
            print(moon.get_state(0))
            total_system_en = total_system_en + moon.get_total_energy()

        period = x_repeat * y_repeat // math.gcd(x_repeat, y_repeat)
        period = z_repeat * period // math.gcd(z_repeat, period)
        print(f"part2: {period}")


if __name__ == "__main__":
    dayPart1 = Day12()
    dayPart1.solve1()
    dayPart2 = Day12()
    dayPart2.solve2()
