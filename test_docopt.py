"""
   module for unit test of res = old_docopt.py
"""
import docopt as docopt

doc0 = """Perfect

Usage:
  user_program.py ship new <name>... 
  user_program.py ship <name> move <x> <y> [--speed=<kn>]
  user_program.py ship --help

Options:
  -h --help Show this screen.
  -o FILE --output=<value>  Speed in knots [default: ./test.txt].
  --speed=<kn> -s KN  Speed in knots [default: 10].

"""

options = """Options:
  -h --help  Show this screen.
  --sorted  Show sorted.
  -o FILE --output=<value>  Speed in knots [default: ./test.txt].
  --version     Show version."""


#################################################################################
#################################################################################
# Main function test
def test_docopt():
    res = docopt.docopt(doc=doc0, version="test 2.0", help_message=False,
                        argv=['ship', 'Titanic', 'move', 10, 90, '--speed', 70])
    after = {'ship': True, 'new': False, '<name>': 'Titanic', 'move': True,
             '<x>': 10, '<y>': 90, '--speed': 70, '--help': False}

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


# Test If matching option and keyword is working correctly
def test_get_match_option():
    options_pat = docopt.check_option_lines(options=options.split('\n'))
    print(options_pat)
    assert docopt.get_match_option('--help', options_pat) is not None
    assert docopt.get_match_option('--output=<value>', options_pat) is not None
    assert docopt.get_match_option('-h', options_pat) is not None

    assert docopt.get_match_option('--www', options_pat) is None
    assert docopt.get_match_option('--hello', options_pat) is None


# Test function for paring the options lines into array of option tokens
def test_check_option_lines():
    res = docopt.check_option_lines(options=['-h --help Show Help Message.'])
    after = docopt.Option('--help', False, has_value=False, short='-h', long='--help')
    assert after.text == res[0].text
    assert after.value == res[0].value
    assert after.has_value == res[0].has_value
    assert after.short == res[0].short
    assert after.long == res[0].long

    res = docopt.check_option_lines(options=['-v=<input> --value=<input> User input value.'])
    after = docopt.Option('--value', None, has_value=True, short='-v', long='--value')
    assert after.text == res[0].text
    assert after.value == res[0].value
    assert after.has_value == res[0].has_value
    assert after.short == res[0].short
    assert after.long == res[0].long

    res = docopt.check_option_lines(options=['-s KN --speed KN User input speed [default: 10].'])
    after = docopt.Option('--speed', value=10, has_value=True, short='-s', long='--speed')
    assert after.text == res[0].text
    assert 10 == res[0].value
    assert after.has_value == res[0].has_value
    assert after.short == res[0].short
    assert after.long == res[0].long


# Test function for building the long version keywords into the Option object
def test_check_option_lines_long():
    element = '--help'
    tmp_array = ['--help', '-h', 'Show', 'help', 'message']
    token = None
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=0, token=token)
    after = docopt.Option('--help', False, has_value=False, short=None, long='--help')
    assert res.text == after.text
    assert res.long == after.long
    assert res.value == after.value
    assert res.has_value is False

    tmp_array = ['-h', '--help', 'Show', 'help', 'message']
    token = docopt.Option('-h', False, has_value=False, short='-h', long=None)
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=1, token=token)
    assert res.long == '--help'

    element = '--value=<input>'
    tmp_array = ['--value=<input>', '-v=<input>', 'User', 'input', 'value.']
    token = None
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=0, token=token)
    after = docopt.Option('--value', None, has_value=True, short=None, long='--value')
    assert res.text == after.text
    assert res.long == after.long
    assert res.value == after.value
    assert res.has_value is True

    tmp_array = ['-v=<input>', '--value=<input>', 'User', 'input', 'value.']
    token = docopt.Option('-v', None, has_value=True, short='-v', long=None)
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=1, token=token)
    assert res.long == '--value'

    element = '--speed'
    tmp_array = '--speed KN -s KN User input speed.'.split()
    token = None
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=0, token=token)
    after = docopt.Option('--speed', None, has_value=True, short=None, long='--speed')
    assert res.text == after.text
    assert res.long == after.long
    assert res.value == after.value
    assert res.has_value is True

    tmp_array = '-s KN --speed KN User input speed.'.split()
    token = docopt.Option('-s', None, has_value=True, short='-s', long='--speed')
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=1, token=token)
    assert res.long == '--speed'


# Test function for building the short version keywords into the Option object
def test_check_option_lines_short():
    element = '-h'
    tmp_array = ['-h', '--help', 'Show', 'help', 'message']
    token = None
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=0,
                                          token=token)
    after = docopt.Option('-h', False, has_value=False, short='-h', long=None)
    assert res.text == after.text
    assert res.short == after.short
    assert res.value == after.value
    assert res.has_value is False

    tmp_array = ['--help', '-h', 'Show', 'help', 'message']
    token = docopt.Option('--help', False, has_value=False, short=None, long='--help')
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=1,
                                          token=token)
    assert res.short == '-h'

    element = '-v=<input>'
    tmp_array = ['-v=<input>', '--value=<input>', 'User', 'input', 'value.']
    token = None
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=0,
                                          token=token)
    after = docopt.Option('-v', None, has_value=True, short='-v', long=None)
    assert res.text == after.text
    assert res.short == after.short
    assert res.value == after.value
    assert res.has_value is True

    tmp_array = ['--value=<input>', '-v=<input>', 'User', 'input', 'value.']
    token = docopt.Option('--value', None, has_value=True, short=None, long='--value')
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=1,
                                          token=token)
    assert res.short == '-v'

    element = '-s'
    tmp_array = '-s KN --speed KN User input speed [default: 10].'.split()
    token = None
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=0,
                                          token=token)
    after = docopt.Option('-s', None, has_value=True, short='-s', long=None)
    assert res.text == after.text
    assert res.short == after.short
    assert res.value == after.value
    assert res.has_value is True

    tmp_array = '--speed KN -s KN User input speed [default: 10].'.split()
    token = docopt.Option('--speed', 10, has_value=True, short=None, long='--speed')
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=1,
                                          token=token)
    assert res.short == '-s'


# Test function for finding and inserting the default value for option keyword
def find_default_value():
    tmp_token = docopt.Option('-v', None, True, '-v', None)
    tmp_token = docopt.find_default_value('-v FILE input file [default: ./test.txt].', tmp_token)
    assert tmp_token.value == './test.txt'

    tmp_token = docopt.Option('--location', None, True, '-l', '--location')
    tmp_token = docopt.find_default_value('-l=<location_value> --location=<location_value> '
                                          'insert coordinate [default: 10.88].', tmp_token)
    assert tmp_token.value == 10.88

    tmp_token = docopt.Option('--speed', None, True, '-s', '--speed')
    tmp_token = docopt.find_default_value('--speed KN -s KN input speed [default: 20].', tmp_token)
    assert tmp_token.value == 20
