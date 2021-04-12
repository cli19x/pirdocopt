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
        #print(x, y)
        assert x.__class__ == y.__class__
        if isinstance(x, docopt.Branch):
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


# Test function for building the usage patterns and a output dictionary from docstrings
def test_get_heads_and_dict():
    usages = ['  user_program.py ship new <name>... ', '  \
        user_program.py ship <name> move <x> <y> [--speed=<kn>]',
              '  user_program.py (-h | --help)']
    options_list = ['Options:', '  -h --help Show this screen.',
                    '  -o FILE --output=<value>  Speed in knots [default: ./test.txt].',
                    '  --speed=<kn> -s KN  Speed in knots [default: 10].']
    usage_dic, tree_heads = docopt.get_heads_and_dict(usages, options_list)

    test_heads = [docopt.Command('ship', False), docopt.Required(
        [docopt.Mutex([docopt.Option('--help', value=False),
                       docopt.Option('--help', value=False)])])]
    test_children = [docopt.Command('new', False), docopt.Argument('<name>', None)]
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
    pat1 = [docopt.Command("ship"), docopt.Command("new"), docopt.Argument("<name>")]
    pat2 = [docopt.Command("ship"), docopt.Argument("<name>"), docopt.Command("move")]
    pat3 = [docopt.Mutex([docopt.Option("-h"), docopt.Option("--help")])]
    pat1[0].post = pat1[1]
    pat2[0].post = pat2[1]

    test = [docopt.Command("ship"), docopt.Mutex([docopt.Option("-h"), docopt.Option("--help")])]
    test_children = [docopt.Command("new"), docopt.Argument("<name>")]

    tree_heads = []
    tree_heads = docopt.build_tree_heads(pat1, tree_heads)
    tree_heads = docopt.build_tree_heads(pat2, tree_heads)
    tree_heads = docopt.build_tree_heads(pat3, tree_heads)

    check_loop(test, tree_heads)
    check_loop(test_children, tree_heads[0].children)


# Test function for recursive function for building patterns
def test_dict_populate_loop():
    pat = [docopt.Command("set"), docopt.Mutex([docopt.Argument("<file>"),
                                                docopt.Option("--speed=<k>")]),
           docopt.Option("--sort=<kn>"),
           docopt.Optional([docopt.Option("-o")])]
    test = {"set": False, "<file>": None, "--speed": 0, "--sort": None, "-o": False}
    res = docopt.dict_populate_loop(pat)
    assert res == test


# Test function for identifying keywords and put them into tokens
def test_identify_tokens():
    pat = ['mine', '(', 'set', '|', 'remove', ')',
           '<x>', '<y>', '[', '--moored', '|', '--drifting', ']']
    test = [docopt.Command('mine', False), docopt.RequiredOpen(), docopt.Command('set', False),
            docopt.Pipe(), docopt.Command('remove', False), docopt.RequiredClosed(),
            docopt.Argument('<x>', 0), docopt.Argument('<y>', 0),
            docopt.OptionalOpen(), docopt.Option('--moored', value=False),
            docopt.Pipe(), docopt.Option('--drifting', value=False), docopt.OptionalClosed()]
    opt_pat = ['Options:', '--moored      Moored (anchored) mine.',
               '  --drifting    Drifting mine.']
    opt_pat = docopt.check_option_lines(opt_pat)
    res = docopt.identify_tokens(pat, opt_pat)

    for x, y in zip(test, res):
        assert x.__class__ == y.__class__
        if not isinstance(x, docopt.SpecialToken):
            # print(x.__class__, x.text, x.value)
            assert x.text == y.text
            assert x.value == y.value


# Test function for creating options tokens and required tokens
def test_create_opt_and_req():
    pat = [docopt.RequiredOpen(), docopt.Command("set"), docopt.OptionalOpen(),
           docopt.Command("remove"), docopt.OptionalClosed(), docopt.RequiredClosed(),
           docopt.Argument("<file>"), docopt.OptionalOpen(), docopt.Option("-o"),
           docopt.OptionalClosed()]
    test = [docopt.Required([docopt.Command("set"), docopt.Optional(
        [docopt.Command("remove")])]), docopt.Argument("<file>"),
            docopt.Optional([docopt.Option("-o")])]
    set_prev_post(pat)
    docopt.create_opt_and_req(pat)
    check_loop(test, pat)


# Test function for creating mutex tokens from options, command and other types of tokens
def test_create_mutex():
    pat = [docopt.Required([docopt.Required([docopt.Command("set"), docopt.Option("--aflame")]),
                            docopt.Pipe(), docopt.Command("cool")])]
    test = [docopt.Required(
        [docopt.Mutex([docopt.Required([docopt.Command("set"), docopt.Option("--aflame")]),
                       docopt.Command("cool")])])]
    pat[0].tokens[1].prev = pat[0].tokens[0]
    pat[0].tokens[1].post = pat[0].tokens[2]
    docopt.create_mutex(pat)
    check_loop(test, pat)


# Test function for repeat parameters
def test_create_repeating():
    pat = [docopt.Command("set"),
           docopt.Required([docopt.Argument("<file1>"), docopt.Argument("<file2>")]),
           docopt.Repeats()]
    test = [docopt.Command("set"), docopt.Repeating(
        [docopt.Required([docopt.Argument("<file1>"), docopt.Argument("<file2>")])])]
    pat[2].prev = pat[1]
    docopt.create_repeating(pat)
    check_loop(test, pat)


# Test If matching option and keyword is working correctly
def test_get_match_option():
    options_pat = docopt.check_option_lines(options=options.split('\n'))
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
    after = docopt.Option('--help', value=False, has_value=False, short='-h', long='--help')
    assert after.text == res[0].text
    assert after.value == res[0].value
    assert after.has_value == res[0].has_value
    assert after.short == res[0].short
    assert after.long == res[0].long

    res = docopt.check_option_lines(options=['-v=<input> --value=<input> User input value.'])
    after = docopt.Option('--value', value=None, has_value=True, short='-v', long='--value')
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
    after = docopt.Option('--help', value=False, has_value=False, short=None, long='--help')
    assert res.text == after.text
    assert res.long == after.long
    assert res.value == after.value
    assert res.has_value is False

    tmp_array = ['-h', '--help', 'Show', 'help', 'message']
    token = docopt.Option('-h', value=False, has_value=False, short='-h', long=None)
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=1, token=token)
    assert res.long == '--help'

    element = '--value=<input>'
    tmp_array = ['--value=<input>', '-v=<input>', 'User', 'input', 'value.']
    token = None
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=0, token=token)
    after = docopt.Option('--value', value=None, has_value=True, short=None, long='--value')
    assert res.text == after.text
    assert res.long == after.long
    assert res.value == after.value
    assert res.has_value is True

    tmp_array = ['-v=<input>', '--value=<input>', 'User', 'input', 'value.']
    token = docopt.Option('-v', value=None, has_value=True, short='-v', long=None)
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=1, token=token)
    assert res.long == '--value'

    element = '--speed'
    tmp_array = '--speed KN -s KN User input speed.'.split()
    token = None
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=0, token=token)
    after = docopt.Option('--speed', value=None, has_value=True, short=None, long='--speed')
    assert res.text == after.text
    assert res.long == after.long
    assert res.value == after.value
    assert res.has_value is True

    tmp_array = '-s KN --speed KN User input speed.'.split()
    token = docopt.Option('-s', value=None, has_value=True, short='-s', long='--speed')
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=1, token=token)
    assert res.long == '--speed'


# Test function for building the short version keywords into the Option object
def test_check_option_lines_short():
    element = '-h'
    tmp_array = ['-h', '--help', 'Show', 'help', 'message']
    token = None
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=0,
                                          token=token)
    after = docopt.Option('-h', value=False, has_value=False, short='-h', long=None)
    assert res.text == after.text
    assert res.short == after.short
    assert res.value == after.value
    assert res.has_value is False

    tmp_array = ['--help', '-h', 'Show', 'help', 'message']
    token = docopt.Option('--help', value=False, has_value=False, short=None, long='--help')
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=1,
                                          token=token)
    assert res.short == '-h'

    element = '-v=<input>'
    tmp_array = ['-v=<input>', '--value=<input>', 'User', 'input', 'value.']
    token = None
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=0,
                                          token=token)
    after = docopt.Option('-v', value=None, has_value=True, short='-v', long=None)
    assert res.text == after.text
    assert res.short == after.short
    assert res.value == after.value
    assert res.has_value is True

    tmp_array = ['--value=<input>', '-v=<input>', 'User', 'input', 'value.']
    token = docopt.Option('--value', value=None, has_value=True, short=None, long='--value')
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=1,
                                          token=token)
    assert res.short == '-v'

    element = '-s'
    tmp_array = '-s KN --speed KN User input speed [default: 10].'.split()
    token = None
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=0,
                                          token=token)
    after = docopt.Option('-s', value=None, has_value=True, short='-s', long=None)
    assert res.text == after.text
    assert res.short == after.short
    assert res.value == after.value
    assert res.has_value is True

    tmp_array = '--speed KN -s KN User input speed [default: 10].'.split()
    token = docopt.Option('--speed', value=10, has_value=True, short=None, long='--speed')
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=1,
                                          token=token)
    assert res.short == '-s'


# Test function for finding and inserting the default value for option keyword
def find_default_value():
    tmp_token = docopt.Option('-v', value=None, has_value=True, short='-v', long=None)
    tmp_token = docopt.find_default_value('-v FILE input file [default: ./test.txt].', tmp_token)
    assert tmp_token.value == './test.txt'

    tmp_token = docopt.Option('--location', value=None, has_value=True,
                              short='-l', long='--location')
    tmp_token = docopt.find_default_value('-l=<location_value> --location=<location_value> '
                                          'insert coordinate [default: 10.88].', tmp_token)
    assert tmp_token.value == 10.88

    tmp_token = docopt.Option('--speed', value=None, has_value=True,
                              short='-s', long='--speed')
    tmp_token = docopt.find_default_value('--speed KN -s KN input speed [default: 20].', tmp_token)
    assert tmp_token.value == 20
