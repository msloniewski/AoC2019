import sys
import os
import re
import enum
import math
from itertools import permutations
sys.path.insert(0, os.path.abspath('..'))
from common.DayBase import DayBase

def sort_asteroids_clockwise(asteroid):
    return - (math.atan2(-asteroid[1], asteroid[0]) + math.pi / 2 * 3 + math.pi * 2) % (math.pi * 2)

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

    def _shoot_asteroid_and_asteroid_behind(self, asteroids, asteroid_to_remove):
        shot_asteroid = None

        dx = asteroid_to_remove[0]
        dy = asteroid_to_remove[1]

        gcd = math.gcd(dx, dy)
        dx = dx / gcd
        dy = dy / gcd

        x = 0
        y = 0

        while -self._max_x <= x <= self._max_x and -self._max_y <= y <= self._max_y:
            x = x + dx
            y = y + dy

            if [x, y] in asteroids:
                if not shot_asteroid:
                    shot_asteroid = [x, y]
                asteroids.remove([x, y])

        return [shot_asteroid, asteroids]

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

        return self._asteroids[results.index(max(results))]

    def solve2(self):
        monitoring_station = self.solve1()

        asteroids_left = self._asteroids[:]


        for i, ast in enumerate(asteroids_left):
            asteroids_left[i] = [ast[0] - monitoring_station[0], ast[1] - monitoring_station[1]]
        asteroids_left.remove([0, 0])

        asteroid_taken_down = []

        asteroids_left.sort(key=sort_asteroids_clockwise)
        while len(asteroid_taken_down) < 200:
            asteroids_left_copy = asteroids_left[:]
            while asteroids_left_copy:
                asteroid_shot, asteroids_left_copy = self._shoot_asteroid_and_asteroid_behind(asteroids_left_copy, asteroids_left_copy[0])
                asteroid_taken_down.append(asteroid_shot)
            for asteroid in asteroid_taken_down:
                if asteroid in asteroids_left:
                    asteroids_left.remove(asteroid)

        print(f"Part 2: {(asteroid_taken_down[199][0] + monitoring_station[0]) * 100 + asteroid_taken_down[199][1] + monitoring_station[1]}")

if __name__ == "__main__":
    dayPart1 = Day10()
    dayPart1.solve1()
    dayPart2 = Day10()
    dayPart2.solve2()
