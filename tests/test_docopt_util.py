import docopt_util
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


# Test function for processing string
@pytest.mark.filterwarnings("ignore:api v1")
def test_processing_string(capsys):
    usage_array, options_array = docopt_util.processing_string(
        doc=doc1, help_message=False, version="test 2.0")
    assert usage.split('\n') == usage_array
    assert options.split('\n') == options_array
    print(usage_array)
    print(options_array)

    res = docopt_util.processing_string(doc=None, help_message=False, version="test 2.0")
    assert res is None

    usage_array, options_array = docopt_util.processing_string(
        doc=doc1, help_message=True, version="test 2.0")
    assert usage.split('\n') == usage_array
    assert options.split('\n') == options_array
    captured = capsys.readouterr()
    assert len(captured.out) > 0


# Test getting the usage and options strings from docstring
def test_get_usage_and_options():
    tmp_name, tmp_usage, tmp_options, display = \
        docopt_util.get_usage_and_options(doc=doc1, version=version)
    assert tmp_name == name
    assert tmp_usage == usage
    assert tmp_options == options
    print(display)

    tmp_name, tmp_usage, tmp_options, display = \
        docopt_util.get_usage_and_options(doc=doc2, version=version)
    assert tmp_name == ""
    assert tmp_usage == usage
    assert tmp_options == options

    tmp_name, tmp_usage, tmp_options, display = \
        docopt_util.get_usage_and_options(doc=doc3, version=version)
    assert tmp_name == ""
    assert tmp_usage == usage
    assert tmp_options == ""

    tmp_name, tmp_usage, tmp_options, display = \
        docopt_util.get_usage_and_options(doc=doc4, version=version)
    assert tmp_name == ""
    assert tmp_usage == usage
    print(tmp_options)
    print(options_2)
    assert tmp_options == options_2

    tmp_name, tmp_usage, tmp_options, display = \
        docopt_util.get_usage_and_options(doc=doc5, version=version)
    assert tmp_name == name
    assert tmp_usage == usage
    assert tmp_options == options_2


# Test if the warnings will cause the function to return a correct integer value
@pytest.mark.filterwarnings("ignore:api v1")
def test_check_warnings():
    res = docopt_util.check_warnings(usage=usage, options=options)
    assert res == 0

    res = docopt_util.check_warnings(usage="", options=options)
    assert res == 1

    res = docopt_util.check_warnings(usage=usage, options="")
    assert res == 2


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
    dic_total, res = docopt_util.print_output_dictionary(usage_dic=usage_dic)
    assert dic_total == {**usage_dic, **dic_total}
    dic_total, res = docopt_util.print_output_dictionary(usage_dic={})
    assert dic_total == input2
    dic_total, res = docopt_util.print_output_dictionary(usage_dic=input3)
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
    res = docopt_util.output_formatter(rows=4, length=len(dic_list), dic_list=dic_list,
                                       dictionary_total=dic)
    assert res == after


# Test function for the function on inserting the key value pairs into the output arrays
def test_insert_content():
    dic = {'--helping': True, '--sorted': None, '--output': 'ttt.pdf', '--speed': 10, '--aaa': 20.9}
    dic_list = list(dic)
    res = docopt_util.insert_content(dic_list=dic_list, idx=0, rows=0,
                                     col_idx=0, dictionary_total=dic)
    assert '\'--helping\'' + ': ' + 'True' == res

    res = docopt_util.insert_content(dic_list=dic_list, idx=1, rows=0,
                                     col_idx=0, dictionary_total=dic)
    assert '\'--sorted\'' + ': ' + 'None' == res

    res = docopt_util.insert_content(dic_list=dic_list, idx=2, rows=0,
                                     col_idx=0, dictionary_total=dic)
    assert '\'--output\'' + ': ' + '\'ttt.pdf\'' == res

    res = docopt_util.insert_content(dic_list=dic_list, idx=3, rows=0,
                                     col_idx=0, dictionary_total=dic)
    assert '\'--speed\'' + ': ' + '10' == res

    res = docopt_util.insert_content(dic_list=dic_list, idx=4, rows=0,
                                     col_idx=0, dictionary_total=dic)
    assert '\'--aaa\'' + ': ' + '20.9' == res


# Test function for the function that check if the value provided is primitive type or a string
def test_check_value_type():
    res = docopt_util.check_value_type(value="hello world")
    assert not res

    res = docopt_util.check_value_type(value=10)
    assert res

    res = docopt_util.check_value_type(value=10.67)
    assert res

    res = docopt_util.check_value_type(value=None)
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
    res = docopt_util.print_output_from_rows(col1=col1, col2=col2, col3=col3, num_rows=5)
    assert res == outputting
