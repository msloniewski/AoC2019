import sys, os, re
sys.path.insert(0, os.path.abspath('..'))
from common.DayBase import DayBase


class Day2(DayBase):

    def __init__(self):
        super(Day2, self).__init__()
        self._instructions = None
        self._instructions_backup = None

    def process_input(self):
        self._instructions = self._file.readline()
        self._instructions = re.split(",", self._instructions)
        for i, instr in enumerate(self._instructions):
            self._instructions[i] = int(self._instructions[i])
        self._instructions_backup = self._instructions

    def _compute_program(self, noun, verb):

        self._instructions[1] = noun
        self._instructions[2] = verb

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

    def solve1(self):
        self.process_input()

        self._compute_program(12, 2)

        print(f"part1: {self._instructions[0]}")

    def solve2(self):
        self.process_input()

        noun = None
        verb = None

        for i in range(0, 100):
            for j in range(0, 100):
                self._instructions = self._instructions_backup[:]
                self._compute_program(i, j)
                if self._instructions[0] == 19690720:
                    noun = i
                    verb = j

        print(f"part2: {100 * noun + verb}")


if __name__ == "__main__":
    dayPart1 = Day2()
    dayPart1.solve1()
    dayPart2 = Day2()
    dayPart2.solve2()
