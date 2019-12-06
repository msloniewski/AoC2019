import sys, os, re
sys.path.insert(0, os.path.abspath('..'))
from common.DayBase import DayBase


class Day6(DayBase):

    def __init__(self):
        super(Day6, self).__init__()
        self.orbit_map = {}

    def process_input(self):
        for line in self._file.readlines():
            line = re.sub('\s*', '', line)
            center, moon = re.split('\)', line)
            self.orbit_map[moon] = center

    def _compute_number_of_orbits(self, moon):
        i = 0
        while moon in self.orbit_map:
            moon = self.orbit_map[moon]
            i = i + 1
        return i

    def solve1(self):
        self.process_input()

        orbit_sum = 0
        for moon in self.orbit_map:
            orbit_sum = orbit_sum + self._compute_number_of_orbits(moon)

        print(f"part1: {orbit_sum}")

    def solve2(self):
        self.process_input()

        print(f"part2: {0}")


if __name__ == "__main__":
    dayPart1 = Day6()
    dayPart1.solve1()
    dayPart2 = Day6()
    dayPart2.solve2()
