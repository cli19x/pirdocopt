"""
   module for unit test of res = docopt.py
"""
import docopt
import pytest

doc0 = """Perfect

Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]

Options:
  -h --help --helping --haha -hhh --ooooo  Show this screen.
  -o FILE --output=<value>  Speed in knots [default: ./test.txt].
  --speed=<kn> -s KN  Speed in knots [default: 10].

"""

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

options = """Options:
  -h --help --helping --haha -hhh --ooooo  Show this screen.
  --sorted  Show sorted.
  -o FILE --output=<value>  Speed in knots [default: ./test.txt].
  --version     Show version.
  --speed=<kn> -s KN  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
  --rr     Show version.
  --aaa=<value>      Moored (anchored) mine [default: 20].
  --yyy    Drifting mine."""

options_2 = """-h --help --helping --haha -hhh --ooooo  Show this screen.
  --sorted  Show sorted.
  -o FILE --output=<value>  Speed in knots [default: ./test.txt].
  --version     Show version.
  --speed=<kn> -s KN  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
  --rr     Show version.
  --aaa=<value>      Moored (anchored) mine [default: 20].
  --yyy    Drifting mine."""

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

"""


#################################################################################
#################################################################################
# Main function test
def test_docopt():
    res = docopt.docopt(doc=doc0, version="test 2.0", help_message=False,
                        argv=['ship', 'Titanic', 'move', 10, 90, '--speed=70'])
    after = {'ship': True, 'new': False, '<name>...': False, 'name': 'Titanic', 'move': True,
             'x': 10, 'y': 90, '--helping': False, '--output': './test.txt', '--speed': 70}
    assert after == res


# Test function for processing string
@pytest.mark.filterwarnings("ignore:api v1")
def test_processing_string(capsys):
    usage_array, options_array = docopt.processing_string(doc=doc1, help_message=False, version="test 2.0")
    assert usage.split('\n') == usage_array
    assert options.split('\n') == options_array

    res = docopt.processing_string(doc=None, help_message=False, version="test 2.0")
    assert res is None

    usage_array, options_array = docopt.processing_string(doc=doc1, help_message=True, version="test 2.0")
    assert usage.split('\n') == usage_array
    assert options.split('\n') == options_array
    captured = capsys.readouterr()
    assert len(captured.out) > 0


# Test getting the usage and options strings from docstring
def test_get_usage_and_options():
    tmp_name, tmp_usage, tmp_options = docopt.get_usage_and_options(doc=doc1)
    assert tmp_name == name
    assert tmp_usage == usage
    assert tmp_options == options

    tmp_name, tmp_usage, tmp_options = docopt.get_usage_and_options(doc=doc2)
    assert tmp_name == ""
    assert tmp_usage == usage
    assert tmp_options == options

    tmp_name, tmp_usage, tmp_options = docopt.get_usage_and_options(doc=doc3)
    assert tmp_name == ""
    assert tmp_usage == usage
    assert tmp_options == ""

    tmp_name, tmp_usage, tmp_options = docopt.get_usage_and_options(doc=doc4)
    assert tmp_name == ""
    assert tmp_usage == usage
    assert tmp_options == options_2

    tmp_name, tmp_usage, tmp_options = docopt.get_usage_and_options(doc=doc5)
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


# Test if help message will display to user correctly
def test_show_help():
    res = docopt.show_help(name=name, version=version, usage=usage, options=options)
    assert res == help1

    res = docopt.show_help(name=name, version="", usage=usage, options=options)
    assert res == help2


#################################################################################
#################################################################################
# # Usage function test
def test_usage_parser():
    usages = ['Usage:',
              "  naval_fate.py ship new <name>",
              "  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]",
              "  naval_fate.py ship shoot <x> <y>",
              "  naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]",
              "  naval_fate.py (-h | --help)",
              "  naval_fate.py --version"]

    args1 = ["ship", "new", "Boat"]
    args2 = ["ship", "new"]
    args3 = ["ship", "shoot", "50", "100"]
    args4 = ["ship", "Boat", "move", "50", "100"]
    args5 = ["mine", "set", "remove", "50", "100", "--drifting"]
    args6 = ["mine", "remove", "50", "100"]
    args7 = ["--help"]

    usage_dic_1 = docopt.usage_parser(usages.copy(), None, args1)
    assert usage_dic_1["ship"] is True and usage_dic_1["new"] is True and usage_dic_1["name"] == "Boat"

    with pytest.raises(Exception) as exc_info:
        res = docopt.usage_parser(usages.copy(), None, args2)
    assert exc_info.value.args[0] == "No matching usage pattern found."

    usage_dic_3 = docopt.usage_parser(usages.copy(), args3, None)
    assert usage_dic_3["ship"] is True and usage_dic_3["shoot"] is True and usage_dic_3["x"] == '50' and usage_dic_3[
        "y"] == '100'

    usage_dic_4 = docopt.usage_parser(usages.copy(), args4, None)
    assert usage_dic_3["ship"] is True and usage_dic_3["shoot"] is True and usage_dic_3["x"] == '50' and usage_dic_3[
        "y"] == '100'

    with pytest.raises(Exception) as exc_info:
        res = docopt.usage_parser(usages.copy(), None, args5)
    assert exc_info.value.args[0] == "No matching usage pattern found."

    usage_dic_6 = docopt.usage_parser(usages.copy(), args6, None)
    assert usage_dic_6["mine"] is True and usage_dic_6["remove"] is True and usage_dic_6["x"] == '50' and usage_dic_6[
        "set"] is False

    usage_dic_7 = docopt.usage_parser(usages.copy(), args7, None)


def test_split_token():
    arg1 = docopt.Token("comm1|comm2", None, None, "Command")
    arg2 = docopt.Token("--opt1|--opt2", None, None, "Option")
    res1 = docopt.split_token(arg1)
    res2 = docopt.split_token(arg2)
    assert res1[0].txt == "comm1" and res1[1].txt == "comm2" and res1[0].type == "Command"
    assert res2[0].txt == "--opt1" and res2[1].txt == "--opt2" and res2[0].type == "Option"


def test_convert_tokens():
    p_name = "myProgram.py"
    pattern = "  myProgram.py arg1 arg2 arg3"
    tokens = docopt.convert_tokens(pattern, p_name)
    assert tokens[0].txt == "arg1" and tokens[1].txt == "arg2" and tokens[2].txt == "arg3"


def test_parse_args():
    tokens = [docopt.Token("<arg>", None, None, None), docopt.Token("extra", None, None, None),
              docopt.Token("ARG", None, None, None)]
    docopt.parse_args(tokens)
    assert tokens[0].type == "Argument" and tokens[1].type != "Argument" and tokens[2].type == "Argument"


def test_parse_options():
    tokens = [docopt.Token("extra-", None, None, None), docopt.Token("-o", None, None, None),
              docopt.Token("--option", None, None, None)]
    docopt.parse_options(tokens)
    assert tokens[0].type != "Option" and tokens[1].type == "Option" and tokens[2].type == "Option"


def test_parse_commands():
    tokens = [docopt.Token("|", None, None, None), docopt.Token("-o", None, None, "Option")]
    tokens.extend([docopt.Token("<arg>", None, None, "Argument"), docopt.Token("comm", None, None, None)])
    docopt.parse_commands(tokens)
    assert tokens[0].type != "Command" and tokens[1].type == "Option" and tokens[2].type == "Argument" and tokens[
        3].type == "Command"


def test_parse_mutex():
    t1 = docopt.Token("mu1|mu2", None, None, "Command")
    t2 = docopt.Token("--opt", None, None, "Option")
    t3 = docopt.Token("--tex1", None, None, "Option")
    t4 = docopt.Token("|", None, None, None)
    t5 = docopt.Token("--tex2", None, None, "Option")
    t1.r = t2
    t2.lf, t2.r = t1, t3
    t3.lf, t3.r = t2, t4
    t4.lf, t4.r = t3, t5
    t5.lf = t4
    tokens = [t1, t2, t3, t4, t5]
    docopt.parse_mutex(tokens)
    assert tokens[0][0].txt == "mu1" and tokens[0][0].type == "Command"
    assert tokens[0][1].txt == "mu2" and tokens[0][1].type == "Command"
    assert tokens[1].txt == "--opt" and tokens[1].type == "Option"
    assert tokens[2][0].txt == "--tex1" and tokens[2][0].type == "Option"
    assert tokens[2][1].txt == "--tex2" and tokens[2][1].type == "Option"


def test_build_usage_dic():
    t1 = [docopt.Token("comm1", None, None, "Command"), docopt.Token("comm2", None, None, "Command")]
    t2 = docopt.Token("<arg1>", None, None, "Argument")
    t3 = docopt.Token("comm3", None, None, "Command")
    t4 = docopt.Token("<arg2>", None, None, "Argument")
    tokens = [t1, t2, t3, t4]
    res1 = {"comm1": False, "comm2": False, "arg1": None, "comm3": False, "arg2": None}
    res2 = docopt.build_usage_dic(tokens)
    assert res1 == res2


def test_process_paren():
    t1 = docopt.Token("[<arg1>]", None, None, None)
    t2 = docopt.Token("[comm1", None, None, None)
    t3 = docopt.Token("comm2", None, None, None)
    t4 = docopt.Token("comm3]", None, None, None)
    t5 = docopt.Token("--opt", None, None, None)
    t1.r = t2
    t2.lf, t2.r = t1, t3
    t3.lf, t3.r = t2, t4
    t4.lf, t4.r = t3, t5
    t5.lf = t4
    tokens1 = [t1, t2, t3, t4, t5]
    docopt.process_paren(tokens1, '[')
    assert t1.is_req is False and t1.txt == "<arg1>"
    assert t2.is_req is False and t2.txt == "comm1"
    assert t3.is_req is False and t3.txt == "comm2"
    assert t4.is_req is False and t4.txt == "comm3"
    assert t5.is_req is True and t5.txt == "--opt"

    # Test for exception raised if unmatched paren
    t6 = docopt.Token("[<arg2>", None, None, None)
    tokens2 = [t6]
    with pytest.raises(Exception) as exc_info:
        docopt.process_paren(tokens2, "[")
    assert exc_info.value.args[0] == "Could not find closed paren or bracket."


def test_parse_usage():
    usages = ['Usage:', '  myProgram.py <arg1> comm1 --opt1', '  myProgram.py comm2 ARG2 [--opt2] <ARG3>',
              '  myProgram.py (mut1|mut2) [--mut3 | --mut4]']
    u = {"arg1": None, "comm1": False, "comm2": False, "ARG2": None, "ARG3": None, "mut1": False, "mut2": False}
    patterns, usage_dic = docopt.parse_usage(usages)

    assert usage_dic == u

    assert patterns[0][0].txt == "<arg1>" and patterns[0][0].type == "Argument"
    assert patterns[0][1].txt == "comm1" and patterns[0][1].type == "Command"
    assert patterns[0][2].txt == "--opt1" and patterns[0][2].type == "Option"

    assert patterns[1][0].txt == "comm2" and patterns[1][0].type == "Command"
    assert patterns[1][1].txt == "ARG2" and patterns[1][1].type == "Argument"
    assert patterns[1][2].txt == "--opt2" and patterns[1][2].type == "Option" and patterns[1][2].is_req is False
    assert patterns[1][3].txt == "<ARG3>" and patterns[1][3].type == "Argument"

    # Handle mutually exclusive tokens
    assert isinstance(patterns[2][0], list) is True
    assert patterns[2][0][0].txt == "mut1" and patterns[2][0][0].type == "Command"
    assert patterns[2][0][1].txt == "mut2" and patterns[2][0][1].type == "Command"

    assert isinstance(patterns[2][1], list) is True
    assert patterns[2][1][0].txt == "--mut3" and patterns[2][1][0].type == "Option" and patterns[2][1][
        0].is_req is False
    assert patterns[2][1][1].txt == "--mut4" and patterns[2][1][1].type == "Option" and patterns[2][1][
        1].is_req is False


def test_check_mutex():
    token = [docopt.Token("comm1", None, None, "Command"), docopt.Token("comm2", None, None, "Command")]
    token[0].is_req, token[1].is_req = True, True
    arguments = ["blah", "bleh", "comm1", "blih"]
    index = 2
    assert docopt.check_mutex(index, token, arguments) is False

    arguments.insert(3, "comm2")
    assert docopt.check_mutex(index, token, arguments) is True

    arguments = ["blah", "bleh", "blih"]
    assert docopt.check_mutex(index, token, arguments) is True

    token[0].is_req, token[1].is_req = False, False
    token[0].r = docopt.Token("extra", None, None, "Command")
    assert docopt.check_mutex(index, token, arguments) is False


def test_check_tokens():
    # Check handling of missing optional arguments
    t_right = docopt.Token("--opt1", None, None, "Option")
    token = docopt.Token("<arg1>", None, t_right, "Argument")
    token.is_req = False

    arguments = ["comm1", "--opt1"]
    index = 1

    assert docopt.check_tokens(index, token, arguments) is False

    t_right = [docopt.Token("--opt1", None, None, "Option"), docopt.Token("--opt2", None, None, "Option")]
    assert docopt.check_tokens(index, token, arguments) is False

    # Check for commands, optional and required
    token = docopt.Token("comm1", None, None, "Command")
    arguments = ["<arg1>", "comm1"]
    assert docopt.check_tokens(index, token, arguments) is False

    arguments = ["<arg1>", "--opt1"]
    assert docopt.check_tokens(index, token, arguments) is True

    token.is_req = False
    assert docopt.check_tokens(index, token, arguments) is False

    # Check for options, optional and required
    token = docopt.Token("--opt1=<kn>", None, None, "Option")
    arguments = ["<arg1>", "--opt1=50"]
    assert docopt.check_tokens(index, token, arguments) is False

    token.txt = "--opt1"
    arguments[1] = "--opt1"
    assert docopt.check_tokens(index, token, arguments) is False

    arguments[1] = "comm1"
    assert docopt.check_tokens(index, token, arguments) is True

    token.is_req = False
    assert docopt.check_tokens(index, token, arguments) is False


def test_find_conflict():
    usage = [[docopt.Token("mut1", None, None, "Command"), docopt.Token("mut2", None, None, "Command")]]
    usage.extend([docopt.Token("<arg1>", None, None, "Argument"), docopt.Token("--opt1", None, None, "Option")])

    arguments = ["mut1", "50", "--opt1"]
    assert docopt.find_conflict(usage, arguments) is False

    arguments = ["mut1", "mut2", "50", "--opt1"]
    assert docopt.find_conflict(usage, arguments) is True

    usage[2].is_req = False
    arguments = ["mut2", "50"]
    assert docopt.find_conflict(usage, arguments) is False

    usage[1].is_req = False
    usage[1].r = usage[2]
    arguments = ["mut1", "--opt1"]
    assert docopt.find_conflict(usage, arguments) is False


def test_find_matching_pattern():
    pattern1 = [docopt.Token("comm1", None, None, "Command")]
    pattern1.append(docopt.Token("<arg1>", None, None, "Argument"))
    pattern1.append(docopt.Token("<arg2>", None, None, "Argument"))
    pattern1.append([docopt.Token("--opt1", None, None, "Option"), docopt.Token("--opt2", None, None, "Option")])
    pattern1[3][0].is_req, pattern1[3][1].is_req = False, False

    pattern2 = [[docopt.Token("comm1", None, None, "Command"), docopt.Token("comm2", None, None, "Command")]]
    pattern2.append(docopt.Token("-o", None, None, "Option"))
    pattern2.append(docopt.Token("ARG3", None, None, "Argument"))

    patterns = [pattern1, pattern2]

    arguments1 = ["comm1", "50", "Mine", "--opt2"]
    arguments2 = ["comm1", "100", "Yours", "--opt1"]
    arguments3 = ["comm2", "-o", "shoot"]
    arguments4 = ["comm1", "50", "Mine"]
    arguments5 = ["comm1", "comm2", "-o", "shoot"]

    assert docopt.find_matching_pattern(patterns, arguments1) == 0
    assert docopt.find_matching_pattern(patterns, arguments2) == 0
    assert docopt.find_matching_pattern(patterns, arguments3) == 1
    assert docopt.find_matching_pattern(patterns, arguments4) == 0
    assert docopt.find_matching_pattern(patterns, arguments5) is None


def test_populate_usage_dic():
    pattern1 = [docopt.Token("comm1", None, None, "Command")]
    pattern1.append(docopt.Token("<arg1>", None, None, "Argument"))
    pattern1.append(docopt.Token("<arg2>", None, None, "Argument"))
    pattern1.append([docopt.Token("--opt1", None, None, "Option"), docopt.Token("--opt2", None, None, "Option")])
    pattern1[3][0].is_req, pattern1[3][1].is_req = False, False

    pattern2 = [[docopt.Token("comm1", None, None, "Command"), docopt.Token("comm2", None, None, "Command")]]
    pattern2.append(docopt.Token("-o", None, None, "Option"))
    pattern2.append(docopt.Token("ARG3", None, None, "Argument"))

    patterns = [pattern1, pattern2]
    usage_dic_1 = {"comm1": False, "comm2": False, "arg1": None, "arg2": None, "ARG3": None}
    usage_dic_2 = {"comm1": False, "comm2": False, "arg1": None, "arg2": None, "ARG3": None}

    args1 = ["comm1", "50", "100", "--opt1"]
    args2 = ["comm2", "-o", "shoot"]

    ptu0 = None
    ptu1 = 0
    ptu2 = 1

    with pytest.raises(Exception) as exc_info:
        docopt.populate_usage_dic(ptu0, patterns, args1, usage_dic_1)
    assert exc_info.value.args[0] == "No matching usage pattern found."

    docopt.populate_usage_dic(ptu1, patterns, args1, usage_dic_1)
    assert usage_dic_1 == {"comm1": True, "comm2": False, "arg1": '50', "arg2": '100', "ARG3": None}

    docopt.populate_usage_dic(ptu2, patterns, args2, usage_dic_2)
    assert usage_dic_2 == {"comm1": False, "comm2": True, "arg1": None, "arg2": None, "ARG3": "shoot"}


##########################################################################################
##########################################################################################
# Option function test
def test_options_parser():
    options_dic = {'--helping': True, '--sorted': True, '--output': 'ttt.pdf', '--version': False, '--speed': 10,
                   '--moored': True, '--drifting': False, '--rr': False, '--aaa': 20, '--yyy': False}
    res = docopt.options_parser(argv=argv, user_argv=['--sorted'], options=options.split("\n"))
    assert res == options_dic

    options_dic = {'--helping': True, '--sorted': False, '--output': 'ttt.pdf', '--version': False, '--speed': 10,
                   '--moored': False, '--drifting': False, '--rr': False, '--aaa': 20, '--yyy': False}
    res = docopt.options_parser(argv=None, user_argv=['-h', '-o=ttt.pdf'], options=options.split("\n"))
    assert res == options_dic


# Test getting the usage and options strings from docstring
def test_check_option_lines():
    options_dic = {'-h --help --helping --haha -hhh --ooooo': False, '--sorted': False,
                   '-o=<file> --output=<value>': './test.txt', '--version': False,
                   '--speed=<kn> -s=<kn>': 10, '--moored': False, '--drifting': False,
                   '--rr': False, '--aaa=<value>': 20, '--yyy': False}

    res = docopt.check_option_lines(options=options.split('\n'))
    assert res == options_dic


# Test for if function can get the default values correctly from the docstring
def test_find_default_value():
    options_dic = {'-o=<file> --output=<file>': None}
    line = '-o FILE --output=<value>  Speed in knots [default: ./test.txt].'
    res = docopt.find_default_value(line=line, old_key="-o=<file> --output=<file>", options_dic=options_dic)
    assert res == {'-o=<file> --output=<file>': './test.txt'}

    options_dic = {'--speed=<kn> -s=<kn>': None}
    line = '--speed=<kn> -s KN  Speed in knots [default: 10].'
    res = docopt.find_default_value(line=line, old_key="--speed=<kn> -s=<kn>", options_dic=options_dic)
    assert res == {'--speed=<kn> -s=<kn>': 10}

    options_dic = {'--aaa=<value>': None}
    line = '--aaa=<value>   Moored (anchored) mine [default: 20.9].'
    res = docopt.find_default_value(line=line, old_key="--aaa=<value>", options_dic=options_dic)
    assert res == {'--aaa=<value>': 20.9}


# Test function for the function for inserting new options into the dictionary
def test_check_first_option():
    tmp_array = ['--help', 'Show', ' this', 'screen.']
    old_key, tmp_dic = docopt.check_first_option(tmp_array=tmp_array, count=0)
    assert old_key == '--help'
    assert tmp_dic == {'--help': False}

    tmp_array = ['-o', 'FILE', 'Speed', 'in', 'knots']
    old_key, tmp_dic = docopt.check_first_option(tmp_array=tmp_array, count=0)
    assert old_key == '-o=<file>'
    assert tmp_dic == {'-o=<file>': None}

    tmp_array = ['--output=<file>', 'Speed', 'in', 'knots']
    old_key, tmp_dic = docopt.check_first_option(tmp_array=tmp_array, count=0)
    assert old_key == '--output=<file>'
    assert tmp_dic == {'--output=<file>': None}


# Test function for the function for inserting a secondary or more keyword for an option into the dictionary
def test_check_other_option():
    tmp_array = ['--help', '-h', 'this', 'screen.']
    old_key, new_key = docopt.check_other_option(tmp_array=tmp_array, count=1, old_key='--help')
    assert old_key == '--help'
    assert new_key == '--help -h'

    tmp_array = ['-s=<kn>', '--speed', 'KN', 'Speed', 'in', 'knots']
    old_key, tmp_dic = docopt.check_other_option(tmp_array=tmp_array, count=1, old_key='-s=<kn>')
    assert old_key == '-s=<kn>'
    assert tmp_dic == '-s=<kn> --speed=<kn>'


# Test function for if the function can build a correct dictionary based on docstring and user inputs
def test_build_output_options_dictionary():
    before = {'-h --help --helping': False, '-o=<file> --output=<file>': 'ttt.pdf',
              '--speed=<kn>': 10}
    after = {'--helping': False, '--output': 'ttt.pdf', '--speed': 10}
    res = docopt.build_output_options_dictionary(user_argv=[], options_dic=before)
    assert res == after

    before = {'-h --help --helping': False, '-o=<file> --output=<file>': 'ttt.pdf',
              '--speed=<kn>': 10}
    after = {'--helping': True, '--output': 'haha.pdf', '--speed': 10}
    res = docopt.build_output_options_dictionary(user_argv=['-h', '-o=haha.pdf'], options_dic=before)
    assert res == after


# Test function for the function to decide whether the current keyword contains a value
def test_check_option_contain_value():
    options_dic = {'-h --help --helping': False, '-o=<file> --output=<file>': 'ttt.pdf'}
    before = {'-h --help --helping': False, '-o=<file> --output=<file>': 'ttt.pdf'}

    after = {'-h --help --helping': True, '-o=<file> --output=<file>': 'ttt.pdf'}
    res = docopt.check_option_contain_value(output_dic=before, options_dic=options_dic,
                                            arguments=['-h'])
    assert res == after

    after = {'-h --help --helping': True, '-o=<file> --output=<file>': 'haha.pdf'}
    res = docopt.check_option_contain_value(output_dic=before, options_dic=options_dic,
                                            arguments=['-h', '-o=haha.pdf'])
    assert res == after


# Test function for the function to check the keywords without a cooperating value
def test_check_key_without_equal():
    options_dic = {'-h --help --helping': False, '--moored': False}

    before = {'-h --help --helping': False, '--moored': False}
    after = {'-h --help --helping': True, '--moored': False}
    res = docopt.check_key_without_equal(element='--help', options_dic=options_dic, output_dic=before)
    assert res == after

    before = {'-h --help --helping': False, '--moored': False}
    after = {'-h --help --helping': False, '--moored': True}
    res = docopt.check_key_without_equal(element='--moored', options_dic=options_dic, output_dic=before)
    assert res == after


# Test function for the function to check the keywords with a cooperating value
def test_check_key_contain_equal():
    options_dic = {'--speed=<kn>': 0, '-o=<file> --output=<file>': 'default.txt'}

    before = {'--speed=<kn>': 0, '-o=<file> --output=<file>': 'default.txt'}
    after = {'--speed=<kn>': 10.7, '-o=<file> --output=<file>': 'default.txt'}
    res = docopt.check_key_contain_equal(element="--speed=10.7", options_dic=options_dic, output_dic=before)
    assert res == after

    before = {'--speed=<kn>': 0, '-o=<file> --output=<file>': 'default.txt'}
    after = {'--speed=<kn>': 0, '-o=<file> --output=<file>': 'haha.pdf'}
    res = docopt.check_key_contain_equal(element="-o=haha.pdf", options_dic=options_dic, output_dic=before)
    assert res == after


##############################################################################
##############################################################################
# Test print function
def test_print_output_dictionary():
    input1 = {'1': True, '2': 'haha', '3': False, '4': True, '5': 'haha'}
    input2 = {'1': True, '2': 'haha', '3': False, '4': True, '5': 'haha', '6': False,
              '7': True, '8': 'haha', '9': False, '10': True, '11': 'haha', '12': False}
    input3 = {'1': True, '2': 'haha', '3': False, '4': True, '5': 'haha', '6': False,
              '7': True, '8': 'haha', '9': False, '10': True, '11': 'haha', '12': False,
              '13': True, '14': 'haha', '15': False, '16': True, '17': 'haha', '18': False,
              '19': True, '20': 'haha', '21': False, '22': True, '23': 'haha', '24': False,
              '25': True, '26': 'haha', '27': False, '28': True, '29': 'haha', '30': False}
    usage_dic = {'usage1': 'x', 'usage2': 'y'}
    options_dic = {'options1': 'x', 'options2': 'y'}
    dic_total, res = docopt.print_output_dictionary(usage_dic=usage_dic, options_dic=input1)
    assert dic_total == {**usage_dic, **dic_total}
    dic_total, res = docopt.print_output_dictionary(usage_dic={}, options_dic=input2)
    assert dic_total == input2
    dic_total, res = docopt.print_output_dictionary(usage_dic=input3, options_dic=options_dic)
    assert dic_total == {**input3, **options_dic}


# Test function for testing the function for outputting a correct format of dictionary according
# to the user arguments as well as the docstring
def test_output_formatter():
    dic = {'--helping': True, '--sorted': True, '--output': 'ttt.pdf', '--version': False, '--speed': 10,
           '--moored': True, '--drifting': None, '--rr': False, '--aaa': 20.9, '--yyy': False}
    after = "{'--helping': True         '--speed': 10          '--aaa': 20.9\n" + \
            " '--sorted': True          '--moored': True       '--yyy': False\n" + \
            " '--output': 'ttt.pdf'     '--drifting': None\n" + \
            " '--version': False        '--rr': False}\n"
    dic_list = list(dic)
    res = docopt.output_formatter(rows=4, length=len(dic_list), dic_list=dic_list, dictionary_total=dic)
    assert res == after


# Test function for the function on inserting the key value pairs into the output arrays
def test_insert_content():
    dic = {'--helping': True, '--sorted': None, '--output': 'ttt.pdf', '--speed': 10, '--aaa': 20.9}
    dic_list = list(dic)
    res = docopt.insert_content(dic_list=dic_list, idx=0, rows=0, col_idx=0, dictionary_total=dic)
    assert '\'--helping\'' + ': ' + 'True' == res

    res = docopt.insert_content(dic_list=dic_list, idx=1, rows=0, col_idx=0, dictionary_total=dic)
    assert '\'--sorted\'' + ': ' + 'None' == res

    res = docopt.insert_content(dic_list=dic_list, idx=2, rows=0, col_idx=0, dictionary_total=dic)
    assert '\'--output\'' + ': ' + '\'ttt.pdf\'' == res

    res = docopt.insert_content(dic_list=dic_list, idx=3, rows=0, col_idx=0, dictionary_total=dic)
    assert '\'--speed\'' + ': ' + '10' == res

    res = docopt.insert_content(dic_list=dic_list, idx=4, rows=0, col_idx=0, dictionary_total=dic)
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
    res = docopt.print_output_from_rows(col1=col1,
                                        col2=col2,
                                        col3=col3, rows=5)
    assert res == outputting
