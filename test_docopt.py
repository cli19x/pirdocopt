"""
   module for unit test of res = docopt.py
"""
import docopt

doc = """Perfect

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
  -o FILE --output=<file>  Speed in knots [default: ./test.txt].
  --version     Show version.
  --speed=<kn> -s KN  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
  --rr     Show version.
  --fff=<tt> -s KN  Speed in knots.
  --aaa=<file>      Moored (anchored) mine [default: haha.pdf].
  --yyy    Drifting mine.

"""

name = """Perfect"""

usage = """
Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
  naval_fate.py ship shoot <x> <y>
  naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]
  naval_fate.py (-h | --help)
  naval_fate.py --version
"""

options = """
Options:
  -h --help --helping --haha -hhh --ooooo  Show this screen.
  --sorted  Show sorted.
  -o FILE --output=<file>  Speed in knots [default: ./test.txt].
  --version     Show version.
  --speed=<kn> -s KN  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
  --rr     Show version.
  --fff=<tt> -s KN  Speed in knots.
  --aaa=<file>      Moored (anchored) mine [default: haha.pdf].
  --yyy    Drifting mine.
"""

version = """test 2.1"""


#################################################################################
#################################################################################
# Main function test
def test_docopt():
    res = docopt.docopt(doc=doc, version="test 2.0", help_message=True,
                        argv=['--help', '--moored', '--output=ttt.pdf'])


def test_processing_string():
    res = docopt.processing_string(doc=doc, help_message=True, version="test 2.0")


def test_get_usage_and_options():
    res = docopt.get_usage_and_options(doc=doc)


def test_check_warnings():
    res = docopt.check_warnings(usage="", options="")


def test_show_help():
    res = docopt.show_help(name="", version="", usage="", options="")


#################################################################################
#################################################################################
# Usage function test
def test_usage_parser():
    res = docopt.usage_parser(usages="", arguments="")


def test_split_token():
    res = docopt.split_token(token="")


def test_convert_tokens():
    res = docopt.convert_tokens(pattern="", name="")


def test_parse_args():
    res = docopt.parse_args(tokens="")


def test_parse_options():
    res = docopt.parse_options(tokens="")


def test_parse_commands():
    res = docopt.parse_commands(tokens="")


def test_parse_mutex():
    res = docopt.parse_mutex(tokenObjects="")


def test_build_usage_dic():
    res = docopt.build_usage_dic(tokenObjects="")


def test_process_paren():
    res = docopt.process_paren(tokens="", op="")


def test_parse_usage():
    res = docopt.parse_usage(usages="")


def test_check_mutex():
    res = docopt.check_mutex(index="", token="", arguments="")


def test_check_tokens():
    res = docopt.check_tokens(index="", token="", arguments="")


def test_find_conflict():
    res = docopt.find_conflict(p="", arguments="")


def test_find_matching_pattern():
    res = docopt.find_matching_pattern(patterns="", arguments="")


def test_populate_usage_dic():
    res = docopt.populate_usage_dic(patternToUse="", patterns="", arguments="", usage_dic="")


##########################################################################################
##########################################################################################
# Option function test
def test_options_parser():
    res = docopt.options_parser(argv="", user_argv="", options="")


def test_check_option_lines():
    res = docopt.check_option_lines(options="")


def test_find_default_value():
    res = docopt.find_default_value(line="", old_key="", options_dic={})


def test_check_first_option():
    res = docopt.check_first_option(tmp_array="", count="")


def test_check_other_option():
    res = docopt.check_other_option(tmp_array="", count=0, old_key="")


def test_build_output_options_dictionary():
    res = docopt.build_output_options_dictionary(user_argv="", options_dic="")


def test_check_option_contain_value():
    res = docopt.check_option_contain_value(output_dic="", options_dic="", arguments="", remove_duplicate="")


def test_check_keys():
    res = docopt.check_keys(element="", is_contain_equal="", output_dic="", options_dic="", remove_duplicate="")


def test_check_key_without_equal():
    res = docopt.check_key_without_equal(element="", remove_duplicate="", options_dic="", output_dic="")


def test_check_key_contain_equal():
    res = docopt.check_key_contain_equal(element="", remove_duplicate="", options_dic="", output_dic="")


def test_print_output_dictionary():
    res = docopt.print_output_dictionary(usage_dic={}, options_dic={})


def test_output_formatter():
    res = docopt.output_formatter(rows="", length="", dic_list="", dictionary_total="")


def test_insert_content():
    res = docopt.insert_content(dic_list="", idx="", rows="", col_idx="", dictionary_total="")


def test_check_value_type():
    res = docopt.check_value_type(value="")


def test_print_output_from_rows():
    res = docopt.print_output_from_rows(col1="", col2="", col3="", rows="")
