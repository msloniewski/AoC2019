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


class Robot:

    def __init__(self):
        # right 0, up 1, left 2, down 3
        self.orientation = 1
        self.x = 0
        self.y = 0

    def turn_right(self):
        self.orientation = (self.orientation - 1) % 4

    def turn_left(self):
        self.orientation = (self.orientation + 1) % 4

    def move_forward(self):
        if self.orientation == 0:
            self.x = self.x + 1
        elif self.orientation == 1:
            self.y = self.y + 1
        elif self.orientation == 2:
            self.x = self.x - 1
        elif self.orientation == 3:
            self.y = self.y - 1


class Plate:

    def __init__(self):
        self.board = {}

    def get_color(self, x, y):
        if x in self.board:
            if y in self.board[x]:
                return self.board[x][y]
            else:
                return 0
        else:
            return 0

    def set_color(self, x, y, color):
        if x in self.board:
            self.board[x][y] = color
        else:
            new = {y: color}
            self.board[x] = new

    def get_painted_size(self):
        sum = 0
        for x in self.board:
            sum = sum + len(self.board[x])
        return sum

    def print_plate(self):
        for line in sorted(self.board.keys()):
            line_to_print = []
            for tile in sorted(self.board[line].keys()):
                while len(line_to_print) < tile:
                    line_to_print.append(" ")
                if self.board[line][tile] == 1:
                    line_to_print.append("\u2588")
                else:
                    line_to_print.append(" ")
            print("".join(line_to_print))


class Day11(DayBase):

    def __init__(self):
        super(Day11, self).__init__()
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

        robot = Robot()
        plate = Plate()

        run = True
        while run:
            stop_cause, output = self._compute_program(False, [plate.get_color(robot.x, robot.y)])
            if stop_cause == ReturnCause.program_stop:
                run = False
            plate.set_color(robot.x, robot.y, output[0])
            if output[1] == 0:
                robot.turn_left()
            else:
                robot.turn_right()
            robot.move_forward()


        print (plate.get_painted_size())
        print(f"Part 1: done")

    def solve2(self):
        self.process_input()

        robot = Robot()
        plate = Plate()

        plate.set_color(0, 0, 1)

        run = True
        while run:
            stop_cause, output = self._compute_program(False, [plate.get_color(robot.x, robot.y)])
            if stop_cause == ReturnCause.program_stop:
                run = False
            plate.set_color(robot.x, robot.y, output[0])
            if output[1] == 0:
                robot.turn_left()
            else:
                robot.turn_right()
            robot.move_forward()

        plate.print_plate()
        print(f"Part 2: done")

if __name__ == "__main__":
    dayPart1 = Day11()
    dayPart1.solve1()
    dayPart2 = Day11()
    dayPart2.solve2()
