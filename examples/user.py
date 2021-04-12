"""Perfect

Usage:
  user.py ship new <name>
  user.py ship <name> move <x> <y> [--speed=<kn>]
  user.py ship shoot <x> <y>
  user.py mine (set|remove) <x> <y> [--moored | --drifting]
  user.py (-h | --help)
  user.py --version

Options:
  -h --help Show this screen.
  --sorted  Show sorted.
  -o FILE --output=<file>  Speed in knots [default: ./test.txt].
  --version     Show version.
  --speed=<kn> -s KN  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
  --rr     Show version.
  --aaa=<file>      Moored (anchored) mine [default: 20].
  --yyy    Drifting mine.

"""

from docopt import docopt

# user.py mine (set|remove) <x> <y> [--moored | --drifting]
if __name__ == '__main__':
    arguments = docopt(__doc__, version="test 2.0", help_message=False,
                       argv=['mine', 'set', '50', '200', '--moored'])
    print("this is the total dictionary:")
    print(arguments)
