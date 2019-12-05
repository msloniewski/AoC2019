import sys, os, re
sys.path.insert(0, os.path.abspath('..'))
from common.DayBase import DayBase


class Day5(DayBase):

    def __init__(self):
        super(Day5, self).__init__()
        self._instructions = None

    def process_input(self):
        self._instructions = self._file.readline()
        self._instructions = re.split(",", self._instructions)

    def _give_param_val(self, param_modes, param_num, param):
        if param_num + 1 > len(param_modes):
            return int(self._instructions[param])
        if param_modes[-param_num - 1] == '1':
            return param
        else:
            return int(self._instructions[param])

    def _compute_program(self):
        i = 0

        run_program = True
        while run_program:
            instruction = self._instructions[i]
            opcode = int(instruction[-2:]) # two last chars
            parameters_modes = instruction[:-2] # first x chars without two last chars
            if opcode == 99:
                run_program = False
            elif opcode == 1 or opcode == 2:
                operand1 = self._give_param_val(parameters_modes, 0, int(self._instructions[i + 1]))
                operand2 = self._give_param_val(parameters_modes, 1, int(self._instructions[i + 2]))
                destination = int(self._instructions[i + 3])
                if opcode == 1:
                    self._instructions[destination] = str(operand1 + operand2)
                else:
                    self._instructions[destination] = str(operand1 * operand2)
                i = i + 4
            elif opcode == 3:
                val = input("Provide value:")
                self._instructions[int(self._instructions[i + 1])] = val
                i = i + 2
            elif opcode == 4:
                operand = self._give_param_val(parameters_modes, 0, int(self._instructions[i + 1]))
                print(f'value: {operand}')
                i = i + 2
            else:
                print(f'Unknown opcode {opcode}')
                exit()

    def solve1(self):
        self.process_input()

        self._compute_program()

        #print(f"part1: {self._instructions[0]}")

    def solve2(self):
        self.process_input()


        print(f"part2: {0}")


if __name__ == "__main__":
    dayPart1 = Day5()
    dayPart1.solve1()
    dayPart2 = Day5()
    dayPart2.solve2()
