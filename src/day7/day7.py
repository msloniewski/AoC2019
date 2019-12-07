import sys
import os
import re
from itertools import permutations
sys.path.insert(0, os.path.abspath('..'))
from common.DayBase import DayBase


class Day7(DayBase):

    def __init__(self):
        super(Day7, self).__init__()
        self._instructions = None
        self._instructions_copy = None
        self._current_input = 0

    def process_input(self):
        self._instructions = re.sub("\s*", "", self._file.readline())
        self._instructions = re.split(",", self._instructions)
        self._instructions_copy = self._instructions[:]

    def reset_machine(self):
        self._instructions = self._instructions_copy[:]
        self._current_input = 0

    def _give_param_val(self, param_modes, param_num, param):
        if param_num + 1 > len(param_modes):
            return int(self._instructions[param])
        if param_modes[-param_num - 1] == '1':
            return param
        else:
            return int(self._instructions[param])

    def _compute_program(self, use_keyboard_input=True, input_vals=[]):
        i = 0
        output_vals = []

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
                if opcode == 1: # add
                    self._instructions[destination] = str(operand1 + operand2)
                else:  # mult
                    self._instructions[destination] = str(operand1 * operand2)
                i = i + 4
            elif opcode == 3:  # scan
                val = 0
                if use_keyboard_input:
                    val = input("Provide value:")
                else:
                    val = input_vals[self._current_input]
                    self._current_input = self._current_input + 1
                self._instructions[int(self._instructions[i + 1])] = val
                i = i + 2
            elif opcode == 4: # print
                operand = self._give_param_val(parameters_modes, 0, int(self._instructions[i + 1]))
                print(f'value: {operand}')
                output_vals.append(operand)
                i = i + 2
            elif opcode == 5:  # jmp if true
                operand = self._give_param_val(parameters_modes, 0, int(self._instructions[i + 1]))
                if operand != 0:
                    i = self._give_param_val(parameters_modes, 1, int(self._instructions[i + 2]))
                else:
                    i = i + 3
            elif opcode == 6:  # jmp if false
                operand = self._give_param_val(parameters_modes, 0, int(self._instructions[i + 1]))
                if operand == 0:
                    i = self._give_param_val(parameters_modes, 1, int(self._instructions[i + 2]))
                else:
                    i = i + 3
            elif opcode == 7:  # less than
                operand1 = self._give_param_val(parameters_modes, 0, int(self._instructions[i + 1]))
                operand2 = self._give_param_val(parameters_modes, 1, int(self._instructions[i + 2]))
                destination = int(self._instructions[i + 3])
                if operand1 < operand2:
                    self._instructions[destination] = str(1)
                else:
                    self._instructions[destination] = str(0)
                i = i + 4
            elif opcode == 8:  # eq
                operand1 = self._give_param_val(parameters_modes, 0, int(self._instructions[i + 1]))
                operand2 = self._give_param_val(parameters_modes, 1, int(self._instructions[i + 2]))
                destination = int(self._instructions[i + 3])
                if operand1 == operand2:
                    self._instructions[destination] = str(1)
                else:
                    self._instructions[destination] = str(0)
                i = i + 4
            else:
                print(f'Unknown opcode {opcode}')
                exit()
        return output_vals

    def solve1(self):
        self.process_input()

        phase_settings = permutations(["0", "1", "2", "3", "4"])
        phase_settings_results = []

        for phase_setting in phase_settings:
            current_output = "0"
            for phase in phase_setting:
                self.reset_machine()
                current_output = self._compute_program(False, [phase, current_output])[0]
            phase_settings_results.append(int(current_output))
        print(f"Part 1: {max(phase_settings_results)}")

    def solve2(self):
        self.process_input()

        #self._compute_program()
        print("Part 2 done")

if __name__ == "__main__":
    dayPart1 = Day7()
    dayPart1.solve1()
    dayPart2 = Day7()
    dayPart2.solve2()
