import sys
import os
import re
import enum
from itertools import permutations
sys.path.insert(0, os.path.abspath('..'))
from common.DayBase import DayBase


class ReturnCause(enum.Enum):
    print_stop = enum.auto()
    input_empty_stop = enum.auto()
    program_stop = enum.auto()


class Day13(DayBase):

    def __init__(self):
        super(Day13, self).__init__()
        self._instructions = None
        self._instructions_copy = None
        self._current_input = 0
        self._curr_instruction = 0
        self._base_offset = 0

    def process_input(self):
        self._instructions = re.sub("\s*", "", self._file.readline())
        self._instructions = re.split(",", self._instructions)
        self._instructions = dict(enumerate(self._instructions))
        self._instructions_copy = self._instructions.copy()

    def reset_machine(self):
        self._instructions = self._instructions_copy.copy()
        self._current_input = 0
        self._curr_instruction = 0

    def _fetch_new_data(self):
        if self._curr_instruction not in self._instructions:
            self._instructions[self._curr_instruction] = "0"
        ret = self._instructions[self._curr_instruction]
        self._curr_instruction = self._curr_instruction + 1
        return ret

    def _give_param_val(self, param_modes, param_num, param):
        index = 0
        if param_num + 1 > len(param_modes):
            index = param
        else:
            if param_modes[-param_num - 1] == '1':
                return param
            elif param_modes[-param_num - 1] == '2':
                index = param + self._base_offset
            else:
                index = param
        if index not in self._instructions:
            self._instructions[index] = 0
        return int(self._instructions[index])

    def _give_index(self, param_modes, param_num, param):
        index = 0
        if param_num + 1 > len(param_modes):
            index = param
        else:
            if param_modes[-param_num - 1] == '1':
                return param
            elif param_modes[-param_num - 1] == '2':
                index = param + self._base_offset
            else:
                index = param
        if index not in self._instructions:
            self._instructions[index] = 0
        return index

    def _compute_program(self, use_keyboard_input=True, input_vals=[], halt_on_io=False):
        output_vals = []
        stop_cause = ReturnCause.program_stop

        run_program = True
        while run_program:
            instruction = self._fetch_new_data()
            opcode = int(instruction[-2:]) # two last chars
            parameters_modes = instruction[:-2] # first x chars without two last chars
            if opcode == 99:
                run_program = False
                stop_cause = ReturnCause.program_stop
            elif opcode == 1 or opcode == 2:
                operand1 = self._give_param_val(parameters_modes, 0, int(self._fetch_new_data()))
                operand2 = self._give_param_val(parameters_modes, 1, int(self._fetch_new_data()))
                destination = self._give_index(parameters_modes, 2, int(self._fetch_new_data()))
                if opcode == 1:  # add
                    self._instructions[destination] = str(operand1 + operand2)
                else:  # mult
                    self._instructions[destination] = str(operand1 * operand2)
            elif opcode == 3:  # scan
                if use_keyboard_input:
                    val = input("Provide value:")
                    self._instructions[self._give_index(parameters_modes, 0, int(self._fetch_new_data()))] = val
                else:
                    if self._current_input == len(input_vals):
                        run_program = False
                        stop_cause = ReturnCause.input_empty_stop
                        self._current_input = 0
                        #  hack
                        self._curr_instruction = self._curr_instruction - 1
                    else:
                        val = input_vals[self._current_input]
                        self._current_input = self._current_input + 1
                        self._instructions[self._give_index(parameters_modes, 0, int(self._fetch_new_data()))] = val
            elif opcode == 4:  # print
                operand = self._give_param_val(parameters_modes, 0, int(self._fetch_new_data()))
                print(f'value: {operand}')
                output_vals.append(operand)
                if halt_on_io:
                    run_program = False
                    stop_cause = ReturnCause.print_stop
            elif opcode == 5:  # jmp if true
                operand = self._give_param_val(parameters_modes, 0, int(self._fetch_new_data()))
                if operand != 0:
                    self._curr_instruction = self._give_param_val(parameters_modes, 1, int(self._fetch_new_data()))
                else:
                    #  omit 3rd operand
                    self._fetch_new_data()
            elif opcode == 6:  # jmp if false
                operand = self._give_param_val(parameters_modes, 0, int(self._fetch_new_data()))
                if operand == 0:
                    self._curr_instruction = self._give_param_val(parameters_modes, 1, int(self._fetch_new_data()))
                else:
                    #  omit 3rd operand
                    self._fetch_new_data()
            elif opcode == 7:  # less than
                operand1 = self._give_param_val(parameters_modes, 0,
                                                int(self._fetch_new_data()))
                operand2 = self._give_param_val(parameters_modes, 1,
                                                int(self._fetch_new_data()))
                destination = self._give_index(parameters_modes, 2, int(self._fetch_new_data()))
                if operand1 < operand2:
                    self._instructions[destination] = str(1)
                else:
                    self._instructions[destination] = str(0)
            elif opcode == 8:  # eq
                operand1 = self._give_param_val(parameters_modes, 0,
                                                int(self._fetch_new_data()))
                operand2 = self._give_param_val(parameters_modes, 1,
                                                int(self._fetch_new_data()))
                destination = self._give_index(parameters_modes, 2, int(self._fetch_new_data()))
                if operand1 == operand2:
                    self._instructions[destination] = str(1)
                else:
                    self._instructions[destination] = str(0)
            elif opcode == 9:  # adj relative
                operand = self._give_param_val(parameters_modes, 0, int(self._fetch_new_data()))
                self._base_offset = self._base_offset + operand
            else:
                print(f'Unknown opcode {opcode}')
                exit()
        return [stop_cause, output_vals]

    def solve1(self):
        self.process_input()

        board = self._compute_program()[1]
        block_tiles = 0
        for i in range(len(board)):
            if i % 3 == 2:
                print(board[i])
                if board[i] == 2:
                    block_tiles = block_tiles + 1

        print(f"Part 1: {block_tiles}")

    def solve2(self):
        self.process_input()

        print(f"Part 2: done")

if __name__ == "__main__":
    dayPart1 = Day13()
    dayPart1.solve1()
    dayPart2 = Day13()
    #dayPart2.solve2()
