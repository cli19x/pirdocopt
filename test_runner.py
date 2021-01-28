import os
import subprocess

doc = """Perfect

Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
  naval_fate.py ship shoot <x> <y>
  naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]
  naval_fate.py (-h | --help)
  naval_fate.py --version

Options:
  -h --help --helping --haha -hhh --ooooo  Show this screen.
  --sorted  Show sorted.
  -o FILE --output=<file>  Speed in knots [default: ./test.txt].
  --version     Show version.
  --speed=<kn> -s KN  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
  --rr     Show version.
  --fff=<tt> -s KN  Speed in knots.
  --aaa=<file>      Moored (anchored) mine [default: haha.pdf].
  --yyy    Drifting mine.

"""

argv = ['--help', '--moored', '--output=default.pdf']


def testing_usages(res, ans):
    pass


def testing_options(res, ans):
    for el, r in zip(res, ans):
        el = el.strip()
        if ':' in el:
            value = el.split(':')[1].strip()
            try:
                assert value == r
            except str:
                print(f"error unexpected value: {value}")
    pass


if __name__ == '__main__':
    input_cmd = "python test.py"
    results = subprocess.check_output(input_cmd, shell=True).decode()
    answers = ['True', 'False']
    testing_usages(results, answers)
    testing_options(results, answers)

