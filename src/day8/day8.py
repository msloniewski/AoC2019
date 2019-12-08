import sys, os, re
sys.path.insert(0, os.path.abspath('..'))
from common.DayBase import DayBase


class Day8(DayBase):

    def __init__(self):
        super(Day8, self).__init__()
        self._width = 25
        self._height = 6
        self._layers = []
        self._layer_size = self._width * self._height

    def process_input(self):
        pixels = self._file.readline()
        pixels = re.sub(r"\s*", "", pixels)
        for i in range(0, int(len(pixels) / self._layer_size)):
            self._layers.append(pixels[i * self._layer_size:(i + 1) * self._layer_size])

    def solve1(self):
        self.process_input()

        layer_num_of_zeroes = []
        for i, layer in enumerate(self._layers):
            num_of_zeroes = layer.count('0')
            layer_num_of_zeroes.append([i, num_of_zeroes])

        found_layer = min(layer_num_of_zeroes, key=lambda x: x[1])

        num_of_ones = self._layers[found_layer[0]].count("1")
        num_of_twos = self._layers[found_layer[0]].count("2")

        print(f"part1: {num_of_ones * num_of_twos}")

    def solve2(self):
        self.process_input()
        print(f"part2:")

        image = ["2"] * self._layer_size

        for layer in self._layers:
            for i, pixel in enumerate(image):
                if pixel == "2":
                    image[i] = layer[i]

        for i in range(0, self._height):
            line = []
            for pixel in image[i*self._width:(i+1)*self._width]:
                if pixel == "1":
                    line.append(u"\u2588")
                else:
                    line.append(" ")
            print("".join(line))


if __name__ == "__main__":
    dayPart1 = Day8()
    dayPart1.solve1()
    dayPart2 = Day8()
    dayPart2.solve2()
