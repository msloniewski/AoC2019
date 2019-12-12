import sys
import os
import re
import enum
import math
from itertools import permutations
sys.path.insert(0, os.path.abspath('..'))
from common.DayBase import DayBase


class ReturnCause(enum.Enum):
    print_stop = enum.auto()
    input_empty_stop = enum.auto()
    program_stop = enum.auto()


class Day10(DayBase):

    def __init__(self):
        super(Day10, self).__init__()
        self._asteroids = []
        self._max_x = None
        self._max_y = None

    def process_input(self):
        for y, line in enumerate(self._file.readlines()):
            line = re.sub(r"\s*", "", line)
            for x, object in enumerate(line):
                if object == '#':
                    self._asteroids.append([x, y])
        self._max_x = max(self._asteroids, key=lambda x: x[0])[0]
        self._max_y = max(self._asteroids, key=lambda x: x[1])[1]

    def solve1(self):
        self.process_input()

        results = []

        for asteroid in self._asteroids:
            asteroids_left = self._asteroids[:]
            asteroids_left.remove(asteroid)

            i = 0
            while asteroids_left:
                i = i + 1
                asteroid_taken = asteroids_left[0]

                asteroids_left.remove(asteroid_taken)

                dx = asteroid_taken[0] - asteroid[0]
                dy = asteroid_taken[1] - asteroid[1]

                gcd = math.gcd(dx, dy)
                dx = dx / gcd
                dy = dy / gcd

                x = asteroid[0]
                y = asteroid[1]

                while 0 <= x <= self._max_x and 0 <= y <= self._max_y:
                    x = x + dx
                    y = y + dy

                    if [x, y] in asteroids_left:
                        asteroids_left.remove([x, y])

            results.append(i)
        print(self._asteroids[results.index(max(results))])

        print(f"Part 1: {max(results)}")

    def solve2(self):
        self.process_input()
        print(f"Part 2: done")


if __name__ == "__main__":
    dayPart1 = Day10()
    dayPart1.solve1()
    dayPart2 = Day10()
    dayPart2.solve2()
