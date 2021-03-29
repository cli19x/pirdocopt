"""
   module for unit test of res = old_docopt.py
"""
import docopt as docopt

doc0 = """Perfect

Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]

Options:
  -h --help --helping --haha -hhh --ooooo  Show this screen.
  -o FILE --output=<value>  Speed in knots [default: ./test.txt].
  --speed=<kn> -s KN  Speed in knots [default: 10].

"""


#################################################################################
#################################################################################
# Main function test
def test_docopt():
    res = docopt.docopt(doc=doc0, version="test 2.0", help_message=False,
                        argv=['ship', 'Titanic', 'move', 10, 90, '--speed=70'])
    after = {'ship': True, 'new': False, '<name>...': False, 'name': 'Titanic', 'move': True,
             'x': 10, 'y': 90, '--helping': False, '--output': './test.txt', '--speed': 70}
    print(after)
    assert after == res


def test_get_patterns_and_dict():
    res = docopt.get_patterns_and_dict(usages=None)


def test_is_num():
    res = docopt.is_num(arg=None)


def test_build_tree_heads():
    res = docopt.build_tree_heads(pattern=None, tree_heads=None)


def test_dict_populate_loop(pattern):
    res = docopt.dict_populate_loop(pattern=None)


def test_identify_tokens():
    res = docopt.identify_tokens(pattern=None)


def test_create_opt_and_req():
    res = docopt.create_opt_and_req(pattern=None)


def test_create_mutex():
    res = docopt.create_mutex(pattern=None)


def test_create_repeating():
    res = docopt.create_repeating(pattern=None)


def test_check_option_lines():
    res = docopt.check_option_lines(options=None)


def test_check_option_lines_long():
    res = docopt.check_option_lines_long(element=None, tmp_array=None, count=0, token=None)


def test_check_option_lines_short():
    res = docopt.check_option_lines_short(element=None, tmp_array=None, count=0, token=None)


def find_default_value(line, token):
    res = docopt.find_default_value(line="", token=None)
