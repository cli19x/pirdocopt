"""Perfect

Usage:
  user2.py ship new <name>
  user2.py ship <name> move <x> <y> [--speed=<kn>]
  user2.py ship shoot <x> <y>
  user2.py mine (set|remove) <x> <y> [--moored | --drifting]
  user2.py (-h | --help)
  user2.py --version

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

# user2.py ship new <name>
if __name__ == '__main__':
    arguments = docopt(__doc__, version="version 2.0", help_message=True, argv=None)
    print("this is the total dictionary:")
    print(arguments)

# if __name__ == '__main__':
#     arguments = docopt(__doc__, version=None, help_message=True, argv=None)
#     print("this is the total dictionary:")
#     print(arguments)
