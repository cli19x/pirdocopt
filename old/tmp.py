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
    new_pat = []
    for line in options:
        tmp_array = line.split()
        if len(tmp_array) > 0 and tmp_array[0].strip()[:1] != '-':
            continue
        key = ""
        token = None
        for count, element in enumerate(tmp_array, start=0):

            if element[:2] == '--':
                token = check_option_lines_long(element, tmp_array, count, token)

            elif element[:1] == '-':
                token = check_option_lines_short(element, tmp_array, count, token)
        token = find_default_value(line, token)
        new_pat.append(token)
    return new_pat


def check_option_lines_long(element, tmp_array, count, token):
    if len(tmp_array) > count + 1 and tmp_array[count + 1].isupper():
        if token is None:
            token = Option(element, tmp_array[count + 1].lower(),
                           has_value=True, short=None, long=element)
        else:
            token.long = element
    elif '=' in element:
        if token is None:
            arg = re.search('<\\S+>', element).group()
            text = re.search('\\S+=', element).group().strip("=")
            token = Option(text, arg,
                           has_value=True, short=None, long=text)
        else:
            token.long = re.search('\\S+=', element).group().strip("=")
    return token


def check_option_lines_short(element, tmp_array, count, token):
    if len(tmp_array) > count + 1 and tmp_array[count + 1].isupper():
        if token is None:
            token = Option(element, tmp_array[count + 1].lower(),
                           has_value=True, short=element, long=None)
        else:
            token.short = element
    elif '=' in element:
        if token is None:
            arg = re.search('<\\S+>', element).group()
            text = re.search('\\S+=', element).group().strip("=")
            token = Option(text, arg,
                           has_value=True, short=text, long=None)
        else:
            token.short = re.search('\\S+=', element).group().strip("=")
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
                token.value = int(default_value.split()[1])
            except ValueError:
                try:
                    float(default_value.split()[1])
                    token.value = float(default_value.split()[1])
                except ValueError:
                    token.value = default_value.split()[1]
    return token
