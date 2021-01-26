"""Perfect

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
from docopt import docopt


def testing_parentheses(array):
    pass


def testing_usages(array):
    pass


def testing_options(array):
    pass


if __name__ == '__main__':
    testing = docopt(__doc__, version="test 2.0", help_message=False,
                     argv=['--help', '--moored'])
    print(testing)


