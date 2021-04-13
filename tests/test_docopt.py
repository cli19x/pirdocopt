"""
   module for unit test of res = old_docopt.py
"""
import pytest

import docopt as docopt
import docopt_util

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
  -h --help --helping  Show this screen.
  --sorted  Show sorted.
  -o FILE --output=<value>  Speed in knots [default: ./test.txt].
  --version     Show version.
  --speed=<kn> -s KN  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
  --rr     Show version.
  --aaa=<value>      Moored (anchored) mine [default: 20].
  --yyy    Drifting mine."""

doc1 = """Perfect

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
  -o FILE --output=<value>  Speed in knots [default: ./test.txt].
  --version     Show version.
  --speed=<kn> -s KN  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
  --rr     Show version.
  --aaa=<value>      Moored (anchored) mine [default: 20].
  --yyy    Drifting mine.

"""

doc2 = """Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
  naval_fate.py ship shoot <x> <y>
  naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]
  naval_fate.py (-h | --help)
  naval_fate.py --version

Options:
  -h --help --helping --haha -hhh --ooooo  Show this screen.
  --sorted  Show sorted.
  -o FILE --output=<value>  Speed in knots [default: ./test.txt].
  --version     Show version.
  --speed=<kn> -s KN  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
  --rr     Show version.
  --aaa=<value>      Moored (anchored) mine [default: 20].
  --yyy    Drifting mine.

"""

doc3 = """Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
  naval_fate.py ship shoot <x> <y>
  naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]
  naval_fate.py (-h | --help)
  naval_fate.py --version

"""

doc4 = """

Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
  naval_fate.py ship shoot <x> <y>
  naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]
  naval_fate.py (-h | --help)
  naval_fate.py --version

  -h --help --helping --haha -hhh --ooooo  Show this screen.
  --sorted  Show sorted.
  -o FILE --output=<value>  Speed in knots [default: ./test.txt].
  --version     Show version.
  --speed=<kn> -s KN  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
  --rr     Show version.
  --aaa=<value>      Moored (anchored) mine [default: 20].
  --yyy    Drifting mine.

"""

doc5 = """Perfect

Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
  naval_fate.py ship shoot <x> <y>
  naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]
  naval_fate.py (-h | --help)
  naval_fate.py --version

  -h --help --helping --haha -hhh --ooooo  Show this screen.
  --sorted  Show sorted.
  -o FILE --output=<value>  Speed in knots [default: ./test.txt].
  --version     Show version.
  --speed=<kn> -s KN  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
  --rr     Show version.
  --aaa=<value>      Moored (anchored) mine [default: 20].
  --yyy    Drifting mine.

"""

argv = ['--help', '--moored', '--output=ttt.pdf']

name = """Perfect"""

usage = """Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
  naval_fate.py ship shoot <x> <y>
  naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]
  naval_fate.py (-h | --help)
  naval_fate.py --version"""

options_2 = """  -h --help --helping --haha -hhh --ooooo  Show this screen.
  --sorted  Show sorted.
  -o FILE --output=<value>  Speed in knots [default: ./test.txt].
  --version     Show version.
  --speed=<kn> -s KN  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
  --rr     Show version.
  --aaa=<value>      Moored (anchored) mine [default: 20].
  --yyy    Drifting mine."""

options_3 = """Options:
  -h --help  Show this screen.
  --sorted  Show sorted.
  -o FILE --output=<value>  Speed in knots [default: ./test.txt].
  --version     Show version."""

version = """test 2.1"""

help1 = """Perfect

Version:
  test 2.1

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
  -o FILE --output=<value>  Speed in knots [default: ./test.txt].
  --version     Show version.
  --speed=<kn> -s KN  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
  --rr     Show version.
  --aaa=<value>      Moored (anchored) mine [default: 20].
  --yyy    Drifting mine.

testing

"""

help2 = """Perfect

Version:


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
  -o FILE --output=<value>  Speed in knots [default: ./test.txt].
  --version     Show version.
  --speed=<kn> -s KN  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
  --rr     Show version.
  --aaa=<value>      Moored (anchored) mine [default: 20].
  --yyy    Drifting mine.

testing

"""

other = "testing"


#################################################################################
# Helper functions

def set_prev_post(pat):
    for index, token in enumerate(pat):
        if index == 0:
            token.post = pat[index + 1] if len(pat) > 1 else None
        elif index == len(pat) - 1:
            token.prev = pat[index - 1]
        else:
            token.prev = pat[index - 1]
            token.post = pat[index + 1]


def check_loop(test, pat):
    for x, y in zip(test, pat):
        # print(x, y)
        assert x.__class__ == y.__class__
        if isinstance(x, docopt_util.Branch):
            check_loop(x.tokens, y.tokens)
        else:
            assert x.text == y.text
            assert x.value == y.value


#################################################################################
#################################################################################
# Main function test
def test_docopt():
    res = docopt.docopt(doc=doc0, version="test 2.0", help_message=False,
                        argv=['ship', 'Titanic', 'move', 10, 90, '--speed', 70])
    after = {'ship': True, 'new': False, '<name>': 'Titanic', 'move': True,
             '<x>': 10, '<y>': 90, '--speed': 70, '--help': False}

    assert after == res


# Test function for processing string
@pytest.mark.filterwarnings("ignore:api v1")
def test_processing_string(capsys):
    usage_array, options_array = docopt.processing_string(
        doc=doc1, help_message=False, version="test 2.0")
    assert usage.split('\n') == usage_array
    assert options.split('\n') == options_array
    print(usage_array)
    print(options_array)

    res = docopt.processing_string(doc=None, help_message=False, version="test 2.0")
    assert res is None

    usage_array, options_array = docopt.processing_string(
        doc=doc1, help_message=True, version="test 2.0")
    assert usage.split('\n') == usage_array
    assert options.split('\n') == options_array
    captured = capsys.readouterr()
    assert len(captured.out) > 0


# Test getting the usage and options strings from docstring
def test_get_usage_and_options():
    tmp_name, tmp_usage, tmp_options, display = \
        docopt.get_usage_and_options(doc=doc1, version=version)
    assert tmp_name == name
    assert tmp_usage == usage
    assert tmp_options == options
    print(display)

    tmp_name, tmp_usage, tmp_options, display = \
        docopt.get_usage_and_options(doc=doc2, version=version)
    assert tmp_name == ""
    assert tmp_usage == usage
    assert tmp_options == options

    tmp_name, tmp_usage, tmp_options, display = \
        docopt.get_usage_and_options(doc=doc3, version=version)
    assert tmp_name == ""
    assert tmp_usage == usage
    assert tmp_options == ""

    tmp_name, tmp_usage, tmp_options, display = \
        docopt.get_usage_and_options(doc=doc4, version=version)
    assert tmp_name == ""
    assert tmp_usage == usage
    print(tmp_options)
    print(options_2)
    assert tmp_options == options_2

    tmp_name, tmp_usage, tmp_options, display = \
        docopt.get_usage_and_options(doc=doc5, version=version)
    assert tmp_name == name
    assert tmp_usage == usage
    assert tmp_options == options_2


# Test if the warnings will cause the function to return a correct integer value
@pytest.mark.filterwarnings("ignore:api v1")
def test_check_warnings():
    res = docopt.check_warnings(usage=usage, options=options)
    assert res == 0

    res = docopt.check_warnings(usage="", options=options)
    assert res == 1

    res = docopt.check_warnings(usage=usage, options="")
    assert res == 2


# Test function for building the usage patterns and a output dictionary from docstrings
def test_get_heads_and_dict():
    usages = ['  user_program.py ship new <name>... ', '  \
        user_program.py ship <name> move <x> <y> [--speed=<kn>]',
              '  user_program.py (-h | --help)']
    options_list = ['Options:', '  -h --help Show this screen.',
                    '  -o FILE --output=<value>  Speed in knots [default: ./test.txt].',
                    '  --speed=<kn> -s KN  Speed in knots [default: 10].']
    usage_dic, tree_heads = docopt.get_heads_and_dict(usages, options_list)

    test_heads = [docopt_util.Command('ship', False), docopt_util.Required(
        [docopt_util.Mutex([docopt_util.Option('--help', value=False),
                            docopt_util.Option('--help', value=False)])])]
    test_children = [docopt_util.Command('new', False), docopt_util.Argument('<name>', None)]
    test_dic = {'ship': False, 'new': False, '<name>': None,
                'move': False, '<x>': 0, '<y>': 0, '--speed': 10, '--help': False}

    check_loop(test_heads, tree_heads)
    check_loop(test_children, tree_heads[0].children)
    assert test_dic == usage_dic


# Test function for identifying if the input is a number
def test_is_num():
    assert docopt.is_num("5") is True
    assert docopt.is_num("0.87") is True
    assert docopt.is_num("-4.2") is True
    assert docopt.is_num("x") is False
    assert docopt.is_num("argument") is False


# Test function for building correct tree structure for the matching process
def test_build_tree_heads():
    pat1 = [docopt_util.Command("ship"), docopt_util.Command("new"), docopt_util.Argument("<name>")]
    pat2 = [docopt_util.Command("ship"), docopt_util.Argument("<name>"),
            docopt_util.Command("move")]
    pat3 = [docopt_util.Mutex([docopt_util.Option("-h"), docopt_util.Option("--help")])]
    pat1[0].post = pat1[1]
    pat2[0].post = pat2[1]

    test = [docopt_util.Command("ship"), docopt_util.Mutex([docopt_util.Option("-h"),
                                                            docopt_util.Option("--help")])]
    test_children = [docopt_util.Command("new"), docopt_util.Argument("<name>")]

    tree_heads = []
    tree_heads = docopt.build_tree_heads(pat1, tree_heads)
    tree_heads = docopt.build_tree_heads(pat2, tree_heads)
    tree_heads = docopt.build_tree_heads(pat3, tree_heads)

    check_loop(test, tree_heads)
    check_loop(test_children, tree_heads[0].children)


# Test function for recursive function for building patterns
def test_dict_populate_loop():
    pat = [docopt_util.Command("set"), docopt_util.Mutex([docopt_util.Argument("<file>"),
                                                          docopt_util.Option("--speed=<k>")]),
           docopt_util.Option("--sort=<kn>"),
           docopt_util.Optional([docopt_util.Option("-o")])]
    test = {"set": False, "<file>": None, "--speed": 0, "--sort": None, "-o": False}
    res = docopt.dict_populate_loop(pat)
    assert res == test


# Test function for identifying keywords and put them into tokens
def test_identify_tokens():
    pat = ['mine', '(', 'set', '|', 'remove', ')',
           '<x>', '<y>', '[', '--moored', '|', '--drifting', ']']
    test = [docopt_util.Command('mine', False), docopt_util.RequiredOpen(),
            docopt_util.Command('set', False),
            docopt_util.Pipe(), docopt_util.Command('remove', False), docopt_util.RequiredClosed(),
            docopt_util.Argument('<x>', 0), docopt_util.Argument('<y>', 0),
            docopt_util.OptionalOpen(), docopt_util.Option('--moored', value=False),
            docopt_util.Pipe(), docopt_util.Option('--drifting', value=False),
            docopt_util.OptionalClosed()]
    opt_pat = ['Options:', '--moored      Moored (anchored) mine.',
               '  --drifting    Drifting mine.']
    opt_pat = docopt.check_option_lines(opt_pat)
    res = docopt.identify_tokens(pat, opt_pat)

    for x, y in zip(test, res):
        assert x.__class__ == y.__class__
        if not isinstance(x, docopt_util.SpecialToken):
            # print(x.__class__, x.text, x.value)
            assert x.text == y.text
            assert x.value == y.value


# Test function for creating options tokens and required tokens
def test_create_opt_and_req():
    pat = [docopt_util.RequiredOpen(), docopt_util.Command("set"), docopt_util.OptionalOpen(),
           docopt_util.Command("remove"), docopt_util.OptionalClosed(),
           docopt_util.RequiredClosed(),
           docopt_util.Argument("<file>"), docopt_util.OptionalOpen(), docopt_util.Option("-o"),
           docopt_util.OptionalClosed()]
    test = [docopt_util.Required([docopt_util.Command("set"), docopt_util.Optional(
        [docopt_util.Command("remove")])]), docopt_util.Argument("<file>"),
            docopt_util.Optional([docopt_util.Option("-o")])]
    set_prev_post(pat)
    docopt.create_opt_and_req(pat)
    check_loop(test, pat)


# Test function for creating mutex tokens from options, command and other types of tokens
def test_create_mutex():
    pat = [docopt_util.Required(
        [docopt_util.Required([docopt_util.Command("set"), docopt_util.Option("--aflame")]),
         docopt_util.Pipe(), docopt_util.Command("cool")])]
    test = [docopt_util.Required(
        [docopt_util.Mutex(
            [docopt_util.Required([docopt_util.Command("set"), docopt_util.Option("--aflame")]),
             docopt_util.Command("cool")])])]
    pat[0].tokens[1].prev = pat[0].tokens[0]
    pat[0].tokens[1].post = pat[0].tokens[2]
    docopt.create_mutex(pat)
    check_loop(test, pat)


# Test function for repeat parameters
def test_create_repeating():
    pat = [docopt_util.Command("set"),
           docopt_util.Required([docopt_util.Argument("<file1>"), docopt_util.Argument("<file2>")]),
           docopt_util.Repeats()]
    test = [docopt_util.Command("set"), docopt_util.Repeating(
        [docopt_util.Required([docopt_util.Argument("<file1>"), docopt_util.Argument("<file2>")])])]
    pat[2].prev = pat[1]
    docopt.create_repeating(pat)
    check_loop(test, pat)


# Test If matching option and keyword is working correctly
def test_get_match_option():
    options_pat = docopt.check_option_lines(options=options_3.split('\n'))
    assert docopt.get_match_option('--help', options_pat) is not None
    assert docopt.get_match_option('--output=<value>', options_pat) is not None
    assert docopt.get_match_option('-h', options_pat) is not None

    assert docopt.get_match_option('--www', options_pat) is not None
    assert docopt.get_match_option('--hello', options_pat) is not None


# Test If matching option and keyword is working correctly
def test_create_tmp_token():
    res = docopt.create_tmp_token('--hello', False)
    assert res.text == '--hello'
    assert res.long == '--hello'
    assert res.has_value is False

    res = docopt.create_tmp_token('-h', False)
    assert res.text == '-h'
    assert res.short == '-h'
    assert res.has_value is False

    res = docopt.create_tmp_token('--hello', True)
    assert res.text == '--hello'
    assert res.long == '--hello'
    assert res.has_value is True

    res = docopt.create_tmp_token('-h', True)
    assert res.text == '-h'
    assert res.short == '-h'
    assert res.has_value is True


# Test function for paring the options lines into array of option tokens
def test_check_option_lines():
    res = docopt.check_option_lines(options=['-h --help Show Help Message.'])
    after = docopt_util.Option('--help', value=False, has_value=False, short='-h', long='--help')
    assert after.text == res[0].text
    assert after.value == res[0].value
    assert after.has_value == res[0].has_value
    assert after.short == res[0].short
    assert after.long == res[0].long

    res = docopt.check_option_lines(options=['-v=<input> --value=<input> User input value.'])
    after = docopt_util.Option('--value', value=None, has_value=True, short='-v', long='--value')
    assert after.text == res[0].text
    assert after.value == res[0].value
    assert after.has_value == res[0].has_value
    assert after.short == res[0].short
    assert after.long == res[0].long

    res = docopt.check_option_lines(options=['-s KN --speed KN User input speed [default: 10].'])
    after = docopt_util.Option('--speed', value=10, has_value=True, short='-s', long='--speed')
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
    after = docopt_util.Option('--help', value=False, has_value=False, short=None, long='--help')
    assert res.text == after.text
    assert res.long == after.long
    assert res.value == after.value
    assert res.has_value is False

    tmp_array = ['-h', '--help', 'Show', 'help', 'message']
    token = docopt_util.Option('-h', value=False, has_value=False, short='-h', long=None)
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=1, token=token)
    assert res.long == '--help'

    element = '--value=<input>'
    tmp_array = ['--value=<input>', '-v=<input>', 'User', 'input', 'value.']
    token = None
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=0, token=token)
    after = docopt_util.Option('--value', value=None, has_value=True, short=None, long='--value')
    assert res.text == after.text
    assert res.long == after.long
    assert res.value == after.value
    assert res.has_value is True

    tmp_array = ['-v=<input>', '--value=<input>', 'User', 'input', 'value.']
    token = docopt_util.Option('-v', value=None, has_value=True, short='-v', long=None)
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=1, token=token)
    assert res.long == '--value'

    element = '--speed'
    tmp_array = '--speed KN -s KN User input speed.'.split()
    token = None
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=0, token=token)
    after = docopt_util.Option('--speed', value=None, has_value=True, short=None, long='--speed')
    assert res.text == after.text
    assert res.long == after.long
    assert res.value == after.value
    assert res.has_value is True

    tmp_array = '-s KN --speed KN User input speed.'.split()
    token = docopt_util.Option('-s', value=None, has_value=True, short='-s', long='--speed')
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=1, token=token)
    assert res.long == '--speed'


# Test function for building the short version keywords into the Option object
def test_check_option_lines_short():
    element = '-h'
    tmp_array = ['-h', '--help', 'Show', 'help', 'message']
    token = None
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=0,
                                          token=token)
    after = docopt_util.Option('-h', value=False, has_value=False, short='-h', long=None)
    assert res.text == after.text
    assert res.short == after.short
    assert res.value == after.value
    assert res.has_value is False

    tmp_array = ['--help', '-h', 'Show', 'help', 'message']
    token = docopt_util.Option('--help', value=False, has_value=False, short=None, long='--help')
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=1,
                                          token=token)
    assert res.short == '-h'

    element = '-v=<input>'
    tmp_array = ['-v=<input>', '--value=<input>', 'User', 'input', 'value.']
    token = None
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=0,
                                          token=token)
    after = docopt_util.Option('-v', value=None, has_value=True, short='-v', long=None)
    assert res.text == after.text
    assert res.short == after.short
    assert res.value == after.value
    assert res.has_value is True

    tmp_array = ['--value=<input>', '-v=<input>', 'User', 'input', 'value.']
    token = docopt_util.Option('--value', value=None, has_value=True, short=None, long='--value')
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=1,
                                          token=token)
    assert res.short == '-v'

    element = '-s'
    tmp_array = '-s KN --speed KN User input speed [default: 10].'.split()
    token = None
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=0,
                                          token=token)
    after = docopt_util.Option('-s', value=None, has_value=True, short='-s', long=None)
    assert res.text == after.text
    assert res.short == after.short
    assert res.value == after.value
    assert res.has_value is True

    tmp_array = '--speed KN -s KN User input speed [default: 10].'.split()
    token = docopt_util.Option('--speed', value=10, has_value=True, short=None, long='--speed')
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=1,
                                          token=token)
    assert res.short == '-s'


# Test function for finding and inserting the default value for option keyword
def find_default_value():
    tmp_token = docopt_util.Option('-v', value=None, has_value=True, short='-v', long=None)
    tmp_token = docopt.find_default_value('-v FILE input file [default: ./test.txt].', tmp_token)
    assert tmp_token.value == './test.txt'

    tmp_token = docopt_util.Option('--location', value=None, has_value=True,
                                   short='-l', long='--location')
    tmp_token = docopt.find_default_value('-l=<location_value> --location=<location_value> '
                                          'insert coordinate [default: 10.88].', tmp_token)
    assert tmp_token.value == 10.88

    tmp_token = docopt_util.Option('--speed', value=None, has_value=True,
                                   short='-s', long='--speed')
    tmp_token = docopt.find_default_value('--speed KN -s KN input speed [default: 20].',
                                          tmp_token)
    assert tmp_token.value == 20


##############################################################################
##############################################################################
# Test print function
def test_print_output_dictionary():
    input2 = {'1': True, '2': 'haha', '3': False, '4': True, '5': 'haha', '6': False,
              '7': True, '8': 'haha', '9': False, '10': True, '11': 'haha', '12': False}
    input3 = {'1': True, '2': 'haha', '3': False, '4': True, '5': 'haha', '6': False,
              '7': True, '8': 'haha', '9': False, '10': True, '11': 'haha', '12': False,
              '13': True, '14': 'haha', '15': False, '16': True, '17': 'haha', '18': False,
              '19': True, '20': 'haha', '21': False, '22': True, '23': 'haha', '24': False,
              '25': True, '26': 'haha', '27': False, '28': True, '29': 'haha', '30': False}
    usage_dic = {'usage1': 'x', 'usage2': 'y'}
    options_dic = {'options1': 'x', 'options2': 'y'}
    dic_total, res = docopt.print_output_dictionary(usage_dic=usage_dic)
    assert dic_total == {**usage_dic, **dic_total}
    dic_total, res = docopt.print_output_dictionary(usage_dic={})
    assert dic_total == input2
    dic_total, res = docopt.print_output_dictionary(usage_dic=input3)
    assert dic_total == {**input3, **options_dic}


# Test function for testing the function for outputting a correct format of dictionary according
# to the user arguments as well as the docstring
def test_output_formatter():
    dic = {'--helping': True, '--sorted': True, '--output': 'ttt.pdf', '--version': False,
           '--speed': 10,
           '--moored': True, '--drifting': None, '--rr': False, '--aaa': 20.9, '--yyy': False}
    after = "{'--helping': True         '--speed': 10          '--aaa': 20.9\n" + \
            " '--sorted': True          '--moored': True       '--yyy': False\n" + \
            " '--output': 'ttt.pdf'     '--drifting': None\n" + \
            " '--version': False        '--rr': False}\n"
    dic_list = list(dic)
    res = docopt.output_formatter(rows=4, length=len(dic_list), dic_list=dic_list,
                                  dictionary_total=dic)
    assert res == after


# Test function for the function on inserting the key value pairs into the output arrays
def test_insert_content():
    dic = {'--helping': True, '--sorted': None, '--output': 'ttt.pdf', '--speed': 10, '--aaa': 20.9}
    dic_list = list(dic)
    res = docopt.insert_content(dic_list=dic_list, idx=0, rows=0,
                                col_idx=0, dictionary_total=dic)
    assert '\'--helping\'' + ': ' + 'True' == res

    res = docopt.insert_content(dic_list=dic_list, idx=1, rows=0,
                                col_idx=0, dictionary_total=dic)
    assert '\'--sorted\'' + ': ' + 'None' == res

    res = docopt.insert_content(dic_list=dic_list, idx=2, rows=0,
                                col_idx=0, dictionary_total=dic)
    assert '\'--output\'' + ': ' + '\'ttt.pdf\'' == res

    res = docopt.insert_content(dic_list=dic_list, idx=3, rows=0,
                                col_idx=0, dictionary_total=dic)
    assert '\'--speed\'' + ': ' + '10' == res

    res = docopt.insert_content(dic_list=dic_list, idx=4, rows=0,
                                col_idx=0, dictionary_total=dic)
    assert '\'--aaa\'' + ': ' + '20.9' == res


# Test function for the function that check if the value provided is primitive type or a string
def test_check_value_type():
    res = docopt.check_value_type(value="hello world")
    assert not res

    res = docopt.check_value_type(value=10)
    assert res

    res = docopt.check_value_type(value=10.67)
    assert res

    res = docopt.check_value_type(value=None)
    assert res


# Test function for the function which will lineup the strings in the arrays in a correct way
def test_print_output_from_rows():
    col1 = [' 11', ' 2', ' 3', ' 4', ' 5']
    col2 = [' 1', ' 222', ' 3', ' 4', ' ']
    col3 = [' 1', ' 2', ' 3333', ' ', ' ']
    outputting = "{11     1       1\n" + \
                 " 2      222     2\n" + \
                 " 3      3       3333\n" + \
                 " 4      4\n" + \
                 " 5}\n"
    res = docopt.print_output_from_rows(col1=col1, col2=col2, col3=col3, num_rows=5)
    assert res == outputting
