"""
   module for unit test of res = old_docopt.py
"""
import pytest

from pirdocopt import docopt_util as du, docopt

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
  -h --help Show this screen.
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
  -h --help Show this screen.
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
  -h --help Show this screen.
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

  -h --help Show this screen.
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

  -h --help Show this screen.
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

options_2 = """  -h --help Show this screen.
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
  -h --help Show this screen.
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
  -h --help Show this screen.
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

min_case = """Usage: naval_fate.py ship new <name>..."""


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
        assert x.__class__ == y.__class__
        if isinstance(x, du.Branch):
            check_loop(x.tokens, y.tokens)
        else:
            assert x.text == y.text
            assert x.value == y.value


def set_post(pat):
    for i, p in enumerate(pat):
        if i < len(pat) - 1:
            p.post = pat[i + 1]


def test_class():
    tk = du.Token(prev=None, post=None, children=None)
    assert len(tk.children) == 0
    assert tk.name == "Token"
    assert tk.get_class == du.Token

    lf = du.Leaf('test', value=None, prev=None, post=None, children=None)
    assert len(lf.children) == 0
    assert lf.flat().text == 'test'
    assert lf.__repr__() == 'Leaf(\'test\', None)'

    ar = du.Argument('test', prev=None, post=None, children=None)
    assert ar.get_res_dict(False) == {}

    op = du.Option('test', value=None, has_value=False, short=None,
                   long=None, prev=None, post=None, children=None)
    op.match(['test', '2', '3'], 0)
    assert op.value is True
    assert op.get_res_dict(False) == {}


def test_branch():
    br = du.Branch(tokens=None, prev=None, post=None, children=None)
    assert len(br.tokens) == 0
    assert len(br.flat()) == 0
    assert isinstance(br.flat(du.Branch), du.Branch)
    assert br.flat(du.Token()) == []
    br.tokens.append('11')
    assert br.__repr__() == 'Branch(\'11\')'

    re = du.Required()
    re.tokens = [du.Argument('test'), du.Argument('1'), du.Argument('2'), du.Argument('3')]
    args = ['test', '1', '2', '3']
    is_match, child_index, _ = re.match(args, 0)
    assert is_match is True
    assert child_index == 4
    re.tokens = [du.Argument('no'), du.Argument('5'), du.Argument('6'), du.Argument('7')]
    args = []
    is_match, child_index, _ = re.match(args, 0)
    assert is_match is False
    assert child_index == 0

    mu = du.Mutex()
    mu.tokens = [du.Argument('test'), du.Argument('1'), du.Argument('2'), du.Argument('3')]
    args = ['test', '1', '2', '3']
    is_match, child_index, _ = mu.match(args, 0)
    assert is_match is True
    assert child_index == 1
    mu.tokens = [du.Argument('no'), du.Argument('5'), du.Argument('6'), du.Argument('7')]
    args = []
    is_match, child_index, _ = mu.match(args, 0)
    assert is_match is False
    assert child_index == 1

    rs = du.Repeating()
    rs.tokens = [du.Argument('test'), du.Argument('1'), du.Argument('2'), du.Argument('3')]
    args = ['test', '1', '2', '3']
    is_match, child_index, _ = rs.match(args, 0)
    assert is_match is True
    assert child_index == 4
    rs.tokens = [du.Command('no'), du.Command('5'), du.Command('6'), du.Command('7')]
    args = ['no', 777]
    is_match, child_index, _ = rs.match(args, 0)
    assert is_match is True
    assert child_index == 1

    rs.tokens = [du.Command('no'), du.Command('5'), du.Command('6'), du.Command('7')]
    args = ['haha', '777']
    is_match, child_index, _ = rs.match(args, 0)
    assert is_match is False
    assert child_index == 1

    ol = du.Optional()
    ol.tokens = [du.Argument('test'), du.Argument('1'), du.Argument('2'), du.Argument('3')]
    args = ['test', '1', '2', '3']
    is_match, child_index, _ = ol.match(args, 0)
    assert is_match is True
    assert child_index == 4
    ol.tokens = [du.Argument('no'), du.Argument('5'), du.Argument('6'), du.Argument('7')]
    args = []
    is_match, child_index, _ = ol.match(args, 0)
    assert is_match is True
    assert child_index == 0


def test_special_token():
    st = du.SpecialToken()
    assert st.name == "SpecialToken"
    assert st.get_class == du.SpecialToken

    op = du.OptionalOpen()
    assert op.name == "OptionalOpen"
    assert op.get_class == du.OptionalOpen

    oc = du.OptionalClosed()
    assert oc.name == "OptionalClosed"
    assert oc.get_class == du.OptionalClosed

    ro = du.RequiredOpen()
    assert ro.name == "RequiredOpen"
    assert ro.get_class == du.RequiredOpen

    rc = du.RequiredClosed()
    assert rc.name == "RequiredClosed"
    assert rc.get_class == du.RequiredClosed

    pi = du.Pipe()
    assert pi.name == "Pipe"
    assert pi.get_class == du.Pipe

    rp = du.Repeats()
    assert rp.name == "Repeats"
    assert rp.get_class == du.Repeats

    assert du.is_num("haha") is False


#################################################################################
#################################################################################
# Main function test
def test_docopt():
    res = docopt.docopt(doc=doc0, version="test 2.0", help_message=False,
                        argv=[])
    after = {'ship': False, 'new': False, '<name>': None, 'move': False,
             '<x>': 0, '<y>': 0, '--speed': 10, '--help': False}
    assert after == res

    res2 = docopt.docopt(doc=min_case, version="test 2.0", help_message=False,
                         argv=['ship', 'new', 'Titanic'])
    after = {'ship': False, 'new': False, '<name>': None}

    assert after == res2


# Test function for processing string
@pytest.mark.filterwarnings("ignore:api v1")
def test_processing_string(capsys):
    usage_array, options_array, _ = docopt.processing_string(
        doc=doc1, help_message=False, version="test 2.0")
    assert usage.split('\n') == usage_array
    assert options.split('\n') == options_array

    res = docopt.processing_string(doc=None, help_message=False, version="test 2.0")
    assert res is None

    usage_array, options_array, _ = docopt.processing_string(
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

    tmp_name, tmp_usage, tmp_options, display = \
        docopt.get_usage_and_options(doc=doc2, version=version)
    assert tmp_name == ""
    assert tmp_usage == usage
    assert tmp_options == options

    tmp_name, tmp_usage, tmp_options, display = \
        docopt.get_usage_and_options(doc=doc1, version=None)
    assert tmp_name == name
    assert tmp_usage == usage
    assert tmp_options == options

    tmp_name, tmp_usage, tmp_options, display = \
        docopt.get_usage_and_options(doc=doc2, version=None)
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
    assert tmp_options == options_2

    tmp_name, tmp_usage, tmp_options, display = \
        docopt.get_usage_and_options(doc=doc5, version=version)
    assert tmp_name == name
    assert tmp_usage == usage
    assert tmp_options == options_2

    with pytest.raises(du.DocoptExit):
        docopt.get_usage_and_options(doc=doc5, version=[])


# Test if the warnings will cause the function to return a correct integer value
@pytest.mark.filterwarnings("ignore:api v1")
def test_check_warnings():
    res = docopt.check_warnings(usage=usage, options=options)
    assert res == 0

    res = docopt.check_warnings(usage="", options=options)
    assert res == 1

    res = docopt.check_warnings(usage=usage, options="")
    assert res == 2


def test_get_child_match():
    pat1 = [du.Argument("<name>"), du.Command("move"),
            du.Argument("<x>"),
            du.Argument("<y>"),
            du.Optional([du.Option("--speed", 10, has_value=True)])]
    pat2 = [du.Command("new"), du.Repeating([du.Argument("<name>")])]
    set_post(pat1)
    set_post(pat2)
    args1 = ['ship', 'Titanic', 'move', 10, 90, '--speed', 70]
    args2 = ['ship', 'new', 'Boaty', 'Titanic', 'Boat2']
    args3 = ['ship', 'Boat']
    orig_head_dict = {'ship': True}

    head_dict = orig_head_dict
    assert docopt.get_child_match([pat1[0], pat2[0]], args1, 1, head_dict)
    assert head_dict == {'ship': True, '<name>': 'Titanic', 'move': True, '<x>': 10, '<y>': 90,
                         '--speed': 70}

    head_dict = {'ship': True}
    assert docopt.get_child_match([pat1[0], pat2[0]], args2, 1, head_dict)
    assert head_dict == {'ship': True, 'new': True, '<name>': ['Boaty', 'Titanic', 'Boat2']}

    head_dict = {'ship': True}
    assert docopt.get_child_match([pat1[0], pat2[0]], args3, 1, head_dict) is False
    assert head_dict == {'ship': True}

    assert docopt.get_child_match([], args3, 1, head_dict) is True


def test_match_user_input():
    pat1 = [du.Argument("<name>"), du.Command("move"),
            du.Argument("<x>"),
            du.Argument("<y>"),
            du.Optional([du.Option("--speed", 10, has_value=True)])]
    pat2 = [du.Command("new"), du.Repeating([du.Argument("<name>")])]
    res = docopt.match_user_input([pat1[0], pat2[0]], {}, ['new'])
    assert res == {'<name>': 'new'}


def test_get_post_match():
    pat = [du.Argument("<name>"), du.Command("move"), du.Argument("<x>"),
           du.Argument("<y>"),
           du.Optional([du.Option("--speed", 10, has_value=True)])]
    set_post(pat)
    args1 = ['ship', 'Titanic', 'move', 10, 90, '--speed', 70]
    orig_index = 2
    index = 2
    orig_child_dict = {'<name>': "Titanic"}
    child_dict = orig_child_dict

    assert docopt.get_post_match(pat[0], args1, index, child_dict)
    assert child_dict == {'<name>': 'Titanic', 'move': True, '<x>': 10, '<y>': 90, '--speed': 70}

    args2 = ['ship', 'Boaty', 'shoot', 10, 90]
    assert docopt.get_post_match(pat[0], args2, orig_index, orig_child_dict) is False


# Test function for building the usage patterns and a output dictionary from docstrings
def test_get_heads_and_dict():
    usages = ['  user_program.py ship new <name>... ', '  \
        user_program.py ship <name> move <x> <y> [--speed=<kn>]',
              '  user_program.py (-h | --help)']

    speed = du.Option('--speed', False, has_value=True, short='-s', long='--speed')
    speed.value = 10
    options_pat = [du.Option('--help', value=False, has_value=False, short='-h', long='--help'),
                   speed]

    usage_dic, tree_heads = docopt.get_heads_and_dict(usages, options_pat)
    test_heads = [du.Command('ship', False), du.Required(
        [du.Mutex([du.Option('--help', value=False),
                   du.Option('--help', value=False)])])]
    test_children = [du.Command('new', False), du.Argument('<name>', None)]
    test_dic = {'ship': False, 'new': False, '<name>': None,
                'move': False, '<x>': 0, '<y>': 0, '--speed': 10, '--help': False}

    check_loop(test_heads, tree_heads)
    check_loop(test_children, tree_heads[0].children)
    assert test_dic == usage_dic


# Test function for identifying if the input is a number
def test_is_num():
    assert du.is_num("5") is True
    assert du.is_num("0.87") is True
    assert du.is_num("-4.2") is True
    assert du.is_num("x") is False
    assert du.is_num("argument") is False


# Test function for building correct tree structure for the matching process
def test_build_tree_heads():
    pat1 = [du.Command("ship"), du.Command("new"), du.Argument("<name>")]
    pat2 = [du.Command("ship"), du.Argument("<name>"),
            du.Command("move")]
    pat3 = [du.Mutex([du.Option("-h"), du.Option("--help")])]
    pat1[0].post = pat1[1]
    pat2[0].post = pat2[1]

    test = [du.Command("ship"), du.Mutex([du.Option("-h"),
                                          du.Option("--help")])]
    test_children = [du.Command("new"), du.Argument("<name>")]

    tree_heads = []
    tree_heads = docopt.build_tree_heads(pat1, tree_heads)
    tree_heads = docopt.build_tree_heads(pat2, tree_heads)
    tree_heads = docopt.build_tree_heads(pat3, tree_heads)

    check_loop(test, tree_heads)
    check_loop(test_children, tree_heads[0].children)


# Test function for recursive function for building patterns
def test_dict_populate_loop():
    pat = [du.Command("set"), du.Mutex([du.Argument("<file>"),
                                        du.Option("--speed=<k>")]),
           du.Option("--sort=<kn>"),
           du.Optional([du.Option("-o")])]
    test = {"set": False, "<file>": None, "--speed": 0, "--sort": None, "-o": False}
    res = docopt.dict_populate_loop(pat)
    assert res == test

    pat = [du.SpecialToken()]
    res = docopt.dict_populate_loop(pat)
    assert res == {}


# Test function for identifying keywords and put them into tokens
def test_identify_tokens():
    pat = ['mine', '(', 'set', '|', 'remove', ')',
           '<x>', '<y>', '[', '--moored', '|', '--drifting', ']']
    test = [du.Command('mine', False), du.RequiredOpen(),
            du.Command('set', False),
            du.Pipe(), du.Command('remove', False), du.RequiredClosed(),
            du.Argument('<x>', 0), du.Argument('<y>', 0),
            du.OptionalOpen(), du.Option('--moored', value=False),
            du.Pipe(), du.Option('--drifting', value=False),
            du.OptionalClosed()]
    opt_pat = ['Options:', '--moored      Moored (anchored) mine.',
               '  --drifting    Drifting mine.']
    opt_pat = docopt.check_option_lines(opt_pat)
    res = docopt.identify_tokens(pat, opt_pat)

    for x, y in zip(test, res):
        assert x.__class__ == y.__class__
        if not isinstance(x, du.SpecialToken):
            # print(x.__class__, x.text, x.value)
            assert x.text == y.text
            assert x.value == y.value


# Test function for creating options tokens and required tokens
def test_create_opt_and_req():
    pat = [du.RequiredOpen(), du.Command("set"), du.OptionalOpen(),
           du.Command("remove"), du.OptionalClosed(),
           du.RequiredClosed(),
           du.Argument("<file>"), du.OptionalOpen(), du.Option("-o"),
           du.OptionalClosed()]
    test = [du.Required([du.Command("set"), du.Optional(
        [du.Command("remove")])]), du.Argument("<file>"),
            du.Optional([du.Option("-o")])]
    set_prev_post(pat)
    docopt.create_opt_and_req(pat)
    check_loop(test, pat)


# Test function for creating mutex tokens from options, command and other types of tokens
def test_create_mutex():
    pat = [du.Required(
        [du.Required([du.Command("set"), du.Option("--aflame")]),
         du.Pipe(), du.Command("cool")])]
    test = [du.Required(
        [du.Mutex(
            [du.Required([du.Command("set"), du.Option("--aflame")]),
             du.Command("cool")])])]
    pat[0].tokens[1].prev = pat[0].tokens[0]
    pat[0].tokens[1].post = pat[0].tokens[2]
    docopt.create_mutex(pat)
    check_loop(test, pat)


# Test function for repeat parameters
def test_create_repeating():
    pat = [du.Command("set"),
           du.Required([du.Argument("<file1>"), du.Argument("<file2>")]),
           du.Repeats()]
    test = [du.Command("set"), du.Repeating(
        [du.Required([du.Argument("<file1>"), du.Argument("<file2>")])])]
    pat[2].prev = pat[1]
    docopt.create_repeating(pat)
    check_loop(test, pat)


# Test If matching option and keyword is working correctly
def test_get_match_option():
    # text, value = None, has_value = False, short = None,
    # long = None, prev = None, post = None, children = None
    options_pat = [du.Option('--help', False, has_value=False, short='-h', long='--help'),
                   du.Option('--sorted', False, has_value=False, short=None, long='--sorted'),
                   du.Option('--output', './test.txt', has_value=True, short='-o', long='--output'),
                   du.Option('--www', False, has_value=False, short='-w', long='--www'),
                   du.Option('--hello', False, has_value=False, short=None, long='--hello')]

    assert docopt.get_match_option('--help', options_pat) is not None
    assert docopt.get_match_option('--output=<value>', options_pat) is not None
    assert docopt.get_match_option('-h', options_pat) is not None

    assert docopt.get_match_option('--www', options_pat) is not None
    assert docopt.get_match_option('--hello', options_pat) is not None
    options_pat = [None]
    assert docopt.get_match_option('--test_empty', options_pat) is not None


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

    res = docopt.create_tmp_token('hello', False)
    assert res is None


# Test function for paring the options lines into array of option tokens
def test_check_option_lines():
    res = docopt.check_option_lines(options=['-h --help Show Help Message.'])
    after = du.Option('--help', value=False, has_value=False, short='-h', long='--help')
    assert after.text == res[0].text
    assert after.value == res[0].value
    assert after.has_value == res[0].has_value
    assert after.short == res[0].short
    assert after.long == res[0].long

    res = docopt.check_option_lines(options=['-v=<input> --value=<input> User input value.'])
    after = du.Option('--value', value=None, has_value=True, short='-v', long='--value')
    assert after.text == res[0].text
    assert after.value == res[0].value
    assert after.has_value == res[0].has_value
    assert after.short == res[0].short
    assert after.long == res[0].long

    res = docopt.check_option_lines(options=['-s KN --speed KN User input speed [default: 10].'])
    after = du.Option('--speed', value=10, has_value=True, short='-s', long='--speed')
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
    after = du.Option('--help', value=False, has_value=False, short=None, long='--help')
    assert res.text == after.text
    assert res.long == after.long
    assert res.value == after.value
    assert res.has_value is False

    tmp_array = ['-h', '--help', 'Show', 'help', 'message']
    token = du.Option('-h', value=False, has_value=False, short='-h', long=None)
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=1, token=token)
    assert res.long == '--help'

    element = '--value=<input>'
    tmp_array = ['--value=<input>', '-v=<input>', 'User', 'input', 'value.']
    token = None
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=0, token=token)
    after = du.Option('--value', value=None, has_value=True, short=None, long='--value')
    assert res.text == after.text
    assert res.long == after.long
    assert res.value == after.value
    assert res.has_value is True

    tmp_array = ['-v=<input>', '--value=<input>', 'User', 'input', 'value.']
    token = du.Option('-v', value=None, has_value=True, short='-v', long=None)
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=1, token=token)
    assert res.long == '--value'

    element = '--speed'
    tmp_array = '--speed KN -s KN User input speed.'.split()
    token = None
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=0, token=token)
    after = du.Option('--speed', value=None, has_value=True, short=None, long='--speed')
    assert res.text == after.text
    assert res.long == after.long
    assert res.value == after.value
    assert res.has_value is True

    tmp_array = '-s KN --speed KN User input speed.'.split()
    token = du.Option('-s', value=None, has_value=True, short='-s', long='--speed')
    res = docopt.check_option_lines_long(element=element, tmp_array=tmp_array, count=1, token=token)
    assert res.long == '--speed'


# Test function for building the short version keywords into the Option object
def test_check_option_lines_short():
    element = '-h'
    tmp_array = ['-h', '--help', 'Show', 'help', 'message']
    token = None
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=0,
                                          token=token)
    after = du.Option('-h', value=False, has_value=False, short='-h', long=None)
    assert res.text == after.text
    assert res.short == after.short
    assert res.value == after.value
    assert res.has_value is False

    tmp_array = ['--help', '-h', 'Show', 'help', 'message']
    token = du.Option('--help', value=False, has_value=False, short=None, long='--help')
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=1,
                                          token=token)
    assert res.short == '-h'

    element = '-v=<input>'
    tmp_array = ['-v=<input>', '--value=<input>', 'User', 'input', 'value.']
    token = None
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=0,
                                          token=token)
    after = du.Option('-v', value=None, has_value=True, short='-v', long=None)
    assert res.text == after.text
    assert res.short == after.short
    assert res.value == after.value
    assert res.has_value is True

    tmp_array = ['--value=<input>', '-v=<input>', 'User', 'input', 'value.']
    token = du.Option('--value', value=None, has_value=True, short=None, long='--value')
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=1,
                                          token=token)
    assert res.short == '-v'

    element = '-s'
    tmp_array = '-s KN --speed KN User input speed [default: 10].'.split()
    token = None
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=0,
                                          token=token)
    after = du.Option('-s', value=None, has_value=True, short='-s', long=None)
    assert res.text == after.text
    assert res.short == after.short
    assert res.value == after.value
    assert res.has_value is True

    tmp_array = '--speed KN -s KN User input speed [default: 10].'.split()
    token = du.Option('--speed', value=10, has_value=True, short=None, long='--speed')
    res = docopt.check_option_lines_short(element=element, tmp_array=tmp_array, count=1,
                                          token=token)
    assert res.short == '-s'


# Test function for finding and inserting the default value for option keyword
def test_find_default_value():
    tmp_token = du.Option('-v', value=None, has_value=True, short='-v', long=None)
    tmp_token = docopt.find_default_value('-v FILE input file [default: ./test.txt].', tmp_token)
    assert tmp_token.value == './test.txt'

    tmp_token = du.Option('--location', value=None, has_value=True,
                          short='-l', long='--location')
    tmp_token = docopt.find_default_value('-l=<location_value> --location=<location_value> '
                                          'insert coordinate [default: 10.88].', tmp_token)
    assert tmp_token.value == 10.88

    tmp_token = du.Option('--speed', value=None, has_value=True,
                          short='-s', long='--speed')
    tmp_token = docopt.find_default_value('--speed KN -s KN input speed [default: 20].',
                                          tmp_token)
    assert tmp_token.value == 20


##############################################################################
##############################################################################
# Test print function
def test_print_output_dictionary():
    input1 = {'1': True, '2': 'haha', '3': False, '4': True, '5': 'haha', '6': False,
              '7': True, '8': 'haha', '9': False, '10': True, '11': 'haha', '12': False,
              '13': True, '14': 'haha', '15': False, '16': True, '17': 'haha', '18': False,
              '19': True, '20': 'haha', '21': False, '22': True, '23': 'haha', '24': False,
              '25': True, '26': 'haha', '27': False, '28': True, '29': 'haha', '30': False}
    usage_dic = {'usage1': 'x', 'usage2': 'y'}
    dic_total, res = docopt.print_output_dictionary(usage_dic=usage_dic)
    assert dic_total == {**usage_dic, **dic_total}
    dic_total, res = docopt.print_output_dictionary(usage_dic=input1)
    assert dic_total == input1


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


