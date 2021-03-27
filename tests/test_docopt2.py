"""
   module for unit test of res = old_docopt.py
"""
import examples.new_usage as docopt


def test_get_patterns_and_dict():
    res = docopt.get_patterns_and_dict(usages=None)


def test_is_num():
    res = docopt.is_num(arg=None)


def test_build_tree_heads():
    res = docopt.build_tree_heads(token_set=None, first_token=None, tree_heads=None)


def test_build_token_set():
    res = docopt.build_token_set(pattern=None, token_set=None)


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


def test_check_patterns_with_user_input():
    res = docopt.check_patterns_with_user_input(usage_tree=None, usage_dic=None, arg=None)


def test_check_patterns_with_user_input_helper():
    res = docopt.check_patterns_with_user_input_helper(children=None, usage_dic=None, arg=None)
