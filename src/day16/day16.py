import sys, os, re, math
import functools
sys.path.insert(0, os.path.abspath('..'))
from common.DayBase import DayBase


class Day16(DayBase):

    def __init__(self):
        super(Day16, self).__init__()
        self.pattern = [0, 1, 0, -1]
        self.input_signal = ""

    def process_input(self):
        self.input_signal = self._file.readline().strip()

    def get_mult(self, position, stage):
        return self.pattern[((position + 1) // (stage + 1)) % len(self.pattern)]

    def solve1(self):
        self.process_input()

        input = self.input_signal
        for _ in range(100):
            output = ""
            for stage in range(len(input)):
                result = 0
                for position in range(len(input)):
                    mult = self.get_mult(position, stage)
                    result = result + int(input[position]) * mult
                output = output + str(abs(result) % 10)

            input = output




        print(f"part1: {input}")

    def solve2(self):
        self.process_input()

        print(f"part2: {0}")


if __name__ == "__main__":
    dayPart1 = Day16()
    dayPart1.solve1()
    dayPart2 = Day16()
    dayPart2.solve2()
