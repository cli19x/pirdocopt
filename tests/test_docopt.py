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
    res = docopt.check_option_lines(options='-h --help Show Help Message.')
    after = docopt.Option('-h', False, has_value=False, short='-h', long='--help')
    print(res)
    assert after == res

    res = docopt.check_option_lines(options='-v=<input> --value=<input> User input value.')
    after = docopt.Option('-v', None, has_value=True, short='-v', long='--value')
    print(res)
    assert after == res

    res = docopt.check_option_lines(options='-s KN --speed KN User input speed [default: 10].')
    after = docopt.Option('-s', 10, has_value=True, short='-s', long='--speed')
    print(res)
    assert after == res


def test_check_option_lines_long():
    element = '--help'
    tmp_array = ['--help', '-h', 'Show', 'help', 'message']
    token = None
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=0, token=token)
    after = docopt.Option('--help', False, has_value=False, short=None, long='--help')
    assert res == after

    tmp_array = ['-h', '--help', 'Show', 'help', 'message']
    token = docopt.Option('-h', False, has_value=False, short='-h', long=None)
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=1, token=token)
    assert res.long == '--help'

    element = '--value=<input>'
    tmp_array = ['--value=<input>', '-v=<input>', 'User', 'input', 'value.']
    token = None
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=0, token=token)
    after = docopt.Option('--value', None, has_value=True, short=None, long='--value')
    assert res == after

    tmp_array = ['-v=<input>', '--value=<input>', 'User', 'input', 'value.']
    token = docopt.Option('-v', None, has_value=True, short='-v', long=None)
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=1, token=token)
    assert res.long == '--value'

    element = '--speed'
    tmp_array = '--speed KN -s KN User input speed.'.split()
    token = None
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=0, token=token)
    after = docopt.Option('--speed', None, has_value=True, short=None, long='--speed')
    assert res == after

    tmp_array = '-s KN --speed KN User input speed.'.split()
    token = docopt.Option('-s', None, has_value=True, short='-s', long='--speed')
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=1, token=token)
    assert res.long == '--speed'


def test_check_option_lines_short():
    element = '-h'
    tmp_array = ['-h', '--help', 'Show', 'help', 'message']
    token = None
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=0, token=token)
    after = docopt.Option('-h', False, has_value=False, short='-h', long=None)
    assert res == after

    tmp_array = ['--help', '-h', 'Show', 'help', 'message']
    token = docopt.Option('--help', False, has_value=False, short=None, long='--help')
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=1, token=token)
    assert res.short == '-h'

    element = '-v=<input>'
    tmp_array = ['-v=<input>', '--value=<input>', 'User', 'input', 'value.']
    token = None
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=0, token=token)
    after = docopt.Option('-v', None, has_value=True, short='-v', long=None)
    assert res == after

    tmp_array = ['--value=<input>', '-v=<input>', 'User', 'input', 'value.']
    token = docopt.Option('--value', None, has_value=True, short=None, long='--value')
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=1, token=token)
    assert res.short == '-v'

    element = '-s'
    tmp_array = '-s KN --speed KN User input speed [default: 10].'.split()
    token = None
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=0, token=token)
    after = docopt.Option('-s', None, has_value=True, short='-s', long=None)
    assert res == after

    tmp_array = '--speed KN -s KN User input speed [default: 10].'.split()
    token = docopt.Option('--speed', 10, has_value=True, short=None, long='--speed')
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=1, token=token)
    assert res.short == '-s'


def find_default_value():
    tmp_token = docopt.Option('-v', None, True, '-v', None)
    tmp_token = docopt.find_default_value('-v FILE input file [default: ./test.txt].', tmp_token)
    after = docopt.Option('-v', './test.txt', True, '-v', None)
    assert tmp_token == after

    tmp_token = docopt.Option('--location', None, True, '-l', '--location')
    tmp_token = docopt.find_default_value('-l=<location_value> --location=<location_value> '
                                          'insert coordinate [default: 10.88].', tmp_token)
    after = docopt.Option('--location', 10.88, True, '-l', '--location')
    assert tmp_token == after

    tmp_token = docopt.Option('--speed', None, True, '-s', '--speed')
    tmp_token = docopt.find_default_value('--speed KN -s KN input speed [default: 20].', tmp_token)
    after = docopt.Option('--speed', 20, True, '-s', '--speed')
    assert tmp_token == after
