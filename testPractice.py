"""Perfect

Usage:
  naval_fate.py ship new <name>
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
  -s KN  Speed in knots [default: 10].
  --aaa=<file>      Moored (anchored) mine [default: 20].
  --yyy    Drifting mine.

"""

from docopt import docopt
import unittest

class TestUsage(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_no_closed_bracket(self):
        doc = '''Usage:
            naval_fate.py ship (new <name>

        Options:
            -h --help --helping --haha -hhh --ooooo  Show this screen.
        '''
        self.assertRaises(Exception, docopt, doc)

    def test_too_few_args(self):
        args = ['ship', 'new']
        self.assertRaises(Exception, docopt, __doc__, args=args)


if __name__ == "__main__":
    unittest.main()