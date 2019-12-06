import sys, os, re
sys.path.insert(0, os.path.abspath('..'))
from common.DayBase import DayBase


class Day6(DayBase):

    def __init__(self):
        super(Day6, self).__init__()
        self.orbit_map_moon_to_center = {}

    def process_input(self):
        for line in self._file.readlines():
            line = re.sub('\s*', '', line)
            center, moon = re.split('\)', line)
            self.orbit_map_moon_to_center[moon] = center

    def _compute_number_of_orbits(self, moon):
        i = 0
        while moon in self.orbit_map_moon_to_center:
            moon = self.orbit_map_moon_to_center[moon]
            i = i + 1
        return i

    def _find_neighbours_of_globe(self, globe):
        moons = []
        for moon in self.orbit_map_moon_to_center:
            center = self.orbit_map_moon_to_center[moon]
            if center == globe:
                moons.append(moon)
            if moon == globe:
                moons.append(center)
        return moons

    def _find_shortest_path(self, start, end):
        i = 0
        visited = [start]
        while end not in visited:
            new_visited = []
            for globe in visited:
                new_globes = self._find_neighbours_of_globe(globe)
                for new_globe in new_globes:
                    if new_globe not in visited:
                        new_visited.append(new_globe)
            i = i + 1
            visited = visited + new_visited
        return i

    def solve1(self):
        self.process_input()

        orbit_sum = 0
        for moon in self.orbit_map_moon_to_center:
            orbit_sum = orbit_sum + self._compute_number_of_orbits(moon)

        print(f"part1: {orbit_sum}")

    def solve2(self):
        self.process_input()

        santa_globe = self.orbit_map_moon_to_center['SAN']
        my_globe = self.orbit_map_moon_to_center['YOU']

        shortest_path = self._find_shortest_path(santa_globe, my_globe)

        print(f"part2: {shortest_path}")


if __name__ == "__main__":
    dayPart1 = Day6()
    dayPart1.solve1()
    dayPart2 = Day6()
    dayPart2.solve2()
