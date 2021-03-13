import re
import sys
import docopt_util

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


def check_patterns_with_user_input(usage_tree, usage_dic, arg):
    """

     Args:
        usage_tree: The usage pattern tree for checking user input arguments.

        usage_dic: The dictionary for output the results of usage pattern.

        arg: Array of user input arguments, either is default or from command line.

    Returns:
        res: Boolean value for if input pattern is matching the patterns in docstring.
        usage_dic: Return None if no pattern matching, else return the updated usage dictionary.

    """

    res, usage_dic = check_patterns_with_user_input_helper(usage_tree, usage_dic, arg)
    return usage_dic if res is not False else None


def check_patterns_with_user_input_helper(usage_tree, usage_dic, arg):
    """

     Args:
        usage_tree: The usage pattern tree for checking user input arguments.

        usage_dic: The dictionary for output the results of usage pattern.

        arg: Array of user input arguments, either is default or from command line.

    Returns:
        res: Boolean value for if input pattern is matching the patterns in docstring.
        usage_dic: Return the updated usage dictionary or stay the same if no pattern found.

    """

    if len(arg) == 0:
        for child in usage_tree.chirden:
            if child.match('`/0'):
                return True, usage_dic
        return False, usage_dic

    current_element = arg.pop(0)
    res = False
    for child in usage_tree.chirden:
        # matching the repeat values (<name>...), skip_to is the index of the last repeat element
        # in user argument list
        # return skip_to == -1 if not matching
        # tmp_dic(2) contains {'<name>...': ['e1', 'e2', 'e3']} for repeat values,
        # and {'ship': Ture} for others
        skip_to, tmp_dic = child.match(arg.insert(0, current_element), 0)
        # skip_to2 is just for the easiness of design of the match function
        skip_to2, tmp_dic2 = child.match(current_element)
        if skip_to > 0:
            arg = arg[skip_to - 1:]
            res, usage_dic = check_patterns_with_user_input_helper(child, usage_dic, arg)
            usage_dic.update(tmp_dic)
        elif tmp_dic2 is not None:
            res, usage_dic = check_patterns_with_user_input_helper(child, usage_dic, arg)
            usage_dic.update(tmp_dic2)
    return res, usage_dic
