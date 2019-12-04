import sys, os, re
sys.path.insert(0, os.path.abspath('..'))
from common.DayBase import DayBase


class Day4(DayBase):

    def __init__(self):
        super(Day4, self).__init__()
        self._down_range = None
        self._range = None
        self._up_range = None

    def process_input(self):
        self._range = self._file.readline()
        splitted = re.split('-', self._range)
        self._down_range = int(splitted[0])
        self._up_range = int(splitted[1])

    def solve1(self):
        self.process_input()

        number_of_possible_pass = 0

        for i in range (self._down_range, self._up_range + 1):
            repeat_cond = False
            rising_cond = True

            val = str(i)
            prev_val = int(val[0])
            for j in range(1, len(val)):
                if int(val[j]) == prev_val:
                    repeat_cond = True
                if int(val[j]) < prev_val:
                    rising_cond = False
                prev_val = int(val[j])

            if rising_cond and repeat_cond:
                number_of_possible_pass = number_of_possible_pass + 1

        print(f"part1: {number_of_possible_pass}")

    def solve2(self):
        self.process_input()

        number_of_possible_pass = 0

        for i in range (self._down_range, self._up_range + 1):
            rising_cond = True
            streak_cond = False

            val = str(i)
            prev_val = int(val[0])
            streak = 1
            for j in range(1, len(val)):
                if int(val[j]) == prev_val:
                    streak = streak + 1
                else:
                    if streak != 1 and streak / 2 == 1:
                        streak_cond = True
                    streak = 1
                if int(val[j]) < prev_val:
                    rising_cond = False
                prev_val = int(val[j])

            if streak != 1 and streak / 2 == 1:
                streak_cond = True

            if rising_cond and streak_cond:
                number_of_possible_pass = number_of_possible_pass + 1

        print(f"part2: {number_of_possible_pass}")


if __name__ == "__main__":
    dayPart1 = Day4()
    dayPart1.solve1()
    dayPart2 = Day4()
    dayPart2.solve2()
