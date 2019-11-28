import argparse


class DayBase:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("file", type=argparse.FileType('r'), help="test file to use")
        args = parser.parse_args()
        self._file = args.file
