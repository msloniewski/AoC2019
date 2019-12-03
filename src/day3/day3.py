import sys, os, re
sys.path.insert(0, os.path.abspath('..'))
from common.DayBase import DayBase


class Day3(DayBase):

    def __init__(self):
        super(Day3, self).__init__()
        self._dirs_a = None
        self._dirs_b = None
        self._path_b = None
        self._path_a = None
        self._intersections = None

    def process_input(self):
        self._dirs_a = re.split(',', self._file.readline())
        self._dirs_b = re.split(',', self._file.readline())

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

        self._intersections = []

        self._path_a = ['0,0']
        for direction in self._dirs_a:
            self._path_a = self._path_a + self._compute_part_of_path(direction, self._path_a[-1])

        self._path_b = ['0,0']
        for direction in self._dirs_b:
            self._path_b = self._path_b + self._compute_part_of_path(direction, self._path_b[-1])

        for point in self._path_a[1:]:
            if point in self._path_b:
                self._intersections.append(point)

        closest_intersection = min(self._intersections, key=self.manhattan_norm)
        print(f"part1: {self.manhattan_norm(closest_intersection)}")

    def solve2(self):
        self.solve1()

        path_a_distances = {}
        path_b_distances = {}
        sum_of_distances = []

        for i, point in enumerate(self._path_a):
            if point in self._intersections:
                if point not in path_a_distances:
                    path_a_distances[point] = i

        for i, point in enumerate(self._path_b):
            if point in self._intersections:
                if point not in path_b_distances:
                    path_b_distances[point] = i

        for point in path_a_distances:
            sum_of_distances.append(path_a_distances[point] + path_b_distances[point])
	
        print(f"part2: {min(sum_of_distances)}")


if __name__ == "__main__":
    dayPart1 = Day3()
    dayPart1.solve1()
    dayPart2 = Day3()
    dayPart2.solve2()
