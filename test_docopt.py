"""
   module for unit test of res = docopt.py
"""
import docopt
import pytest

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
# def test_docopt():
#     res = docopt.docopt(doc=doc1, version="test 2.0", help_message=True,
#                         argv=argv)


def test_processing_string():
    usage_array, options_array = docopt.processing_string(doc=doc1, help_message=False, version="test 2.0")
    assert usage.split('\n') == usage_array
    assert options.split('\n') == options_array

    res = docopt.processing_string(doc=None, help_message=False, version="test 2.0")
    assert res is None
###############################################


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


def test_check_warnings():
    res = docopt.check_warnings(usage=usage, options=options)
    assert res == 0

    res = docopt.check_warnings(usage="", options=options)
    assert res == 1

    res = docopt.check_warnings(usage=usage, options="")
    assert res == 2


def test_show_help():
    res = docopt.show_help(name=name, version=version, usage=usage, options=options)
    assert res == help1

    res = docopt.show_help(name=name, version="", usage=usage, options=options)
    assert res == help2


#################################################################################
#################################################################################
# # Usage function test
# def test_usage_parser():
#     res = docopt.usage_parser(usages="", arguments="")
#
#
def test_split_token():
    arg1 = docopt.Token("comm1|comm2", None, None, "Command")
    arg2 = docopt.Token("--opt1|--opt2", None, None, "Option")
    res1 = docopt.split_token(arg1)
    res2 = docopt.split_token(arg2)
    assert res1[0].txt == "comm1" and res1[1].txt == "comm2" and res1[0].type == "Command"
    assert res2[0].txt == "--opt1" and res2[1].txt == "--opt2" and res2[0].type == "Option"

def test_convert_tokens():
    name = "myProgram.py"
    pattern = "  myProgram.py arg1 arg2 arg3"
    tokens = docopt.convert_tokens(pattern, name)
    assert tokens[0].txt == "arg1" and tokens[1].txt == "arg2" and tokens[2].txt == "arg3"

def test_parse_args():
    tokens = [docopt.Token("<arg>", None, None, None), docopt.Token("extra", None, None, None), docopt.Token("ARG", None, None, None)]
    docopt.parse_args(tokens)
    assert tokens[0].type=="Argument" and tokens[1].type!="Argument" and tokens[2].type=="Argument"

def test_parse_options():
    tokens = [docopt.Token("extra-", None, None, None), docopt.Token("-o", None, None, None), docopt.Token("--option", None, None, None)]
    docopt.parse_options(tokens)
    assert tokens[0].type!="Option" and tokens[1].type=="Option" and tokens[2].type=="Option"

def test_parse_commands():
    tokens = [docopt.Token("|", None, None, None), docopt.Token("-o", None, None, "Option")]
    tokens.extend([docopt.Token("<arg>", None, None, "Argument"), docopt.Token("comm", None, None, None)])
    docopt.parse_commands(tokens)
    assert tokens[0].type!="Command" and tokens[1].type=="Option" and tokens[2].type=="Argument" and tokens[3].type=="Command"

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
    res1 = {"comm1":False, "comm2":False, "arg1":None, "comm3":False, "arg2":None}
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
    assert t1.isReq is False and t1.txt == "<arg1>"
    assert t2.isReq is False and t2.txt == "comm1"
    assert t3.isReq is False and t3.txt == "comm2"
    assert t4.isReq is False and t4.txt == "comm3"
    assert t5.isReq is True and t5.txt == "--opt"

    # Test for exception raised if unmatched paren
    t6 = docopt.Token("[<arg2>", None, None, None)
    tokens2 = [t6]
    with pytest.raises(Exception) as exc_info:
        docopt.process_paren(tokens2, "[")
    assert exc_info.value.args[0] == "Could not find closed paren or bracket." 

# def test_parse_usage():
#     res = docopt.parse_usage(usages="")
#
#
# def test_check_mutex():
#     res = docopt.check_mutex(index="", token="", arguments="")
#
#
# def test_check_tokens():
#     res = docopt.check_tokens(index="", token="", arguments="")
#
#
# def test_find_conflict():
#     res = docopt.find_conflict(p="", arguments="")
#
#
# def test_find_matching_pattern():
#     res = docopt.find_matching_pattern(patterns="", arguments="")
#
#
# def test_populate_usage_dic():
#     res = docopt.populate_usage_dic(patternToUse="", patterns="", arguments="", usage_dic="")
#

##########################################################################################
##########################################################################################
# Option function test
def test_options_parser():
    options_dic = {'--helping': True, '--sorted': True, '--output': 'ttt.pdf', '--version': False, '--speed': 10,
                   '--moored': True, '--drifting': False, '--rr': False, '--aaa': 20, '--yyy': False}
    res = docopt.options_parser(argv=argv, user_argv=['--sorted'], options=options.split("\n"))
    print(res)
    print(options_dic)
    assert res == options_dic

    options_dic = {'--helping': True, '--sorted': True, '--output': 'ttt.pdf', '--version': False, '--speed': 10,
                   '--moored': True, '--drifting': False, '--rr': False, '--aaa': 20, '--yyy': False}
    res = docopt.options_parser(argv=None, user_argv=['-h', '-o=<ttt.pdf>'], options=options.split("\n"))
    assert res == options_dic


if __name__ == '__main__':
    test_options_parser()


def test_check_option_lines():
    options_dic = {'-h --help --helping --haha -hhh --ooooo': False, '--sorted': False,
                   '-o=<file> --output=<file>': './test.txt', '--version': False,
                   '--speed=<kn> -s=<kn>': 10, '--moored': False, '--drifting': False,
                   '--rr': False, '--aaa=<file>': 20, '--yyy': False}

    res = docopt.check_option_lines(options=options)
    assert res == options_dic


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


def test_check_first_option():
    tmp_array = ['--help', 'Show', ' this', 'screen.']
    old_key, tmp_dic = docopt.check_first_option(tmp_array=tmp_array, count=0)
    assert old_key == '--help'
    assert tmp_dic == {'--help': False}

    tmp_array = ['-o', 'FILE', 'Speed', 'in', 'knots']
    old_key, tmp_dic = docopt.check_first_option(tmp_array=tmp_array, count=0)
    assert old_key == '-o=<file>'
    assert tmp_dic == {'-o=<file>': None}

    tmp_array = ['-output=<file>', 'Speed', 'in', 'knots']
    old_key, tmp_dic = docopt.check_first_option(tmp_array=tmp_array, count=0)
    assert old_key == '-o=<file>'
    assert tmp_dic == {'-o=<file>': None}


def test_check_other_option():
    tmp_array = ['--help', '-h', 'this', 'screen.']
    old_key, new_key = docopt.check_other_option(tmp_array=tmp_array, count=1, old_key='--help')
    assert old_key == '--help'
    assert new_key == '--help -h'

    tmp_array = ['-s=<kn>', '--speed', 'KN', 'Speed', 'in', 'knots']
    old_key, tmp_dic = docopt.check_other_option(tmp_array=tmp_array, count=1, old_key='-s=<kn>')
    assert old_key == '-s=<kn>'
    assert tmp_dic == '-s=<kn> --speed=<kn>'


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


def test_check_option_contain_value():
    options_dic = {'-h --help --helping': False, '-o=<file> --output=<file>': 'ttt.pdf'}
    before = {'-h --help --helping': False, '-o=<file> --output=<file>': 'ttt.pdf'}

    after = {'-h --help --helping': True, '-o=<file> --output=<file>': 'ttt.pdf'}
    res = docopt.check_option_contain_value(output_dic=before, options_dic=options_dic,
                                            arguments=['-h'])
    assert res == after

    after = {'--helping  --help -h': True, '-o=<file> --output=<file>': 'haha.pdf'}
    res = docopt.check_option_contain_value(output_dic=before, options_dic=options_dic,
                                            arguments=['-h', '-o=haha.pdf'])
    assert res == after


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
    input1 = {'1': True, '2': 'haha', '3': False, '4': True, '5': 'haha', '6': False}
    input2 = {'1': True, '2': 'haha', '3': False, '4': True, '5': 'haha', '6': False,
              '7': True, '8': 'haha', '9': False, '10': True, '11': 'haha', '12': False}
    input3 = {'1': True, '2': 'haha', '3': False, '4': True, '5': 'haha', '6': False,
              '7': True, '8': 'haha', '9': False, '10': True, '11': 'haha', '12': False,
              '13': True, '14': 'haha', '15': False, '16': True, '17': 'haha', '18': False,
              '19': True, '20': 'haha', '21': False, '22': True, '23': 'haha', '24': False,
              '25': True, '26': 'haha', '27': False, '28': True, '29': 'haha', '30': False}
    res = docopt.print_output_dictionary(usage_dic={}, options_dic=input1)
    res = docopt.print_output_dictionary(usage_dic={}, options_dic=input2)
    res = docopt.print_output_dictionary(usage_dic={}, options_dic=input3)


def test_output_formatter():
    res = docopt.output_formatter(rows="", length="", dic_list="", dictionary_total="")


def test_insert_content():
    res = docopt.insert_content(dic_list="", idx="", rows="", col_idx="", dictionary_total="")


def test_check_value_type():
    res = docopt.check_value_type(value="hello world")
    assert not res

    res = docopt.check_value_type(value=10)
    assert res

    res = docopt.check_value_type(value=10.67)
    assert res

    res = docopt.check_value_type(value=None)
    assert res is None


def test_print_output_from_rows():
    res = docopt.print_output_from_rows(col1="", col2="", col3="", rows="")
