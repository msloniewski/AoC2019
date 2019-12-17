import sys, os, re, math
import functools
sys.path.insert(0, os.path.abspath('..'))
from common.DayBase import DayBase


class Substrate:

    def __init__(self, name="", amount=0):
        self.name = name
        self.amount = amount


class Reaction:

    def __init__(self, result, substrates):
        self.substrates = substrates
        self.result = result


class Day14(DayBase):

    def __init__(self):
        super(Day14, self).__init__()
        self.reactions = []
        self._amount_needed_per_one_fuel = []

    def _find_reaction(self, product):
        for reaction in self.reactions:
            if reaction.result.name == product.name:
                return reaction

    @staticmethod
    def add_substrate(substrates, new_substrate):
        inserted = False

        for substrate in substrates:
            if substrate.name == new_substrate.name:
                substrate.amount = substrate.amount + new_substrate.amount
                inserted = True

        if not inserted:
            substrates.append(new_substrate)

        return substrates

    def process_input(self):
        for line in self._file.readlines():
            sides = re.split(r"=>", line)
            result = Substrate()
            result.amount = int(re.findall(r"\d+", sides[1])[0])
            filtered = re.sub(r"\s*", "", sides[1])
            filtered = re.sub(r"\d+", "", filtered)
            result.name = filtered

            substrates = []
            for substrate in re.split(r",", sides[0]):
                element = Substrate()
                element.amount = int(re.findall(r"\d+", substrate)[0])
                filtered = re.sub(r"\s*", "", substrate)
                filtered = re.sub(r"\d+", "", filtered)
                element.name = filtered
                substrates.append(element)

            self.reactions.append(Reaction(result, substrates))

    def is_sub_needed_somewhere_else(self, substrate, substrates):
        needed = []
        for other_substrate in substrates:
            if other_substrate.name != substrate:
                reaction_needed = self._find_reaction(other_substrate)
                if reaction_needed:
                    for substrate_needed in reaction_needed.substrates:
                        if substrate_needed.name == substrate.name:
                            return True
                    needed.append(self.is_sub_needed_somewhere_else(substrate, reaction_needed.substrates))
                else:
                    needed.append(False)
        return functools.reduce(lambda x, y: x or y, needed)

    def _solve(self, what, how_much):
        substrates_needed = [Substrate(what, how_much)]

        only_needed_ore = False
        while not only_needed_ore:
            only_needed_ore = True
            for substrate_needed in substrates_needed:
                if substrate_needed.name != "ORE":
                    reaction_needed = self._find_reaction(substrate_needed)
                    if not self.is_sub_needed_somewhere_else(substrate_needed, substrates_needed):
                        only_needed_ore = False
                        reaction_result_amount = reaction_needed.result.amount
                        needed_amount = substrate_needed.amount
                        times_reaction = math.ceil(needed_amount / reaction_result_amount)
                        self._amount_needed_per_one_fuel.append([substrate_needed.name,
                                                                 substrate_needed.amount * times_reaction])

                        for ingredient in reaction_needed.substrates:
                            sub_to_add = Substrate(ingredient.name, ingredient.amount * times_reaction)
                            substrates_needed = self.add_substrate(substrates_needed, sub_to_add)
                        substrates_needed.remove(substrate_needed)
        return substrates_needed[0].amount

    def solve1(self):
        self.process_input()

        ans = self._solve("FUEL", 1)

        print(f"part1: {ans}")

    def solve2(self):
        self.process_input()

        target = int(1e12)
        lower_bound = 0
        upper_bound = target

        changed = True
        center = 0
        while changed:
            changed = False
            center = (lower_bound + upper_bound) // 2
            result = self._solve("FUEL", center)
            if result >= target:
                if upper_bound != center:
                    upper_bound = center
                    changed = True
            if result <= target:
                if lower_bound != center:
                    changed = True
                    lower_bound = center
            print (lower_bound, upper_bound)

        print(f"part2: {center}")


if __name__ == "__main__":
    dayPart1 = Day14()
    dayPart1.solve1()
    dayPart2 = Day14()
    dayPart2.solve2()
