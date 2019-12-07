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


class Day7(DayBase):

    def __init__(self):
        super(Day7, self).__init__()
        self._instructions = None
        self._instructions_copy = None
        self._current_input = 0
        self._curr_instruction = 0

    def process_input(self):
        self._instructions = re.sub("\s*", "", self._file.readline())
        self._instructions = re.split(",", self._instructions)
        self._instructions_copy = self._instructions[:]

    def reset_machine(self):
        self._instructions = self._instructions_copy[:]
        self._current_input = 0
        self._curr_instruction = 0

    def _give_param_val(self, param_modes, param_num, param):
        if param_num + 1 > len(param_modes):
            return int(self._instructions[param])
        if param_modes[-param_num - 1] == '1':
            return param
        else:
            return int(self._instructions[param])

    def _compute_program(self, use_keyboard_input=True, input_vals=[], halt_on_io=False):
        output_vals = []
        stop_cause = ReturnCause.program_stop

        run_program = True
        while run_program:
            instruction = self._instructions[self._curr_instruction]
            opcode = int(instruction[-2:]) # two last chars
            parameters_modes = instruction[:-2] # first x chars without two last chars
            if opcode == 99:
                run_program = False
                stop_cause = ReturnCause.program_stop
            elif opcode == 1 or opcode == 2:
                operand1 = self._give_param_val(parameters_modes, 0, int(self._instructions[self._curr_instruction + 1]))
                operand2 = self._give_param_val(parameters_modes, 1, int(self._instructions[self._curr_instruction + 2]))
                destination = int(self._instructions[self._curr_instruction + 3])
                if opcode == 1: # add
                    self._instructions[destination] = str(operand1 + operand2)
                else:  # mult
                    self._instructions[destination] = str(operand1 * operand2)
                self._curr_instruction = self._curr_instruction + 4
            elif opcode == 3:  # scan
                val = 0
                if use_keyboard_input:
                    val = input("Provide value:")
                    self._instructions[int(self._instructions[self._curr_instruction + 1])] = val
                    self._curr_instruction = self._curr_instruction + 2
                else:
                    if self._current_input == len(input_vals):
                        run_program = False
                        stop_cause = ReturnCause.input_empty_stop
                        self._current_input = 0
                    else:
                        val = input_vals[self._current_input]
                        self._current_input = self._current_input + 1
                        self._instructions[int(self._instructions[self._curr_instruction + 1])] = val
                        self._curr_instruction = self._curr_instruction + 2

            elif opcode == 4: # print
                operand = self._give_param_val(parameters_modes, 0, int(self._instructions[self._curr_instruction + 1]))
                print(f'value: {operand}')
                output_vals.append(operand)
                if halt_on_io:
                    run_program = False
                    stop_cause = ReturnCause.print_stop
                self._curr_instruction = self._curr_instruction + 2
            elif opcode == 5:  # jmp if true
                operand = self._give_param_val(parameters_modes, 0, int(self._instructions[self._curr_instruction + 1]))
                if operand != 0:
                    self._curr_instruction = self._give_param_val(parameters_modes, 1, int(self._instructions[self._curr_instruction + 2]))
                else:
                    self._curr_instruction = self._curr_instruction + 3
            elif opcode == 6:  # jmp if false
                operand = self._give_param_val(parameters_modes, 0, int(self._instructions[self._curr_instruction + 1]))
                if operand == 0:
                    self._curr_instruction = self._give_param_val(parameters_modes, 1, int(self._instructions[self._curr_instruction + 2]))
                else:
                    self._curr_instruction = self._curr_instruction + 3
            elif opcode == 7:  # less than
                operand1 = self._give_param_val(parameters_modes, 0, int(self._instructions[self._curr_instruction + 1]))
                operand2 = self._give_param_val(parameters_modes, 1, int(self._instructions[self._curr_instruction + 2]))
                destination = int(self._instructions[self._curr_instruction + 3])
                if operand1 < operand2:
                    self._instructions[destination] = str(1)
                else:
                    self._instructions[destination] = str(0)
                self._curr_instruction = self._curr_instruction + 4
            elif opcode == 8:  # eq
                operand1 = self._give_param_val(parameters_modes, 0, int(self._instructions[self._curr_instruction + 1]))
                operand2 = self._give_param_val(parameters_modes, 1, int(self._instructions[self._curr_instruction + 2]))
                destination = int(self._instructions[self._curr_instruction + 3])
                if operand1 == operand2:
                    self._instructions[destination] = str(1)
                else:
                    self._instructions[destination] = str(0)
                self._curr_instruction = self._curr_instruction + 4
            else:
                print(f'Unknown opcode {opcode}')
                exit()
        return [stop_cause, output_vals]

    def solve1(self):
        self.process_input()

        phase_settings = permutations([str(_) for _ in range(5)])
        phase_settings_results = []

        for phase_setting in phase_settings:
            current_output = "0"
            for phase in phase_setting:
                self.reset_machine()
                current_output = self._compute_program(False, [phase, current_output])[1][0]
            phase_settings_results.append(int(current_output))
        print(f"Part 1: {max(phase_settings_results)}")

    def solve2(self):
        self.process_input()

        phase_settings = permutations([str(_ + 5) for _ in range(5)])
        phase_settings_results = []

        amplifiers = [Day7() for _ in range(0, 5)]
        for amp in amplifiers:
            amp.process_input()

        for phase_setting in phase_settings:
            current_e_out = ""
            current_signal = "0"
            for i, amp in enumerate(amplifiers):
                amp.reset_machine()
                amp._compute_program(False, [phase_setting[i]], True)

            stabilized_flag = False
            while not stabilized_flag:
                for amp in amplifiers:
                    output = amp._compute_program(False, [current_signal], False)
                    current_signal = output[1][0]
                    reason = output[0]
                    if reason != ReturnCause.input_empty_stop:
                        stabilized_flag = True
                    current_e_out = current_signal

            phase_settings_results.append(int(current_e_out))
        print(f"Part 2: {max(phase_settings_results)}")

if __name__ == "__main__":
    dayPart1 = Day7()
    dayPart1.solve1()
    dayPart2 = Day7()
    dayPart2.solve2()
