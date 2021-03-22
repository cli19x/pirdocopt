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


class Token:
    def __init__(self, prev=None, post=None, children=None):
        if children is None:
            children = []
        self.prev = prev
        self.post = post
        self.children = children


class Leaf(Token):
    def __init__(self, text, value=None, prev=None, post=None, children=None):
        if children is None:
            children = []
        self.text = text
        self.value = value
        self.post = post
        super(Leaf, self).__init__(prev, post, children)

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

    def __init__(self, text, value=False, short=False, long=False, prev=None, post=None,
                 children=None):
        if children is None:
            children = []
        self.short = short
        self.long = long
        self.value = value
        if '=' in text:
            arg = re.search('<\\S+>', text).group()
            text = re.search('\\S+=', text).group().strip("=")
            self.value = None if len(arg.strip("<>")) > 1 else 0
        else:
            self.value = None if '=' in text else False
        super(Option, self).__init__(text, self.value, prev, post, children)

    def match(self, args, index):
        is_match = False
        if index < len(args):
            if self.text == args[index]:
                self.value, is_match = True, True
        res_dict = self.get_res_dict(is_match)
        return is_match, index+1, res_dict

    def get_res_dict(self, is_match):
        if not is_match:
            return dict()
        else:
            return dict({self.text: True})

class Command(Leaf):
    """ Placeholder """

    def __init__(self, text, value=False, prev=None, post=None, children=None):
        if children is None:
            children = []
        self.value = value
        super(Command, self).__init__(text, self.value, prev, post, children)

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
        #print(self.tokens)
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
            is_match, new_index, res_dict_item = self.tokens[0].match(args, new_index)
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


def main_function():
    usages, options_array = docopt_util.processing_string(
        doc2, False, "testing new_usage")
    usages.pop(0)
    usages, usage_dic, token_set, tree_heads = get_patterns_and_dict(usages)


    # print(options_array)
    # print(usages)
    #print(usage_dic)
    # print(token_set)\


    #args = sys.argv[1:]

    args = ['naval_fate.py', 'ship', 'shoot', '60', '50']
    args = args[1:]
    usage_dic = check_patterns_with_user_input(tree_heads, usage_dic, args)

    #token = Option('--trap')
    '''for ind, pattern in enumerate(usages):
        index = 0
        is_match = True
        old_dic = usage_dic.copy()
        for token in pattern:
            is_match, index, res_dict = token.match(args, index)
            if not is_match:
                break
            usage_dic.update(res_dict)
        if is_match:
            print(f"PATTERN {ind} MATCHED")
            break
        print(f"pattern {ind} not matched")
        usage_dic = old_dic
    print(usage_dic)

    #print(res_dict, index)'''
    
    '''for head in tree_heads:
        while head.children is not None:
            print(head)
            head = head.children[0]'''

    #usage_dic = check_patterns_with_user_input(tree_heads, usage_dic, args)
    #test_arg = usages[0][0]


def get_patterns_and_dict(usages):
    new_usages = []
    usage_dic = {}
    token_set = []
    tree_heads = []
    for pattern in usages:
        pattern = re.sub(r'([\[\]()|]|\.\.\.)', r' \1 ', pattern).split()
        pattern.pop(0)
        pattern = identify_tokens(pattern)
        create_opt_and_req(pattern)
        create_mutex(pattern)
        create_repeating(pattern)
        for index, token in enumerate(pattern):
            if isinstance(token.post, SpecialToken):
                token.post = pattern[index + 1]
        new_usages.append(pattern)
        usage_dic.update(dict_populate_loop(pattern))
        # print(pattern[0])
        token_set = build_token_set(pattern, token_set)
        tree_heads = build_tree_heads(token_set, pattern[0], tree_heads)

    return new_usages, usage_dic, token_set, tree_heads


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


def build_tree_heads(token_set, first_token, tree_heads):
    for token in token_set:
        # print(token, first_token)
        if not isinstance(first_token, Branch):
            if token == first_token:
                tree_heads.append(token)
                return tree_heads
        elif isinstance(first_token, Mutex):
            for child in first_token.tokens:
                # print(child)
                if token.text == child.text:
                    tree_heads.append(token)
                    break
        else:
            old_len = len(tree_heads)
            tree_heads = build_tree_heads(
                token_set, first_token.tokens[0], tree_heads)
            if len(tree_heads) > old_len:
                return tree_heads
    return tree_heads


def build_token_set(pattern, token_set):
    for token in pattern:
        tree_child = token.post if token.post else None
        if isinstance(token, Branch):
            token_set = build_token_set(token.tokens, token_set)
        else:
            in_set = False
            for t in token_set:
                if token.text == t.text:
                    token = t
                    in_set = True
                    break
            if not in_set:
                token_set.append(token)
            if tree_child:
                # print(f"Child added to {token}: {tree_child}\t{hex(id(token))}")
                token.children.append(tree_child)

            # if token.text == pattern[0].text:
            #   tree_heads.append(token)

    return token_set


def dict_populate_loop(pattern):
    updated_dic = {}
    for token in pattern:
        if isinstance(token, Branch):
            updated_dic.update(dict_populate_loop(token.tokens))
        else:
            updated_dic[token.text] = token.value
    return updated_dic


def identify_tokens(pattern):
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
            token = Option(token, long=True)
        elif token.startswith('-'):
            token = Option(token, short=True)
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
            # print(f"Index: {index}, Token: {token}")
            open_class = token.__class__
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

    res, usage_dic = check_patterns_with_user_input_helper(
        usage_tree, usage_dic, arg)
    return usage_dic if res is not False else None


def check_patterns_with_user_input_helper(children, usage_dic, arg):
    """

     Args:
        children: The List of current node's children.

        usage_dic: The dictionary for output the results of usage pattern.

        arg: Array of user input arguments, either is default or from command line.

    Returns:
        res: Boolean value for if input pattern is matching the patterns in docstring.
        usage_dic: Return the updated usage dictionary or stay the same if no pattern found.

    """

    if len(arg) == 0:
        for child in children:
            if child.match('`/0', 0):
                return True, usage_dic
        return False, usage_dic

    current_element = arg.pop(0)
    res = False
    print(children)
    for child in children:
        print(child)
        # matching the repeat values (<name>...), skip_to is the index of the last repeat element
        # in user argument list
        # return skip_to == -1 if not matching
        # tmp_dic(2) contains {'<name>...': ['e1', 'e2', 'e3']} for repeat values,
        # and {'ship': Ture} for others
        #print([current_element] + arg)
        is_match, skip_to, tmp_dic = child.match([current_element] + arg, 0)
        # skip_to2 is just for the easiness of design of the match function
        is_match2, skip_to2, tmp_dic2 = child.match([current_element], 0)
        print(tmp_dic, tmp_dic2)
        #if not is_match:

        if skip_to > 0:
            arg = arg[skip_to - 1:]
            res, usage_dic = check_patterns_with_user_input_helper(
                child.children, usage_dic, arg)
            usage_dic.update(tmp_dic)
        elif tmp_dic2 is not None:
            res, usage_dic = check_patterns_with_user_input_helper(
                child.children, usage_dic, arg)
            usage_dic.update(tmp_dic2)
    return res, usage_dic


if __name__ == "__main__":
    main_function()
