import sys, os
sys.path.insert(0, os.path.abspath('..'))
from common.DayBase import DayBase


class Day1(DayBase):

    def __init__(self):
        super(Day1, self).__init__()
        self._masses = None

    def process_input(self):
        self._masses = self._file.readlines()
        for i, mass in enumerate(self._masses):
            self._masses[i] = int(self._masses[i])

    def solve(self):
        self.process_input()

        fuel_needed = 0
        for mass in self._masses:
            fuel_needed = fuel_needed + max(0, int(mass / 3) - 2)

        print(fuel_needed)


if __name__ == "__main__":
    day = Day1()
    day.solve()