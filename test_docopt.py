"""
   module for unit test of res = docopt.py
"""
import docopt

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
# def test_split_token():
#     res = docopt.split_token(token="")
#
#
# def test_convert_tokens():
#     res = docopt.convert_tokens(pattern="", name="")
#
#
# def test_parse_args():
#     res = docopt.parse_args(tokens="")
#
#
# def test_parse_options():
#     res = docopt.parse_options(tokens="")
#
#
# def test_parse_commands():
#     res = docopt.parse_commands(tokens="")
#
#
# def test_parse_mutex():
#     res = docopt.parse_mutex(tokenObjects="")
#
#
# def test_build_usage_dic():
#     res = docopt.build_usage_dic(tokenObjects="")
#
#
# def test_process_paren():
#     res = docopt.process_paren(tokens="", op="")
#
#
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
    assert res == options_dic

    options_dic = {'--helping': True, '--sorted': False, '--output': 'ttt.pdf', '--version': False, '--speed': 10,
                   '--moored': False, '--drifting': False, '--rr': False, '--aaa': 20, '--yyy': False}
    res = docopt.options_parser(argv=None, user_argv=['-h', '-o=ttt.pdf'], options=options.split("\n"))
    assert res == options_dic


def test_check_option_lines():
    options_dic = {'-h --help --helping --haha -hhh --ooooo': False, '--sorted': False,
                   '-o=<file> --output=<value>': './test.txt', '--version': False,
                   '--speed=<kn> -s=<kn>': 10, '--moored': False, '--drifting': False,
                   '--rr': False, '--aaa=<value>': 20, '--yyy': False}

    res = docopt.check_option_lines(options=options.split('\n'))
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

    tmp_array = ['--output=<file>', 'Speed', 'in', 'knots']
    old_key, tmp_dic = docopt.check_first_option(tmp_array=tmp_array, count=0)
    assert old_key == '--output=<file>'
    assert tmp_dic == {'--output=<file>': None}


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

    after = {'-h --help --helping': True, '-o=<file> --output=<file>': 'haha.pdf'}
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


def test_output_formatter():
    dic = {'--helping': True, '--sorted': True, '--output': 'ttt.pdf', '--version': False, '--speed': 10,
           '--moored': True, '--drifting': None, '--rr': False, '--aaa': 20.9, '--yyy': False}
    after = [" '--helping': True", " '--sorted': True", " '--output': 'ttt.pdf'", " '--version': False",
             " '--speed': 10", " '--moored': True", " '--drifting': None", " '--rr': False",
             " '--aaa': 20.9", " '--yyy': False", ' ', ' ']
    dic_list = list(dic)
    res = docopt.output_formatter(rows=4, length=len(dic_list), dic_list=dic_list, dictionary_total=dic)
    assert len(res) == 12
    assert res == after


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


if __name__ == '__main__':
    test_insert_content()