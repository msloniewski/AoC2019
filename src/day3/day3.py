import sys, os, re
sys.path.insert(0, os.path.abspath('..'))
from common.DayBase import DayBase


class Day3(DayBase):

    def __init__(self):
        super(Day3, self).__init__()
        self._path_a = None
        self._path_b = None

    def process_input(self):
        self._path_a = re.split(',', self._file.readline())
        self._path_b = re.split(',', self._file.readline())

    @staticmethod
    def _compute_part_of_path(part, current_coord):
        path_part = []
        steps = int(part[1:])
        dir = part[0]

        x = int(re.split(',', current_coord)[0])
        y = int(re.split(',', current_coord)[1])
        for i in range(0, steps):
            if dir == 'U':
                y = y + 1
            elif dir == 'D':
                y = y - 1
            elif dir == 'R':
                x = x + 1
            elif dir == 'L':
                x = x - 1
            path_part.append(f'{x},{y}')
        return path_part

    @staticmethod
    def manhattan_norm(point):
        x = int(re.split(',', point)[0])
        y = int(re.split(',', point)[1])
        return abs(x) + abs(y)

    def solve1(self):
        self.process_input()

        intersections = []

        path_a = ['0,0']
        for direction in self._path_a:
            path_a = path_a + self._compute_part_of_path(direction, path_a[-1])

        path_b = ['0,0']
        for direction in self._path_b:
            path_b = path_b + self._compute_part_of_path(direction, path_b[-1])

        for point in path_a[1:]:
            if point in path_b:
                intersections.append(point)

        closest_intersection = min(intersections, key=self.manhattan_norm)
        print(f"part1: {self.manhattan_norm(closest_intersection)}")

    def solve2(self):
        self.process_input()
	
        print(f"part2: {0}")


if __name__ == "__main__":
    dayPart1 = Day3()
    dayPart1.solve1()
    dayPart2 = Day3()
    dayPart2.solve2()
