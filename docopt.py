import re
import sys

import docopt_util


class Token:
    def __init__(self, prev=None, post=None, children=None):
        if children is None:
            children = []
        self.prev = prev
        self.post = post
        self.children = children
        self.index = 0


class Leaf(Token):
    def __init__(self, text, value=None, prev=None, post=None, children=None):
        if children is None:
            children = []
        self.text = text
        self.value = value
        self.post = post
        super(Leaf, self).__init__(prev, post, children)
        self.index = 0

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.text, self.value)

    def flat(self, *types):
        return self if not types or type(self) in types else None

    def match(self, left, index):
        return True if left else False


class Argument(Leaf):
    """ Placeholder """

    def __init__(self, text, prev=None, post=None, children=None):
        if children is None:
            children = []
        self.value = None if len(text.strip("<>")) > 1 else 0
        super(Argument, self).__init__(text, self.value, prev, post, children)
        self.index = 2

    def match(self, args, index):
        is_match = False
        if index < len(args):
            if self.value != 0 or is_num(args[index]):
                self.value, is_match = args[index], True
        res_dict = self.get_res_dict(is_match)
        return is_match, index + 1, res_dict

    def get_res_dict(self, is_match):
        if not is_match:
            return dict()
        else:
            return dict({self.text: self.value})


class Option(Leaf):
    """ Placeholder """

    def __init__(self, text, value=None, has_value=False, short=None, long=None,
                 prev=None, post=None, children=None):
        if children is None:
            children = []
        self.short = short
        self.long = long
        self.value = value
        self.has_value = has_value
        if '=' in text:
            arg = re.search('<\\S+>', text).group()
            text = re.search('\\S+=', text).group().strip("=")
            self.value = None if len(arg.strip("<>")) > 1 else 0
        else:
            self.value = None if '=' in text else False
        super(Option, self).__init__(text, self.value, prev, post, children)
        self.index = 3

    def match(self, args, index):
        is_match = False
        new_index = index + 1
        if index < len(args):
            if self.text == args[index]:
                if self.has_value:
                    if index + 1 < len(args):
                        self.value = args[index + 1]
                        is_match = True
                        new_index = index + 2
                else:
                    self.value = True
                    is_match = True
        res_dict = self.get_res_dict(is_match)
        return is_match, new_index, res_dict

    def get_res_dict(self, is_match):
        if not is_match:
            return dict()
        else:
            return dict({self.text: self.value})


class Command(Leaf):
    """ Placeholder """

    def __init__(self, text, value=False, prev=None, post=None, children=None):
        if children is None:
            children = []
        self.value = value
        super(Command, self).__init__(text, self.value, prev, post, children)
        self.index = 1

    def match(self, args, index):
        is_match = False
        if index < len(args):
            if self.text == args[index]:
                self.value, is_match = True, True
        res_dict = self.get_res_dict(is_match)
        return is_match, index + 1, res_dict

    def get_res_dict(self, is_match):
        if not is_match:
            return dict()
        else:
            return dict({self.text: True})


# Used for grouping Tokens by optional, required, mutex, or repeating


class Branch(Token):
    def __init__(self, tokens=None, prev=None, post=None, children=None):
        if children is None:
            children = []
        if tokens is None:
            tokens = []
        self.tokens = tokens
        super(Branch, self).__init__(prev, post, children)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,
                           ', '.join(repr(a) for a in self.tokens))

    def flat(self, *types):
        if type(self) in types:
            return self
        return [child.flat(*types) for child in self.tokens]


class Optional(Branch):
    """ Placeholder """

    # Currently only implements all-or-nothing
    def match(self, args, index):
        is_match, child_index, res_dict = True, index, dict()
        for child in self.tokens:
            old_index = child_index
            is_match, child_index, child_dict = child.match(args, child_index)
            if not is_match:
                child_index = old_index
            else:
                res_dict.update(child_dict)

        return True, child_index, res_dict


class Required(Branch):
    """ Placeholder """

    def match(self, args, index):
        is_match, child_index, res_dict = True, index, dict()
        for child in self.tokens:
            old_index = child_index
            is_match, child_index, child_dict = child.match(args, child_index)

            if not is_match:
                child_index = old_index
                break
            else:
                res_dict.update(child_dict)
        return is_match, child_index, res_dict


class Mutex(Branch):
    """ Placeholder """

    def match(self, args, index):
        is_match, new_index, res_dict = False, index, dict()
        for child in self.tokens:
            is_match, new_index, temp_dict = child.match(args, index)
            if is_match:
                res_dict = temp_dict
                break
        return is_match, new_index, res_dict


class Repeating(Branch):
    """ Placeholder """

    # BUG: index 1 less than it should be when repeating pattern incomplete
    def match(self, args, index):
        res_dict_full = dict()
        res_list = []
        is_match, new_index, res_dict_item = self.tokens[0].match(args, index)
        res_list.append(res_dict_item)
        if not is_match:
            return False, new_index, dict()
        while new_index < len(args):
            is_match, new_index, res_dict_item = self.tokens[0].match(
                args, new_index)
            if not is_match:
                new_index = new_index - 1
                break
            res_list.append(res_dict_item)
        for item in res_list:
            for key, val in zip(item.keys(), item.values()):
                if key in res_dict_full.keys():
                    if not isinstance(res_dict_full[key], list):
                        res_dict_full[key] = [res_dict_full[key]]
                    res_dict_full[key].append(val)
                else:
                    res_dict_full[key] = [val]
        return True, new_index, res_dict_full


# Used for identifying branch tokens (Optional, Required, Mutex, Repeating)
class SpecialToken(Token):
    def __init__(self, prev=None, post=None, children=None):
        if children is None:
            children = []
        super(SpecialToken, self).__init__(prev, post, children)

    def __repr__(self):
        return self.__class__.__name__


class OptionalOpen(SpecialToken):
    """ Placeholder """

    @property
    def closed_class(self):
        return OptionalClosed


class OptionalClosed(SpecialToken):
    """ Placeholder """


class RequiredOpen(SpecialToken):
    """ Placeholder """

    @property
    def closed_class(self):
        return RequiredClosed


class RequiredClosed(SpecialToken):
    """ Placeholder """


class Pipe(SpecialToken):
    """ Placeholder """
    # Current limitations: tokens to left and right must be surrounded by own paren
    #   E.g. (run [--fast]) | (jump [--high])


class Repeats(SpecialToken):
    """ Placeholder """


def docopt(doc, version=None, help_message=True, argv=None):
    usages, options_array = docopt_util.processing_string(
        doc, help_message, version)
    args = sys.argv[1:]
    if len(args) == 0 and argv is not None:
        args = argv

    if 'Usage:' in usages[0]:
        tmp = usages[0].split()
        if len(tmp) == 1:
            usages.pop(0)
        else:
            usages[0] = ' '.join(tmp.pop(0))

    usages, output_dic, tree_heads = get_patterns_and_dict(usages, options_array)
    output_dic = match_user_input(tree_heads, output_dic, args)
    total_dic, output_string = docopt_util.print_output_dictionary(output_dic)
    print(output_string)
    return total_dic


def match_user_input(tree_heads, usage_dic, args):
    index = 0
    for head in tree_heads:
        head_dict = dict()
        old_index = index
        is_match, index, dic_entry = head.match(args, index)
        if not is_match:
            index = old_index
            continue
        head_dict.update(dic_entry)
        children_match = get_child_match(head.children, args, index, head_dict)
        if children_match:
            usage_dic.update(head_dict)
    return usage_dic


def get_child_match(children, args, index, head_dict):
    children_match = False
    if not children:
        children_match = True
    for child in children:
        child_dict = dict()
        old_index = index
        is_match, index, dic_entry = child.match(args, index)
        if not is_match:
            index = old_index
            continue
        child_dict.update(dic_entry)
        post_match = get_post_match(child, args, index, child_dict)
        if post_match:
            children_match = True
            head_dict.update(child_dict)
            break
    return children_match


def get_post_match(child, args, index, child_dict):
    post = child.post
    post_match = True
    while post:
        is_match, index, dic_entry = post.match(args, index)
        if not is_match:
            post_match = False
            break
        child_dict.update(dic_entry)
        post = post.post
    return post_match


def get_patterns_and_dict(usages, options):
    new_usages = []
    usage_dic = {}
    tree_heads = []
    options_pat = check_option_lines(options)
    for pattern in usages:
        pattern = re.sub(r'([\[\]()|]|\.\.\.)', r' \1 ', pattern).split()
        pattern.pop(0)
        pattern = identify_tokens(pattern, options_pat)
        create_opt_and_req(pattern)
        create_mutex(pattern)
        create_repeating(pattern)
        for index, token in enumerate(pattern):
            if isinstance(token.post, SpecialToken) and index < len(pattern) - 1:
                token.post = pattern[index + 1]
        new_usages.append(pattern)
        usage_dic.update(dict_populate_loop(pattern))
        tree_heads = build_tree_heads(pattern, tree_heads)

    for pattern in new_usages:
        for index, token in enumerate(pattern):
            token.post = pattern[index + 1] if index + \
                                               1 < len(pattern) else None

    return new_usages, usage_dic, tree_heads


def is_num(arg):
    try:
        float(arg)
        return True
    except ValueError:
        return False


def set_children(pattern):
    for token in pattern:
        if token.post:
            token.children.append(token.post)


def build_tree_heads(pattern, tree_heads):
    token = pattern[0]
    tree_child = token.post if token.post else None
    if isinstance(token, Leaf):
        in_set = False
        test_set = [t for t in tree_heads if isinstance(t, Leaf)]
        for t in test_set:
            if token.text == t.text:
                token = t
                in_set = True
                break
        if not in_set:
            tree_heads.append(token)
    else:
        tree_heads.append(token)
    if tree_child:
        token.children.append(tree_child)

    return tree_heads


def dict_populate_loop(pattern):
    updated_dic = {}
    for token in pattern:
        if isinstance(token, Branch):
            updated_dic.update(dict_populate_loop(token.tokens))
        else:
            updated_dic[token.text] = token.value
    return updated_dic


def identify_tokens(pattern, options_pat):
    new_pat = []
    for index, token in enumerate(pattern):
        if token == '(':
            token = RequiredOpen()
        elif token == ')':
            token = RequiredClosed()
        elif token == '[':
            token = OptionalOpen()
        elif token == ']':
            token = OptionalClosed()
        elif token == '|':
            token = Pipe()
        elif token == '...':
            token = Repeats()
        elif (token.startswith('<') and token.endswith('>')) or token.isupper():
            token = Argument(token)
        elif token.startswith('--'):
            token = get_match_option(token, options_pat)
        elif token.startswith('-'):
            token = get_match_option(token, options_pat)
        else:
            token = Command(token)
        new_pat.append(token)
    for index, token in enumerate(new_pat):
        if index == 0:
            token.post = new_pat[index + 1] if len(new_pat) > 1 else None
        elif index == len(new_pat) - 1:
            token.prev = new_pat[index - 1]
        else:
            token.prev = new_pat[index - 1]
            token.post = new_pat[index + 1]
    return new_pat


def create_opt_and_req(pattern):
    length = len(pattern) - 1
    for index, token in enumerate(pattern[::-1]):
        index = length - index
        if isinstance(token, OptionalOpen) or isinstance(token, RequiredOpen):
            closed_class = token.closed_class
            prev = token.prev if token.prev else None
            post = None
            collected = []
            del pattern[index]
            for x in pattern[index:]:
                if isinstance(x, closed_class):
                    post = x.post if x.post else None
                    del pattern[index]
                    break
                collected.append(x)
                del pattern[index]
            collected[0].prev = prev
            collected[-1].post = post
            res = Required(collected, prev, post) if isinstance(
                token, RequiredOpen) else Optional(collected, prev, post)
            pattern.insert(index, res)


def create_mutex(pattern):
    for index, token in enumerate(pattern):
        if isinstance(token, Optional) or isinstance(token, Required):
            create_mutex(token.tokens)
        elif isinstance(token, Pipe):
            prev = token.prev.prev if token.prev else None
            post = token.post.post if token.post else None
            collected = [token.prev, token.post]
            for tok in collected:
                tok.prev = prev
                tok.post = post
            for i in range(index - 1, index + 2):
                del pattern[index - 1]
            res = Mutex(collected, prev, post)
            pattern.insert(index - 1, res)


def create_repeating(pattern):
    for index, token in enumerate(pattern):
        prev = token.prev if token.prev else None
        post = token.post if token.post else None
        if isinstance(token, Optional) or isinstance(token, Required) or isinstance(token, Mutex):
            create_repeating(token.tokens)
        elif isinstance(token, Repeats):
            token.prev.post = post
            collected = [token.prev]
            res = Repeating(collected, prev, post)
            for i in range(index - 1, index + 1):
                del pattern[index - 1]
            pattern.insert(index - 1, res)


# Match token (keyword for option) with option object in the option pattern array
def get_match_option(token, options_pat):
    """
        Args:
            token: A string that represent the keyword for option
            options_pat: Array of option objects
        Returns:
            option: return option object if found else return None
        >>>pat = [Option('--help', False), Option('--sorted', False),
        >>> Option('--output', './test.txt'), Option('--version', False)]
        >>> get_match_option('--help', pat)
        Option('--help', False)
        >>> get_match_option('--hello', pat)
        Option('--hello', False)
        >>> get_match_option('--hi', [None])
        Option('--hi', False)
        """
    has_value = False
    if '=' in token:
        has_value = True
        token = re.search('\\S+=', token).group().strip("=")

    for option in options_pat:
        if option is None:
            return create_tmp_token(token, has_value)
        if token == option.long or token == option.short:
            return option

    return create_tmp_token(token, has_value)


def create_tmp_token(token, has_value):
    """
        Args:
            token: A string that represent the keyword for option
            has_value: Boolean value for check if keyword contain value
        Returns:
            option: return option object
        >>> create_tmp_token('--hello', False)
        Option('--hello', False)
        >>> create_tmp_token('--hi', True)
        Option('--hello', True)
        """
    if token.startswith('--'):
        if has_value:
            return Option(text=token, value=None, has_value=has_value,  short=None, long=token)
        else:
            return Option(token, False, has_value, None, token)

    elif token.startswith('-'):
        if has_value:
            return Option(text=token, value=None, has_value=has_value,  short=token, long=None)
        else:
            return Option(token, False, has_value, token, None)


# Process options from docstring, treat lines that
# starts with '-' or '--' as options
def check_option_lines(options):
    """
    Args:
        options: options the options strings from docstring.

    Returns:
        new_pat: the array that holds all options objects.

    >>> check_option_lines(options= "-h --help")
    [Option('-h')]
    >>> check_option_lines(options= "hello world")
    []
    """
    options_pat = []
    for line in options:
        tmp_array = line.split()
        if len(tmp_array) > 0 and tmp_array[0].strip()[:1] != '-':
            continue
        token = None
        for count, element in enumerate(tmp_array, start=0):

            if element[:2] == '--':
                token = check_option_lines_long(element, tmp_array, count, token)
            elif element[:1] == '-':
                token = check_option_lines_short(element, tmp_array, count, token)

        token = find_default_value(line, token)
        options_pat.append(token)
    return options_pat


# create the Option with long keyword type if the current keyword is not exists.
# else insert the long version of keyword into the existing keyword object.
def check_option_lines_long(element, tmp_array, count, token):
    """
       Args:
           element: the keyword of the current option.
           tmp_array: the string the contains the current line of option description.
           count: the index of current keyword in the option line.
           token: the class object of Option that holds information of option. If object is None,
                  then create a brand new object for the new keyword.

       Returns:
           token: the updated options object with long form of the keyword.

       >>> check_option_lines_long('--value=<help>', ['--value=<help>', 'Input', 'value'], 0, None)
       token = Option('--value', None, True, None, '--value')
       >>> check_option_lines_long('--value', ['--value', 'HELP'], 0, None)
       token = Option('--value', None, True, None, '--value')
       >>> check_option_lines_long('--help', ['--help', 'show', 'help', 'message'], 0, None)
       token = Option(''--help', False, False, None, ''--help')
       """
    if len(tmp_array) > count + 1 and tmp_array[count + 1].isupper():
        if token is None:
            token = Option(element, None, has_value=True, short=None, long=element)
        else:
            token.long = element
            token.text = element
    elif '=' in element:
        if token is None:
            text = re.search('\\S+=', element).group().strip("=")
            token = Option(text, None, has_value=True, short=None, long=text)
        else:
            token.long = re.search('\\S+=', element).group().strip("=")
            token.text = re.search('\\S+=', element).group().strip("=")
    else:
        if token is None:
            token = Option(element, False, has_value=False, short=None, long=element)
        else:
            token.long = element
            token.text = element
    return token


# create the Option with short keyword type if the current keyword is not exists.
# else insert the short version of keyword into the existing keyword object.
def check_option_lines_short(element, tmp_array, count, token):
    """
    Args:
        element: the keyword of the current option.
        tmp_array: the string the contains the current line of option description.
        count: the index of current keyword in the option line.
        token: the class object of Option that holds information of option.

        Returns:
            token: the updated options object with short form of the keyword.

       >>> check_option_lines_long('-v=<help>', ['-v=<help>', 'Input', 'value'], 0, None)
       token = Option('-v', None, True, '-v', None)
       >>> check_option_lines_long('-v', ['-v', 'HELP'], 0, None)
       token = Option('-v', None, True, '-v', None)
       >>> check_option_lines_long('-h', ['-h', 'show', 'help', 'message'], 0, None)
       token = Option('-h', False, False, '-h', None)
    """
    if len(tmp_array) > count + 1 and tmp_array[count + 1].isupper():
        if token is None:
            token = Option(element, None, has_value=True, short=element, long=None)
        else:
            token.short = element
    elif '=' in element:
        if token is None:
            text = re.search('\\S+=', element).group().strip("=")
            token = Option(text, None, has_value=True, short=text, long=None)
        else:
            token.short = re.search('\\S+=', element).group().strip("=")
    else:
        if token is None:
            token = Option(element, False, has_value=False, short=element, long=None)
        else:
            token.short = element
    return token


# A function for finding whether the current line of option has
# a default value that specify by the programmer
def find_default_value(line, token):
    """
    Args:
        line: a string that holds the current line.
        token: The toekn object for holding option.

    Returns:
        token: the updated token accroding the existence of default value

    >>> tmp_token = Option('-v', None, True, '-v', None)
    >>> find_default_value('-v FILE  input file [default: ./test.txt].', tmp_token)
    tmp_token = Option('-v', './test.txt', True, '-v', None)

    >>> tmp_token = Option('--location', None, True, '-l', '--location')
    >>> find_default_value('-l=<location_value>  insert coordinate [default: 10.88].', tmp_token)
    tmp_token = Option('--location', 10.88, True, '-l', '--location')
    """

    matching = re.search(r'\[.*?]', line)
    if matching is not None:
        default_value = matching.group(0)[1:-1].strip()

        # Test if this line of docstring contains a default value
        if re.search('default:', default_value, re.IGNORECASE):
            try:
                int(default_value.split()[1])
                token.value = int(default_value.split()[1])
            except ValueError:
                try:
                    float(default_value.split()[1])
                    token.value = float(default_value.split()[1])
                except ValueError:
                    token.value = default_value.split()[1]
    return token
