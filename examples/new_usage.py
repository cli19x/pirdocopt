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
    def __init__(self, prev=None, next=None):
        self.prev = prev
        self.next = next


class Leaf(Token):
    def __init__(self, text, value=None, prev=None, next=None):
        self.text = text
        self.value = value
        super(Leaf, self).__init__(prev, next)

    def __repr__(self):
        return '%s(%r, %r)' % (self.__class__.__name__, self.text, self.value)

    def flat(self, *types):
        return self if not types or type(self) in types else None

    def match(self, left):
        return True if left else False


class Argument(Leaf):
    """ Placeholder """
    def __init__(self, text, value=None, prev=None, next=None):
        self.value = None if len(text.strip("<>")) > 1 else 0
        super(Argument, self).__init__(text, self.value, prev, next)



class Option(Leaf):
    """ Placeholder """
    def __init__(self, text, value=False, short=False, long=False, prev=None, next=None):
        self.short = short
        self.long = long
        if '=' in text:
            arg = re.search('<\S+>', text).group()
            self.value = None if len(arg.strip("<>"))>1 else 0
        else:
            self.value = None if '=' in text else False
        super(Option, self).__init__(text, self.value, prev, next)


class Command(Leaf):
    """ Placeholder """
    def __init__(self, text, value=None, prev=None, next=None):
        self.value = False
        super(Command, self).__init__(text, self.value, prev, next)

# Used for grouping Tokens by optional, required, mutex, or repeating


class Branch(Token):
    def __init__(self, children, prev=None, next=None):
        self.children = children
        super(Branch, self).__init__(prev, next)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__,
                           ', '.join(repr(a) for a in self.children))

    def flat(self, *types):
        if type(self) in types:
            return self
        return [child.flat(*types) for child in self.children]

class Optional(Branch):
    """ Placeholder """

    def match(self, left):
        for child in self.children:
            match, left = child.match(left)
        return True, left


class Required(Branch):
    """ Placeholder """


class Mutex(Branch):
    """ Placeholder """


class Repeating(Branch):
    """ Placeholder """


# Used for identifying branch tokens (Optional, Required, Mutex, Repeating)
class SpecialToken(Token):
    def __init__(self, prev=None, next=None):
        super(SpecialToken, self).__init__(prev, next)

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
    usages, options_array = docopt_util.processing_string(doc2, False, "testing new_usage")
    usages.pop(0)
    usages, usage_dic = get_patterns_and_dict(usages)
    args = sys.argv[1:]
    for pattern in usages:
        left = args
        for token in pattern:


def get_patterns_and_dict(usages):
    new_usages = []
    usage_dic = {}
    for pattern in usages:
        pattern = re.sub(r'([\[\]\(\)\|]|\.\.\.)', r' \1 ', pattern).split()
        pattern.pop(0)
        pattern = identify_tokens(pattern)
        create_opt_and_req(pattern)
        create_mutex(pattern)
        create_repeating(pattern)
        new_usages.append(pattern)
        usage_dic.update(dict_populate_loop(pattern))
    return new_usages, usage_dic
        
def dict_populate_loop(pattern):
    updated_dic = {}
    for token in pattern:
        if isinstance(token, Branch):
            updated_dic.update(dict_populate_loop(token.children))
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
            res = Required(collected, prev, next) if isinstance(token, Required_Open) else Optional(collected, prev, next)
            pattern.insert(index, res)


def create_mutex(pattern):
    for index, token in enumerate(pattern):
        if isinstance(token, Optional) or isinstance(token, Required):
            create_mutex(token.children)
        elif isinstance(token, Pipe):
            prev = token.prev.prev if token.prev else None
            next = token.next.next if token.next else None
            collected = [token.prev, token.next]
            for i in range(index-1, index+2):
                del pattern[index-1]
            res = Mutex(collected, prev, next)
            pattern.insert(index-1, res)


def create_repeating(pattern):
    for index, token in enumerate(pattern):
        prev = token.prev if token.prev else None
        next = token.next if token.next else None
        if isinstance(token, Optional) or isinstance(token, Required) or isinstance(token, Mutex):
            create_repeating(token.children)
        elif isinstance(token, Ellipsis):
            collected = [token.prev]
            res = Repeating(collected, prev, next)
            for i in range(index-1, index+1):
                del pattern[index-1]
            pattern.insert(index-1, res)


if __name__ == "__main__":
    main_function()
    
