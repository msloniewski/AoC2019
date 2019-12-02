import sys, os, re
sys.path.insert(0, os.path.abspath('..'))
from common.DayBase import DayBase


class Day2(DayBase):

    def __init__(self):
        super(Day2, self).__init__()
        self._instructions = None

    def process_input(self):
        self._instructions = self._file.readline()
        self._instructions = re.split(",", self._instructions)
        for i, instr in enumerate(self._instructions):
            self._instructions[i] = int(self._instructions[i])

    def solve1(self):
        self.process_input()

        self._instructions[1] = 12
        self._instructions[2] = 2

        i = 0

        run_program = True
        while run_program:
            if self._instructions[i] == 99:
                run_program = False
            else:
                operand1 = self._instructions[self._instructions[i + 1]]
                operand2 = self._instructions[self._instructions[i + 2]]
                destination = self._instructions[i + 3]
                if self._instructions[i] == 1:
                    self._instructions[destination] = operand1 + operand2
                else:
                    self._instructions[destination] = operand1 * operand2
            i = i + 4

        print(f"part1: {self._instructions[0]}")

    def solve2(self):
        pass
        #print(f"part2: {fuel_needed}")


if __name__ == "__main__":
    dayPart1 = Day2()
    dayPart1.solve1()
    dayPart2 = Day2()
    dayPart2.solve2()
