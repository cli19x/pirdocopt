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
    def __init__(self, prev=None, next=None, children=[]):
        self.prev = prev
        self.next = next
        self.children = children


class Leaf(Token):
    def __init__(self, text, value=None, prev=None, next=None, children=[]):
        self.text = text
        self.value = value
        super(Leaf, self).__init__(prev, next, children)

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.text, self.value)

    def flat(self, *types):
        return self if not types or type(self) in types else None

    def match(self, left):
        return True if left else False


class Argument(Leaf):
    """ Placeholder """

    def __init__(self, text, value=None, prev=None, next=None, children=[]):
        self.value = None if len(text.strip("<>")) > 1 else 0
        super(Argument, self).__init__(text, self.value, prev, next, children)

    def match(self, args, index):
        if index < len(args):
            if self.value == 0 and not is_num(args[index]):
                print(f"Argument {self.text} not match 1")
                return False, index+1
            self.value = args[index]
            return True, index+1
        print(f"Argument {self.text} not match 2")
        return False, index+1


class Option(Leaf):
    """ Placeholder """

    def __init__(self, text, value=False, short=False, long=False, prev=None, next=None, children=[]):
        self.short = short
        self.long = long
        if '=' in text:
            arg = re.search('<\S+>', text).group()
            text = re.search('\S+=', text).group().strip("=")
            self.value = None if len(arg.strip("<>")) > 1 else 0
        else:
            self.value = None if '=' in text else False
        super(Option, self).__init__(text, self.value, prev, next, children)

    def match(self, args, index):
        if index < len(args):
            if self.text == args[index]:
                self.value = True
                return True, index+1
        print(f"Option {self.text} not match")
        return False, index+1


class Command(Leaf):
    """ Placeholder """

    def __init__(self, text, value=None, prev=None, next=None, children=[]):
        self.value = False
        super(Command, self).__init__(text, self.value, prev, next, children)

    def match(self, args, index):
        if index < len(args):
            if self.text == args[index]:
                self.value = True
                return True, index+1
        print(f"Command {self.text} not match")
        return False, index+1

# Used for grouping Tokens by optional, required, mutex, or repeating


class Branch(Token):
    def __init__(self, tokens=[], prev=None, next=None, children=[]):
        self.tokens = tokens
        super(Branch, self).__init__(prev, next, children)

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
        child_index = index
        for child in self.tokens:
            is_match, child_index = child.match(args, child_index)
            if not is_match:
                child_index = child_index - 1
        return True, child_index


class Required(Branch):
    """ Placeholder """

    def match(self, args, index):
        child_index = index
        for child in self.tokens:
            is_match, child_index = child.match(args, child_index)
            if not is_match:
                return False, index
        return True, child_index

class Mutex(Branch):
    """ Placeholder """

    def match(self, args, index):
        res, new_index = False, index
        for child in self.tokens:
            res, new_index = child.match(args, index)
            if res:
                return True, new_index
        return False, new_index


class Repeating(Branch):
    """ Placeholder """

    # BUG: index 1 less than it should be when repeating pattern incomplete
    def match(self, args, index):
        is_match, new_index = self.tokens[0].match(args, index)
        #old_index = new_index
        if not is_match:
            return False, new_index
        while new_index < len(args):
            print("Loop")
            is_match, new_index = self.tokens[0].match(args, new_index)
            if not is_match:
                new_index = new_index - 1
                break       
        return True, new_index


# Used for identifying branch tokens (Optional, Required, Mutex, Repeating)
class SpecialToken(Token):
    def __init__(self, prev=None, next=None, children=[]):
        super(SpecialToken, self).__init__(prev, next, children)

    def __repr__(self):
        return self.__class__.__name__


class Optional_Open(SpecialToken):
    """ Placeholder """
    @property
    def closed_class(self):
        return Optional_Closed


class Optional_Closed(SpecialToken):
    """ Placeholder """


class Required_Open(SpecialToken):
    """ Placeholder """
    @property
    def closed_class(self):
        return Required_Closed


class Required_Closed(SpecialToken):
    """ Placeholder """


class Pipe(SpecialToken):
    """ Placeholder """
    # Current limitations: tokens to left and right must be surrounded by own paren
    #   E.g. (run [--fast]) | (jump [--high])


class Ellipsis(SpecialToken):
    """ Placeholder """


def main_function():
    usages, options_array = docopt_util.processing_string(
        doc2, False, "testing new_usage")
    usages.pop(0)
    usages, usage_dic, token_set, tree_heads = get_patterns_and_dict(usages)
    '''print(usages)
    print(usage_dic)
    print(token_set)
    print(tree_heads)'''
    args = sys.argv[1:]
    test_arg = usages[0][0]
    found_patt_match = False
    patt_match = None
    for patt_ind, pattern in enumerate(usages):
        is_match, index = False, 0
        found_patt_match = True
        for token in pattern:
            is_match, index = token.match(args, index)
            if not is_match:
                #print(f"NOT A MATCH\n{usages[0]}\n{args}")
                found_patt_match = False
                break
        if found_patt_match:
            #print("match")
            patt_match = patt_ind
            break
    if patt_match is not None:
        print(f"FOUND A MATCH: {patt_match}")
        for token in usages[patt_match]:
            print(token)
    else:
        print("NO MATCHES FOUND")


def get_patterns_and_dict(usages):
    new_usages = []
    usage_dic = {}
    token_set = []
    tree_heads = []
    for pattern in usages:
        pattern = re.sub(r'([\[\]\(\)\|]|\.\.\.)', r' \1 ', pattern).split()
        pattern.pop(0)
        pattern = identify_tokens(pattern)
        create_opt_and_req(pattern)
        create_mutex(pattern)
        create_repeating(pattern)
        for index, token in enumerate(pattern):
            if isinstance(token.next, SpecialToken):
                token.next = pattern[index+1]
        new_usages.append(pattern)
        usage_dic.update(dict_populate_loop(pattern))
        #print(pattern[0])
        token_set = build_token_set(pattern, token_set)
        tree_heads = build_tree_heads(token_set, pattern[0], tree_heads)

    return new_usages, usage_dic, token_set, tree_heads

def is_num(arg):
    try:
        float(arg)
        return True
    except ValueError:
        return False


def build_tree_heads(token_set, first_token, tree_heads):
    for token in token_set:
        #print(token, first_token)
        if not isinstance(first_token, Branch):
            if token == first_token:
                tree_heads.append(token)
                return tree_heads
        elif isinstance(first_token, Mutex):
            for child in first_token.tokens:
                #print(child)
                if token.text == child.text:
                    tree_heads.append(token)
                    break
        else:
            old_len = len(tree_heads)
            tree_heads = build_tree_heads(token_set, first_token.tokens[0], tree_heads)
            if len(tree_heads) > old_len:
                return tree_heads
    return tree_heads

def build_token_set(pattern, token_set):
    for token in pattern:
        tree_child = token.next if token.next else None
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
                #print(f"Child added to {token}: {tree_child}\t{hex(id(token))}")
                token.children.append(tree_child)

            #if token.text == pattern[0].text:
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
            token = Required_Open()
        elif token == ')':
            token = Required_Closed()
        elif token == '[':
            token = Optional_Open()
        elif token == ']':
            token = Optional_Closed()
        elif token == '|':
            token = Pipe()
        elif token == '...':
            token = Ellipsis()
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
            token.next = new_pat[index+1] if len(new_pat) > 1 else None
        elif index == len(new_pat)-1:
            token.prev = new_pat[index-1]
        else:
            token.prev = new_pat[index-1]
            token.next = new_pat[index+1]
    return new_pat


def create_opt_and_req(pattern):
    length = len(pattern)-1
    for index, token in enumerate(pattern[::-1]):
        index = length - index
        if (isinstance(token, Optional_Open) or isinstance(token, Required_Open)):
            #print(f"Index: {index}, Token: {token}")
            open_class = token.__class__
            closed_class = token.closed_class
            prev = token.prev if token.prev else None
            next = None
            collected = []
            del pattern[index]
            for x in pattern[index:]:
                if isinstance(x, closed_class):
                    next = x.next if x.next else None
                    del pattern[index]
                    break
                collected.append(x)
                del pattern[index]
            collected[0].prev = prev
            collected[-1].next = next
            res = Required(collected, prev, next) if isinstance(
                token, Required_Open) else Optional(collected, prev, next)
            pattern.insert(index, res)


def create_mutex(pattern):
    for index, token in enumerate(pattern):
        if isinstance(token, Optional) or isinstance(token, Required):
            create_mutex(token.tokens)
        elif isinstance(token, Pipe):
            prev = token.prev.prev if token.prev else None
            next = token.next.next if token.next else None
            collected = [token.prev, token.next]
            for tok in collected:
                tok.prev = prev
                tok.next = next
            for i in range(index-1, index+2):
                del pattern[index-1]
            res = Mutex(collected, prev, next)
            pattern.insert(index-1, res)


def create_repeating(pattern):
    for index, token in enumerate(pattern):
        prev = token.prev if token.prev else None
        next = token.next if token.next else None
        if isinstance(token, Optional) or isinstance(token, Required) or isinstance(token, Mutex):
            create_repeating(token.tokens)
        elif isinstance(token, Ellipsis):
            token.prev.next = next
            collected = [token.prev]
            res = Repeating(collected, prev, next)
            for i in range(index-1, index+1):
                del pattern[index-1]
            pattern.insert(index-1, res)


if __name__ == "__main__":
    main_function()
