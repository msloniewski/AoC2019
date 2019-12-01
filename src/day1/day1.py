import sys, os
sys.path.insert(0, os.path.abspath('..'))
from common.DayBase import DayBase


class Day1(DayBase):

    def __init__(self):
        super(Day1, self).__init__()
        self._masses = None

    @staticmethod
    def _process_fuel_consumption(mass):
        fuel_needed = 0
        while mass > 0:
            mass = max(0, int(mass / 3) - 2)
            fuel_needed = fuel_needed + mass
        return fuel_needed

    def process_input(self):
        self._masses = self._file.readlines()
        for i, mass in enumerate(self._masses):
            self._masses[i] = int(self._masses[i])

    def solve1(self):
        self.process_input()

        fuel_needed = 0
        for mass in self._masses:
            fuel_needed = fuel_needed + max(0, int(mass / 3) - 2)

        print(f"part1: {fuel_needed}")

    def solve2(self):
        self.process_input()

        fuel_needed = 0
        for mass in self._masses:
            fuel_needed = fuel_needed + self._process_fuel_consumption(mass)

        print(f"part2: {fuel_needed}")


if __name__ == "__main__":
    dayPart1 = Day1()
    dayPart1.solve1()
    dayPart2 = Day1()
    dayPart2.solve2()