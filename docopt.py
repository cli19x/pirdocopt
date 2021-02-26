"""
  docopt is for displaying the usages and options table that written by the programmer
  to the users. this program allows....
"""


import sys
import re
import docopt_util


# Object for storing token information
# @param text stores the raw text of the token
# @param left is a pointer to the token to the left in the usage pattern
# @param right is a pointer to the token to the right in the usage pattern
# @param ty denotes the type of the token (Argument, Command, or Option)
# @param is_req denotes whether the token is required or optional
# (True if required, False if optional)
class Token:
    """ Class for holding usages patterns

    """

    def __getitem__(self, item):
        pass

    def __init__(self, text, left, right, ty):
        self.txt = text
        self.left = left
        self.right = right
        self.type = ty
        self.is_req = True

    # def __str__(self):
    #    return self.txt

    def __repr__(self):
        return self.txt


#
def docopt(doc, argv=None, help_message=True, version=None):
    """ Main function for docopt program
    Args:
        doc: docstring that pass from the user program
        argv: programmer can pre-pass some parameters into docopt and
              those parameters is treat as default existing arguments
        help_message: user can specify whether they want docopt to display
                      the help message whenever user execute the program
        version: programmers can specify the version of
                 the project and display to user
    Returns:
        total_dic: returns the complete dictionary from parameters passed in

    >>>  doc0 = "Perfect" \
    >>>
    >>>         "Usage:" \
    >>>           "naval_fate.py ship new <name>..." \
    >>>           "naval_fate.py ship <name> move <x> <y> [--speed=<kn>]" \
    >>>
    >>>         "Options:" \
    >>>           '-h --help --helping --haha -hhh Show this screen.' \
    >>>           '-o FILE --output=<value>  Speed in knots [default: ./test.txt].' \
    >>>           '--speed=<kn> -s KN  Speed in knots [default: 10].' \
    >>>
    >>>  docopt(doc=doc0, version="test 2.0", help_message=False,
    >>>                    argv=['ship', 'Titanic', 'move', 10, 90, '--speed=70'])
    {'ship': True, 'new': False, '<name>...': False, 'name': 'Titanic', 'move': True,
    'x': 10, 'y': 90, '--helping': False, '--output': './test.txt', '--speed': 70}
    """

    usages, options = docopt_util.processing_string(doc, help_message, version)
    options_dic = options_parser(argv, sys.argv, options)
    usage_dic = usage_parser(usages, argv, sys.argv[1:])
    total_dic, output_string = docopt_util.print_output_dictionary(usage_dic, options_dic)
    print(output_string)
    return total_dic


def usage_parser(usages, argv, user_argv):
    """Matches user input with usage patterns and returns populated usage_dic.
    Args:
        usages: List of raw usage patterns.
        argv: List of arguments provided by the programmer
        user_argv: List of arguments provided by the user
    Returns:
        usage_dic: Dictionary populated with keys from the usage patterns.
            Appropriate values are filled in from either argv or user_argv.
    >>> usages = ['Usage:',\
    >>>     "  naval_fate.py ship new <name>",\
    >>>     "  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]",\
    >>>     "  naval_fate.py ship shoot <x> <y>",\
    >>>     "  naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]",\
    >>>     "  naval_fate.py (-h | --help)",\
    >>>     "  naval_fate.py --version"]
    >>> args1 = ["ship", "new", "Boat"]
    >>> args2 = ["ship", "new"]
    >>> args3 = ["ship", "shoot", "50", "100"]
    >>> args4 = ["ship", "Boat", "move", "50", "100"]
    >>> args5 = ["mine", "set", "remove", "50", "100", "--drifting"]
    >>> args6 = ["mine", "remove", "50", "100"]
    >>> usage_dic_1 = usage_parser(usages.copy(), None, args1)
    >>> assert usage_dic_1["ship"] is True and usage_dic_1["new"] is True \
    >>>     and usage_dic_1["name"] == "Boat"
    >>> usage_parser(usages.copy(), None, args2)
    Traceback (most recent call last):
        ...
    Exception: No matching usage pattern found.
    >>> usage_dic_3 = usage_parser(usages.copy(), args3, None)
    >>> assert usage_dic_3["ship"] is True and usage_dic_3["shoot"] is True \
    >>>     and usage_dic_3["x"] == '50' and usage_dic_3["y"] == '100'
    >>> usage_dic_4 = usage_parser(usages.copy(), args4, None)
    >>> assert usage_dic_3["ship"] is True and usage_dic_3["shoot"] is True \
    >>>     and usage_dic_3["x"] == '50' and usage_dic_3["y"] == '100'
    >>> usage_parser(usages.copy(), None, args5)
    Traceback (most recent call last):
        ...
    Exception: No matching usage pattern found.
    >>> usage_dic_6 = usage_parser(usages.copy(), args6, None)
    >>> assert usage_dic_6["mine"] is True and usage_dic_6["remove"] is True \
    >>>     and usage_dic_6["x"] == '50' and usage_dic_6["set"] is False
    """
    arguments = user_argv
    if argv is not None:
        arguments = argv
    patterns, usage_dic = parse_usage(usages)
    pattern_to_use = find_matching_pattern(patterns, arguments)
    populate_usage_dic(pattern_to_use, patterns, arguments, usage_dic)
    return usage_dic


def split_token(token):
    """Splits Token by '|' and returns list of separated Tokens.
    Args:
        token: A Token object with a txt parameter of the form "token1|token2".
    Returns:
        res: List of Token objects separated by '|'.
            e.g. ["token1", "token2"]
    >>> arg1 = Token("comm1|comm2", None, None, "Command")
    >>> arg2 = Token("--opt1|--opt2", None, None, "Option")
    >>> res1 = split_token(arg1)
    >>> res2 = split_token(arg2)
    >>> assert res1[0].txt == "comm1" and res1[1].txt == "comm2" and res1[0].type == "Command"
    >>> assert res2[0].txt == "--opt1" and res2[1].txt == "--opt2" and res2[0].type == "Option"
    """
    raw_split = token.txt.split('|')
    res = []
    for index, raw_t in enumerate(raw_split):

        # Create first Token object
        if index == 0:
            token_obj = Token(raw_t, token.left, None, None)
            token_obj.is_req = token.is_req
            res.append(token_obj)

        # Create rest of the Token objects
        else:
            token_obj = Token(raw_t, res[index - 1], None, None)
            token_obj.is_req = token.is_req
            res.append(token_obj)
            res[index].right = token_obj  # Link previous token to new token
            index += 1

        # Set type for split tokens
        token_obj.type = token.type

    res[len(res) - 1].right = token.right

    return res


def convert_tokens(pattern, name):
    """Extracts raw pattern tokens and converts them to list of converted Tokens.
    Args:
        pattern: String containing a single usage pattern.
        name: The name of the program.
    Returns:
        token_objects: A linked list of Token objects.
    >>> p_name = "myProgram.py"
    >>> tmp_p = "  myProgram.py arg1 arg2 arg3"
    >>> tokens = convert_tokens(tmp_p, p_name)
    >>> assert tokens[0].txt == "arg1" and tokens[1].txt == "arg2" and tokens[2].txt == "arg3"
    """
    # Split pattern into individual tokens and remove leading empty space
    tokens_raw = pattern.split(" ")
    tokens_raw.pop(0)
    tokens_raw.pop(0)

    token_objects = list()
    index = 0

    # Convert raw token to Token format, maintained as a linked list
    for token_raw in tokens_raw:
        if token_raw != name:
            if not token_objects:
                token_obj = Token(token_raw, None, None, None)
                token_objects.append(token_obj)
            else:
                token_obj = Token(token_raw, token_objects[index], None, None)
                token_objects[index].right = token_obj
                token_objects.append(token_obj)
                index += 1
    return token_objects


def parse_args(tokens):
    """Sets type attribute for all argument tokens to Argument.
    Args:
        tokens: List of Token objects for a given pattern.
    >>> tmp_tokens = [Token("<arg>", None, None, None), Token("extra", None, None, None), \
    >>>       Token("ARG", None, None, None)]
    >>> parse_args(tmp_tokens)
    >>> assert tmp_tokens[0].type == "Argument" and tmp_tokens[1].type != "Argument"  \
    >>>       and tmp_tokens[2].type == "Argument"
    """
    for token in tokens:
        if token.txt.startswith('<') is True and token.txt.endswith('>') is True:
            token.type = "Argument"
        else:
            if token.txt.isupper():
                token.type = "Argument"


def parse_options(tokens):
    """Sets type attribute for all option tokens to Option.
    Args:
        tokens: List of Token objects for a given pattern.
    >>> tmp_tokens = [Token("extra-", None, None, None), Token("-o", None, None, None),
    >>>       Token("--option", None, None, None)]
    >>> parse_options(tmp_tokens)
    >>> assert tmp_tokens[0].type != "Option" and tmp_tokens[1].type == "Option" and \
    >>>       tmp_tokens[2].type == "Option"
    """
    for token in tokens:
        if token.txt.startswith('-') is True:
            token.type = "Option"


def parse_commands(tokens):
    """Sets type attribute for all command tokens to Command.
    Args:
        tokens: List of Token objects for a given pattern.
    >>> tmp_tokens = [Token("|", None, None, None), Token("-o", None, None, "Option")]
    >>> tmp_tokens.extend( \
    >>>     [Token("<arg>", None, None, "Argument"), Token("comm", None, None, None)])
    >>> parse_commands(tmp_tokens)
    >>> assert tmp_tokens[0].type != "Command" and tmp_tokens[1].type == "Option" and tmp_tokens[\
    >>>     2].type == "Argument" and tmp_tokens[\
    >>>            3].type == "Command"
    """
    for token in tokens:
        # Ignore lone '|' tokens
        if token.txt != '|':
            # If token isn't an argument or an option, it must be a command
            if token.type != "Argument" and token.type != "Option":
                token.type = "Command"


def parse_mutex(token_objects):
    """Replace tokens with mutex elements with a single list of mutex tokens.
    Args:
        token_objects: List of Token objects for a given pattern
    >>> t1 = Token("mu1|mu2", None, None, "Command")
    >>> t2 = Token("--opt", None, None, "Option")
    >>> t3 = Token("--tex1", None, None, "Option")
    >>> t4 = Token("|", None, None, None)
    >>> t5 = Token("--tex2", None, None, "Option")
    >>> t1.right = t2
    >>> t2.left, t2.right = t1, t3
    >>> t3.left, t3.right = t2, t4
    >>> t4.left, t4.right = t3, t5
    >>> t5.left = t4
    >>> tokens = [t1, t2, t3, t4, t5]
    >>> parse_mutex(tokens)
    >>> assert tokens[0][0].txt == "mu1" and tokens[0][0].type == "Command"
    >>> assert tokens[0][1].txt == "mu2" and tokens[0][1].type == "Command"
    >>> assert tokens[1].txt == "--opt" and tokens[1].type == "Option"
    >>> assert tokens[2][0].txt == "--tex1" and tokens[2][0].type == "Option"
    >>> assert tokens[2][1].txt == "--tex2" and tokens[2][1].type == "Option"
    """
    for index, token in enumerate(token_objects):
        if token.txt == '|':
            token_objects[index - 1] = [token.left, token.right]
            token_objects.remove(token.right)
            token_objects.remove(token)
        elif '|' in token.txt:
            token_objects[index] = split_token(token)


def build_usage_dic(token_objects):
    """Uses finalized list of Token objects to return a default-value populated usage_dic.
    Args:
        token_objects: Finalized list of Token objects for a given pattern.
            All attributes for each Token object are properly set.
    Returns:
        usage_dic:
            Dictionary with arguments and commands as keys for a given pattern.
            Default values (None and False) are set.
    >>> t1 = [Token("comm1", None, None, "Command"),\
    >>>       Token("comm2", None, None, "Command")]
    >>> t2 = Token("<arg1>", None, None, "Argument")
    >>> t3 = Token("comm3", None, None, "Command")
    >>> t4 = Token("<arg2>", None, None, "Argument")
    >>> tokens = [t1, t2, t3, t4]
    >>> build_usage_dic(tokens)
    {"comm1": False, "comm2": False, "arg1": None, "comm3": False, "arg2": None}
    """
    usage_dic = {}
    for token in token_objects:
        if isinstance(token, list):
            for tok in token:
                if tok.type == "Command":
                    usage_dic[tok.txt] = False
        else:
            if token.type == "Argument":
                usage_dic[token.txt.strip("<>")] = None
            if token.type == "Command":
                usage_dic[token.txt] = False
    return usage_dic


def process_paren(tokens, open_c):
    """Process and label tokens as optional or required using [] and ().
    Args:
        tokens: List of Token objects for a given pattern.
        open_c: Character used to denote whether to process () or []
    Raises:
        Exception: If there is an unclosed '(' or '['.
    >>> process_paren([Token("[<arg2>", None, None, None)])
    Traceback (most recent call last):
        ...
    Exception: Could not find closed paren or bracket.
    """
    if open_c == '(':
        closed_c = ')'
        is_req = True
    else:
        closed_c = ']'
        is_req = False
    for token in tokens:
        if open_c in token.txt:
            complete = False
            token.txt = token.txt.strip(open_c)
            # if closed parenthesis is in the same token
            if closed_c in token.txt:
                token.txt = token.txt.strip(closed_c)
                token.is_req = is_req
            else:
                token.is_req = is_req
                temp_required = [token]
                token = token.right
                # search for closed parenthesis until we find it or reach the end of the pattern
                while complete is False and token is not None:
                    token.is_req = is_req
                    temp_required.append(token)
                    if closed_c in token.txt:
                        complete = True
                        token.txt = token.txt.strip(closed_c)
                    else:
                        token = token.right
                if complete is False:
                    raise Exception("Could not find closed paren or bracket.")


def parse_usage(usages):
    """Processes usages string to return default usage_dic and list of tokens for each pattern.
    Args:
        usages: List of raw usage patterns.
    Returns:
        patterns: Nested list of finalized tokens for each pattern.
        usage_dic: Dictionary with keys as commands and args from all patterns.
            Default values are set.
    >>> tmp_u = ['Usage:', '  myProgram.py <arg1> comm1 --opt1']
    >>> pat, u = parse_usage(tmp_u)
    >>> assert u == {"arg1":None, "comm1":None}
    >>> assert pat[0][0].txt == "<arg1>" and pat[0][0].type == "Argument"
    >>> assert pat[0][1].txt == "comm1" and pat[0][1].type == "Command"
    >>> assert pat[0][2].txt == "--opt1" and pat[0][2].type == "Option"
    """
    # Extract program name
    usages.pop(0)
    usages_split = usages[1].split(" ")
    name = usages_split[2]
    patterns = []
    usage_dic = {}

    # Parse each pattern in Usages
    for pattern in usages:
        # Convert tokens in pattern to a linked list
        token_objects = convert_tokens(pattern, name)

        # Process required tokens
        process_paren(token_objects, '(')

        # Process optional tokens
        process_paren(token_objects, '[')

        parse_args(token_objects)
        parse_options(token_objects)
        parse_commands(token_objects)

        # Handle mutually exclusive elements
        parse_mutex(token_objects)

        # Build the usage dic using finalized token objects
        usage_dic.update(build_usage_dic(token_objects))

        # Append the finalized token list to the list of patterns
        patterns.append(token_objects)

    return patterns, usage_dic


def check_mutex(index, token, arguments):
    """Checks if input matches only one of the mutex tokens, returns false if no conflict.
    Args:
        index: Index value of which token we are examining.
        token: Usage Token object we are examining.
        arguments: List of user input tokens.
    Returns:
        bool: True if a conflict is found, False otherwise.
    >>> tmp_token = [Token("comm1", None, None, "Command"),\
    >>>     Token("comm2", None, None, "Command")]
    >>> args = ["blah", "bleh", "comm1", "blih"]
    >>> check_mutex(2, tmp_token, args)
    False
    >>> args.insert(3, "comm2")
    >>> check_mutex(2, tmp_token, args)
    True
    >>> args = ["blah", "bleh", "blih"]
    >>> check_mutex(2, tmp_token, args)
    True
    """
    found_conflict = False
    if isinstance(token, list):
        if token[0].is_req is False and index >= len(arguments):
            arguments.insert(index, "None")
            return False
        found_mutex_match = False
        for tok in token:
            if arguments[index] == tok.txt:
                found_mutex_match = True

                # Check if next input token is also in mutex list
                if index + 1 < len(arguments):
                    if any(n.txt == arguments[index + 1] for n in token):
                        found_conflict = True
                break
        if found_mutex_match is False:
            if token[0].is_req is True:
                found_conflict = True
            else:
                if token[0].right is not None:
                    arguments.insert(index, "None")
                else:
                    found_conflict = True
    return found_conflict


def check_tokens(index, token, arguments):
    """Check individual tokens for a match with corresponding input token.
    Args:
        index: Index value of which token we are examining.
        token: Usage Token object we are examining.
        arguments: List of user input tokens.
    Returns:
        bool: True if a conflict is found, False otherwise.
    >>> tmp_token = Token("comm1", None, None, "Command")
    >>> check_tokens(1, tmp_token, ["<arg1>", "comm1"])
    False
    >>> check_tokens(1, tmp_token, ["<arg1>", "--opt1"])
    True
    >>> tmp_token = Token("--opt1=<kn>", None, None, "Option")
    >>> check_tokens(1, tmp_token, ["<arg1>", "--opt1=50"])
    False
    >>> check_tokens(1, tmp_token, ["<arg1>", "comm1"])
    True
    """
    found_conflict = False
    # Handle missing optional arguments
    if token.type == "Argument" and token.is_req is False:
        if arguments[index] == \
                (token.right.txt if isinstance(token.right, Token) else token.right[0].txt):
            arguments.insert(index, "None")

    # If pattern token is a command, check if input token matches
    elif token.type == "Command":
        if arguments[index] != token.txt:
            # Ignore if optional, break if required
            if token.is_req is True:
                found_conflict = True
            else:
                arguments.insert(index, "None")

    # If pattern token is an option, check if input token matches
    elif token.type == "Option":
        input_token = arguments[index]
        p_token = token.txt
        # Ignore option arguments
        if '=' in arguments[index] and '=' in token.txt:
            input_token = arguments[index][:arguments[index].find('=')]
            p_token = p_token[:p_token.find('=')]
        if input_token != p_token:
            # Ignore if optional, break if required
            if token.is_req is True:
                found_conflict = True
            else:
                arguments.insert(index, "None")
    return found_conflict


def find_conflict(pat, arguments):
    """Compare user args with a usage pattern p, return false if no conflict.
    Args:
        pat: List of Token objects for the usage pattern we are checking.
        arguments: List of user input tokens.
    Returns:
        bool: True if a conflict is found, False otherwise.
    >>> usage = [[Token("mut1", None, None, "Command"),\
    >>>     Token("mut2", None, None, "Command")]]
    >>> usage.extend([Token("<arg1>", None, None, "Argument"),\
    >>>     Token("--opt1", None, None, "Option")])
    >>> args = ["mut1", "50", "--opt1"]
    >>> find_conflict(usage, args)
    False
    >>> args = ["mut1", "mut2", "50", "--opt1"]
    >>> find_conflict(usage, args)
    True
    >>> usage[2].is_req = False
    >>> find_conflict(usage, ["mut2", "50"])
    False
    """
    # Used to check if the pattern does not match, success if found_conflict remains False
    found_conflict = False
    for index, token in enumerate(pat):

        if isinstance(token, list):
            found_conflict = check_mutex(index, token, arguments)
            if found_conflict is True:
                break

        # Check if input doesn't contain trailing optional token
        elif token.is_req is False and index >= len(arguments):
            arguments.insert(index, "None")
            continue

        else:
            found_conflict = check_tokens(index, token, arguments)
            if found_conflict is True:
                break

    return found_conflict


def find_matching_pattern(patterns, arguments):
    """Finds which usage pattern matches user args and returns index of that pattern.
    Args:
        patterns: Nested list of finalized Tokens for each pattern.
        arguments: List of user input tokens.
    Returns:
        pattern_to_use: Index of first usage pattern match found.
    >>> pattern1 = [Token("comm1", None, None, "Command")]
    >>> pattern1.append(Token("<arg1>", None, None, "Argument"))
    >>> pattern1.append(Token("<arg2>", None, None, "Argument"))
    >>> pattern1.append([Token("--opt1", None, None, "Option"),\
    >>>     Token("--opt2", None, None, "Option")])
    >>> pattern1[3][0].is_req, pattern1[3][1].is_req = False, False
    >>> pattern2 = [[Token("comm1", None, None, "Command"),\
    >>>     Token("comm2", None, None, "Command")]]
    >>> pattern2.append(Token("-o", None, None, "Option"))
    >>> pattern2.append(Token("ARG3", None, None, "Argument"))
    >>> tmp_patterns = [pattern1, pattern2]
    >>> args1 = ["comm1", "50", "Mine", "--opt2"]
    >>> args2 = ["comm1", "100", "Yours", "--opt1"]
    >>> args3 = ["comm2", "-o", "shoot"]
    >>> args4 = ["comm1", "50", "Mine"]
    >>> args5 = ["comm1", "comm2", "-o", "shoot"]
    >>> find_matching_pattern(tmp_patterns, args1)
    0
    >>> find_matching_pattern(tmp_patterns, args2)
    0
    >>> find_matching_pattern(tmp_patterns, args3)
    1
    >>> find_matching_pattern(tmp_patterns, args4)
    0
    >>> find_matching_pattern(tmp_patterns, args5)
    None
    """
    pattern_to_use = None

    # Explore each pattern to determine which one matches the input
    for num, pat in enumerate(patterns):

        num_req = 0
        # Get number of req tokens for each pattern
        for tok in pat:
            if isinstance(tok, Token):
                if tok.is_req is True:
                    num_req += 1
            else:
                if tok[0].is_req is True:
                    num_req += 1

        if len(arguments) < num_req:
            continue

        # Skip if more input tokens than tokens in the pattern
        if len(arguments) > len(pat):
            continue

        if find_conflict(pat, arguments) is False:
            pattern_to_use = num
            break
    return pattern_to_use


def populate_usage_dic(pattern_to_use, patterns, arguments, usage_dic):
    """Fill usage_dic with appropriate input values if pattern match found.
    Args:
        pattern_to_use: Index of first matching usage pattern found.
        patterns: Nested list of finalized Tokens for each pattern.
        arguments: List of user input tokens.
        usage_dic: Dictionary with keys as commands and args from all patterns.
            Default values are currently set.
    Raises:
        Exception: If pattern_to_use is None.
            This means that no matching usage pattern was found.
    >>> pattern1 = [docopt.Token("comm1", None, None, "Command")]
    >>> pattern1.append(docopt.Token("<arg1>", None, None, "Argument"))
    >>> pattern1.append(docopt.Token("<arg2>", None, None, "Argument"))
    >>> pattern1.append([docopt.Token("--opt1", None, None, "Option"),\
    >>>     docopt.Token("--opt2", None, None, "Option")])
    >>> pattern1[3][0].is_req, pattern1[3][1].is_req = False, False
    >>> pattern2 = [[docopt.Token("comm1", None, None, "Command"),\
    >>>     docopt.Token("comm2", None, None, "Command")]]
    >>> pattern2.append(docopt.Token("-o", None, None, "Option"))
    >>> pattern2.append(docopt.Token("ARG3", None, None, "Argument"))
    >>> patterns = [pattern1, pattern2]
    >>> usage_dic_1 = {"comm1": False, "comm2": False, "arg1": None, "arg2": None, "ARG3": None}
    >>> usage_dic_2 = {"comm1": False, "comm2": False, "arg1": None, "arg2": None, "ARG3": None}
    >>> args1 = ["comm1", "50", "100", "--opt1"]
    >>> args2 = ["comm2", "-o", "shoot"]
    >>> populate_usage_dic(None, patterns, args1, usage_dic_1)
    Traceback (most recent call last):
        ...
    Exception: No matching usage pattern found.
    >>> populate_usage_dic(0, patterns, args1, usage_dic_1)
    >>> assert usage_dic_1 == {"comm1": True, "comm2": False, "arg1": '50', "arg2": '100', \
    >>>     "ARG3": None}
    >>> populate_usage_dic(1, patterns, args2, usage_dic_2)
    >>> assert usage_dic_2 == {"comm1": False, "comm2": True, "arg1": None, "arg2": None,\
    >>>     "ARG3": "shoot"}
    """
    if pattern_to_use is not None:
        for index, token in enumerate(patterns[pattern_to_use]):
            if isinstance(token, list):
                if token[0].type != "Option":
                    usage_dic[arguments[index]] = True
            else:
                if token.type == "Argument":
                    usage_dic[token.txt.strip('<>')] = arguments[index]
                elif token.type == "Command":
                    # Check if input ignores optional command
                    if arguments[index] != "None":
                        usage_dic[token.txt] = True
    else:
        raise Exception("No matching usage pattern found.")


# Main function for checking options
def options_parser(argv, user_argv, options):
    """
    Args:
        argv: the default arguments that specify by the programmer.
        user_argv: the arguments passed from user command line.
        options: the options strings from docstring.

    Returns:
        returns the built options dictionary from another method.

    >>> options_parser(argv= ['--help'], user_argv= , options= "-h --help")
    {'-h --help': True}
    >>> options_parser(argv=, user_argv= , options= "-h --help")
    {'-h --help': False}
    >>> options_parser(argv=, user_argv=['--help'], options= "-h --help")
    {'-h --help': True}
    """

    options_dic = check_option_lines(options)
    if argv is not None:
        output_dic = options_dic.copy()
        options_dic = check_option_contain_value(output_dic, options_dic, argv)
    return build_output_options_dictionary(user_argv, options_dic)


# Process options from docstring, treat lines that
# starts with '-' or '--' as options
def check_option_lines(options):
    """
    Args:
        options: options the options strings from docstring.

    Returns:
        options_dic: the updated options dictionary to caller function

    >>> check_option_lines(options= "-h --help")
    {'-h --help': False}
    >>> check_option_lines(options= "hello world")
    {}
    """

    options_dic = {}
    for line in options:
        tmp_array = line.split()

        if len(tmp_array) > 0 and tmp_array[0].strip()[:1] != '-':
            continue

        key = ""
        hasValue = False

        for count, element in enumerate(tmp_array, start=0):
            if element[:1] == '-':
                if len(tmp_array) > count + 1 and tmp_array[count + 1].isupper():
                    key += f"{element}=<{tmp_array[count + 1].lower()}> "
                    hasValue = True
                else:
                    key += element + ' '

        if hasValue:
            options_dic.update({key[:-1]: None})
        else:
            options_dic.update({key[:-1]: False})

        options_dic = find_default_value(line, key[:-1], options_dic)

    return options_dic


# A function for finding whether the current line of option has
# a default value that specify by the programmer
def find_default_value(line, old_key, options_dic):
    """
    Args:
        line: a string that holds the current line.
        old_key: a string that holds the current key for the options dictionary.
        options_dic: a dictionary that passed from main function,
                     needs to do updates on it from this function.
    Returns:
        options_dic: the updated options dic to the caller function

    >>> find_default_value(line='-o FILE --output=<value>  Speed in knots [default: ./test.txt].',
    >>> old_key="-o=<file> --output=<file>", options_dic={'-o=<file> --output=<file>': None})
    {'-o=<file> --output=<file>': './test.txt'}

    >>> find_default_value(line='--speed=<kn> -s KN  Speed in knots [default: 10].',
    >>> old_key="--speed=<kn> -s=<kn>", options_dic={'--speed=<kn> -s=<kn>': None})
    {'--speed=<kn> -s=<kn>': 10}

    >>> find_default_value(line='--aaa=<value>   Moored (anchored) mine [default: 20.9].',
    >>> old_key="--aaa=<value>", options_dic={'--aaa=<value>': None})
    {'--aaa=<value>': 20.9}

    >>> find_default_value(line='--aaa=<value>   Moored (anchored) mine.',
    >>> old_key="--aaa=<value>", options_dic={'--aaa=<value>': None})
    {'--aaa=<value>': None}
    """

    matching = re.search(r'\[.*?]', line)
    if matching is not None:
        default_value = matching.group(0)[1:-1].strip()

        # Test if this line of docstring contains a default value
        if re.search('default:', default_value, re.IGNORECASE):
            try:
                int(default_value.split()[1])
                tmp_dic = {old_key: int(default_value.split()[1])}
            except ValueError:
                try:
                    float(default_value.split()[1])
                    tmp_dic = {old_key: float(default_value.split()[1])}
                except ValueError:
                    tmp_dic = {old_key: default_value.split()[1]}
            options_dic.update(tmp_dic)
        return options_dic
    return options_dic


# Update the options dictionary with new value according to user arguments,
# remove the duplicated option keys after the new dictionary is built
def build_output_options_dictionary(user_argv, options_dic):
    """
    Args:
        user_argv: passed in arguments from user command line.
        options_dic: passed in the options dictionary from main function.
    Returns:
        output_dic: the new dictionary and set values according to the user command line.

    >>> before = {'-h --help --helping': False, '-o=<file> --output=<file>': 'ttt.pdf',
    >>>           '--speed=<kn>': 10}
    >>> build_output_options_dictionary(user_argv=[], options_dic=before)
    {'--helping': False, '--output': 'ttt.pdf', '--speed': 10}
    """

    output_dic = options_dic.copy()
    output_dic = check_option_contain_value(output_dic, options_dic, user_argv)
    for k in list(output_dic):
        if ' ' in k:
            put = sorted(k.split(), key=len, reverse=True)[0]
            if '=' in put:
                output_dic = {key if key != k else put.split('=')[0]: value for
                              key, value in output_dic.items()}
            else:
                output_dic = {key if key != k else put: value for key, value in
                              output_dic.items()}
        elif '=' in k:
            output_dic = {key if key != k else k.split('=')[0]: value for
                          key, value in output_dic.items()}
    return output_dic


# Matching the input options and separate them by whether
# the argument has a value (contains a equals sign)
def check_option_contain_value(output_dic, options_dic, arguments):
    """
    Args:
        output_dic: a copy of the options dictionary.
        options_dic: the original options dictionary from main function.
        arguments: a boolean to indicate whether needs to remove the duplicate keywords
                   in the dictionary.
    Returns:
        output_dic: the updated output_dic according to the user arguments.

    >>> options_dic1 = {'-h --help --helping': False, '-o=<file> --output=<file>': 'ttt.pdf'}
    >>> before = {'-h --help --helping': False, '-o=<file> --output=<file>': 'ttt.pdf'}
    >>> check_option_contain_value(output_dic=before, options_dic=options_dic1, arguments=['-h'])
    {'-h --help --helping': True, '-o=<file> --output=<file>': 'ttt.pdf'}
    """

    for tmp in arguments:
        element = str(tmp).strip()
        if element[:1] == "-" and '=' not in element:
            output_dic = check_key_without_equal(element, options_dic, output_dic)
        elif element[:1] == "-" and '=' in element:
            output_dic = check_key_contain_equal(element, options_dic, output_dic)
    return output_dic


# Helper function for check keys that not contains a value
def check_key_without_equal(element, options_dic, output_dic):
    """
     Args:
        element: one of the arguments that pass in by the user command line.
        options_dic: indicates whether the program  needs to remove
                     duplicate keyword for options dictionary.
        output_dic: a copy of the options dic.
    Returns:
        output_dic: a updated value dictionary according the arguments
                    in the user command line

    >>> options_dic1 = {'-h --help --helping': False, '--moored': False}
    >>> before = {'-h --help --helping': False, '--moored': False}
    >>> check_key_without_equal(element='--help', options_dic=options_dic1, output_dic=before)
    {'-h --help --helping': True, '--moored': False}
    >>> before = {'-h --help --helping': False, '--moored': False}
    >>> check_key_without_equal(element='--moored', options_dic=options_dic1, output_dic=before)
    {'-h --help --helping': False, '--moored': True}
    """

    for k in options_dic:
        if element in k:
            tmp_dic = {k: True}
            output_dic.update(tmp_dic)
    return output_dic


# Helper function for check keys that contains a value
def check_key_contain_equal(element, options_dic, output_dic):
    """
    Args:
        element: one of the argument that pass in by the user command line.
        options_dic: the original options dictionary from main function.
        output_dic: a copy of the options dic.
    Returns:
        output_dic: a updated value dictionary according the arguments
                    in the user command line

    >>> options_dic1 = {'--speed=<kn>': 0, '-o=<file> --output=<file>': 'default.txt'}
    >>> before = {'--speed=<kn>': 0, '-o=<file> --output=<file>': 'default.txt'}
    >>> check_key_contain_equal(element="--speed=10.7", options_dic=options_dic1,
    >>>                                    output_dic=before)
    {'--speed=<kn>': 10.7, '-o=<file> --output=<file>': 'default.txt'}
    >>> before = {'--speed=<kn>': 0, '-o=<file> --output=<file>': 'default.txt'}
    >>> check_key_contain_equal(element="-o=haha.pdf", options_dic=options_dic,
    >>>                                     output_dic=before)
    {'--speed=<kn>': 0, '-o=<file> --output=<file>': 'haha.pdf'}
    """

    for k in options_dic:
        if '=' in k:
            for tmp in k.split(' '):
                if element.split('=')[0] == tmp.split('=')[0]:
                    try:
                        int(element.split('=')[1])
                        tmp_dic = {k: int(element.split('=')[1])}
                    except ValueError:
                        try:
                            float(element.split('=')[1])
                            tmp_dic = {k: float(element.split('=')[1])}
                        except ValueError:
                            tmp_dic = {k: element.split('=')[1]}
                    output_dic.update(tmp_dic)
    return output_dic
