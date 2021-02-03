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

import pytest
from docopt import docopt

# Test for exception raised when usage pattern contains unmatched parenthesis/bracket
def test_no_closed_bracket():
  doc = __doc__
  doc = doc.replace("new", "(new", 1)
  with pytest.raises(Exception) as exc_info:
    res = docopt(doc, argv=['ship', 'new', 'boat'])
  assert exc_info.value.args[0] == "Could not find closed paren or bracket."

# Test for when input matches first few tokens of a pattern but stops short
def test_too_few_input_tokens():
  doc = __doc__
  with pytest.raises(Exception) as exc_info:
    res = docopt(doc, argv=['ship', 'new'])
  assert exc_info.value.args[0] == "No matching usage pattern found."

# Test for when input matches a pattern but contains extraneous tokens at the end
def test_too_many_input_tokens():
  doc = __doc__
  with pytest.raises(Exception) as exc_info:
    res = docopt(doc, argv=['ship', 'new', 'Boat', 'extra'])
  assert exc_info.value.args[0] == "No matching usage pattern found."

# Test for when input contains more than one tokens that are mutually exclusive to each other
def test_more_than_one_mutex():
  doc = __doc__
  with pytest.raises(Exception) as exc_info:
    res = docopt(doc, argv=['mine', 'set', 'remove', '50', '100', '--moored'])
  assert exc_info.value.args[0] == "No matching usage pattern found."

# Test to check if we skip missing optional tokens
def test_skip_optional_token():
  doc = __doc__
  