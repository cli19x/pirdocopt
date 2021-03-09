import re
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


class UsageToken:
    def __init__(self, e_list, pointers, contain_options):
        self.e_list = e_list
        self.pointers = pointers
        self.contain_options = contain_options


def main_function():
    usage_array, options_array = docopt_util.processing_string(doc2, False, version="testing tmp")
    token = UsageToken([], [], False)
    usage_dic, token = processing_usages(usage_array, token)
    turned_on_options = []
    usage_dic, turned_on_options = check_usage_pattern(usage_dic, token, turned_on_options)


def processing_usages(usage_array, token):
    usage_dic = {}
    for usage in usage_array:
        if 'Usage:' in usage:
            continue
        res = re.sub(r'\[.*?]', lambda x: ''.join(x.group(0).split()), usage)
        res = re.sub(r'\(.*?\)', lambda x: ''.join(x.group(0).split()), res)
        res = re.sub(r'<.*?>', lambda x: ''.join(x.group(0).split()), res)
        tmp_dic, token = processing_element(res.split(), token)
        usage_dic.update(tmp_dic)
    return usage_dic, token


def processing_element(line_usage, token):
    usage_dic = {}
    usage_list = []
    for element in line_usage:
        element = element.strip()
        if element[-3:] == '.py':
            token.e_list = element
        elif '(' in element:
            res = re.search(r'\((.*?)\)', element.strip()).group(1)
            usage_dic.update(update_usage_dic(res.split('|'), False))
            usage_list.append(res.split('|'))
        elif '[' in element:
            res = re.search(r'\[(.*?)]', element.strip()).group(1)
            usage_dic.update(update_usage_dic(res.split('|'), False))
            usage_list.append(res.split('|'))
        elif '<' and '...' in element:
            usage_dic.update(update_usage_dic([element], True))
            usage_list.append([element])
        elif '<' in element:
            res = re.search(r'<(.*?)>', element.strip()).group(1)
            usage_dic.update(update_usage_dic([res], True))
            usage_list.append([element])
        else:
            usage_dic.update(update_usage_dic([element], False))
            usage_list.append([element])
    token = update_usage_tree(usage_list, token)
    return usage_dic, token


def update_usage_dic(element_list, is_value):
    tmp_dic = {}
    for element in element_list:
        if is_value and len(element) == 1:
            tmp_dic.update({element: 0})
        elif is_value and len(element) > 1:
            tmp_dic.update({element: None})
        else:
            tmp_dic.update({element: False})
    return tmp_dic


def update_usage_tree(usage_array, token):
    token = update_usage_tree_helper(usage_array, token)
    return token


def update_usage_tree_helper(usage_array, token):
    if len(usage_array) == 0:
        for pointer in token.pointers:
            if '`/0' in pointer.e_list:
                return token
        token.pointers.append(UsageToken('`/0', [], False))
        return token

    current_array = usage_array.pop(0)
    for element in current_array:
        contain = False
        for index, current_pointer in enumerate(token.pointers):
            if element == current_pointer.e_list:
                token.pointers[index] = update_usage_tree_helper(usage_array, token.pointers[index])
                contain = True
        if not contain:
            if element[:1] == "-":
                token.pointers.append(UsageToken(element, [], True))
            else:
                token.pointers.append(UsageToken(element, [], False))
            token.pointers[-1] = update_usage_tree_helper(usage_array, token.pointers[-1])

    return token


def check_usage_pattern(usage_dic, token, turned_on_options):
    return usage_dic, turned_on_options


if __name__ == '__main__':
    main_function()
