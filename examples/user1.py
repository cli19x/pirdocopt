"""Perfect

Usage:
  user1.py ship new <name>
  user1.py ship <name> move <x> <y> [--speed=<kn>]
  user1.py ship shoot <x> <y>
  user1.py mine (set|remove) <x> <y> [--moored | --drifting]
  user1.py (-h | --help)
  user1.py --version

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

# user1.py ship shoot <x> <y>
if __name__ == '__main__':
    arguments = docopt(__doc__, version="test 2.0", help_message=False, argv=None)
    print("this is the total dictionary:")
    print(arguments)

