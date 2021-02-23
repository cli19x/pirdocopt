"""
  This module is for the helper functions of docopt.py.
  Contains the function for processing docstrings and
  formatting the print strings to user
"""
import warnings
import math


# Main Controller for processing the docstring.
def processing_string(doc, help_message, version):
    """
     Args:
        doc: docstring pass from the main function.
        help_message: to tell docopt whether user want to display help message when
                      the program executes.
        version: the version string pass from main function.
        version: programmers can specify the version of the project and display to user.
    Returns:
        usage.split("\n"): returns the array of usage patterns.
        options.split("\n"): returns the array of options from docstring.

    >>> doc1 = 'Perfect' \
    >>>
    >>>        'Usage:' \
    >>>          'naval_fate.py ship new <name>...' \
    >>>
    >>>        'Options:' \
    >>>           '-h --help --helping Show this screen.' \
    >>>           '--sorted  Show sorted.'
    >>>
    >>> processing_string(doc=doc1, help_message=False, version="test 2.0")
    ['Usage:', '  naval_fate.py ship new <name>...'], \
    ['Options:', '  -h --help --helping Show this screen.', '  --sorted  Show sorted.']
    """

    if doc is None:
        warnings.warn('No docstring found')
        return None
    name, usage, options = get_usage_and_options(doc)
    check_warnings(usage, options)
    if help_message:
        print(show_help(name, version, usage, options))
    return usage.split("\n"), options.split("\n")


# Helper function for getting usage, options and name strings from doc
def get_usage_and_options(doc):
    """
     Args:
        doc: docstring that passed from main function.
    Returns:
        name: returns the strings of name of program.
        usage: returns the strings of usage patterns.
        options: returns the strings of options that received from docstring

    >>> doc1 = 'Perfect' \
    >>>
    >>>        'Usage:' \
    >>>          'naval_fate.py ship new <name>...' \
    >>>
    >>>        'Options:' \
    >>>           '-h --help --helping Show this screen.' \
    >>>           '--sorted  Show sorted.'
    >>>
    >>> get_usage_and_options(doc1)
    "Perfect",
    "Usage: \
    naval_fate.py ship new <name>...", \
    "Options: \
    -h --help --helping Show this screen. \
    --sorted  Show sorted."
    """

    usage = ""
    options = ""
    partition_string = doc.strip().split('\n\n')
    name = partition_string[0]
    if "Usage:" in name:
        usage = name.strip()
        name = ""
    for line in partition_string:
        if "Usage:" in line:
            usage = line.strip()
        if "Options:" in line:
            options = line.strip()

    if len(options) == 0 and len(name) == 0:
        for i in range(1, len(partition_string)):
            if len(partition_string[i]) > 0:
                options = partition_string[i].strip()
    elif len(options) == 0 and len(name) != 0:
        for i in range(2, len(partition_string)):
            if len(partition_string[i]) > 0:
                options = partition_string[i].strip()
    return name, usage, options


# Will display warning to the user program when missing parts
def check_warnings(usage, options):
    """ Function for testing whether the docstring contains a usage part and a options part.
     Args:
        usage: a string the retrieve from the docstring.
        options: a string that retrieve from the docstring.
    Returns:
        returns 1 if no usage pattern found, returns 2 if no options found,
        and returns 0 if everything is ok in docstring
    Raises:
        Warnings: If no usages or options contained in the docstring.

    >>> check_warnings(usage="Usages: ...", options="")
    0
    >>> check_warnings(usage="", options="Options: ...")
    1
    >>> check_warnings(usage="Usages: ...", options="")
    2
    """

    if len(usage) == 0:
        warnings.warn('No usage indicated from docstring')
        return 1
    if len(options) == 0:
        warnings.warn('No options indicated from docstring')
        return 2
    return 0


#
def show_help(name, version, usage, options):
    """ This function will be involved when user program specify help=True.
    Args:
        name: name passed from the main function that retrieve
              from the docstring.
        version: version information that retrieve from the docstring.
        usage: usage string that retrieve from the docstring.
        options: options string that retrieve from the docstring.
    Returns:
        output: returns the help message to caller function

    >>> show_help('Perfect', 'test 2.0', 'Usage: ...', 'Options: ...')
    Perfect

    Version:
      test 2.0

    Usage: ...

    Options: ...

    """

    output = ""
    if len(name) > 0:
        output += name + "\n\n"
    if version is not None:
        output += "Version:\n  " + version + "\n\n"
    output += usage + "\n\n"
    output += options + "\n\n"
    return output


# Main function for building output strings to user
def print_output_dictionary(usage_dic, options_dic):
    """
    Args:
        usage_dic: the original usage dictionary from main function.
        options_dic: the original options dictionary from main function.
    Returns:
        dictionary_total: the final dictionary object that built from usage pattern and options.
        return the formatted json like dictionary string to user.

    >>> input1 = {'1': True, '2': 'haha', '3': False, '4': True, '5': 'haha'}
    >>> u_dic = {'usage1': 'x', 'usage2': 'y'}
    >>> dic_total, res = print_output_dictionary(usage_dic=u_dic, options_dic=input1)
    >>> assert dic_total == {**usage_dic, **dic_total}
    {'usage1': 'x'
     'usage2': 'y'
     '1': True
     '2': 'haha'
     '3': False
     '4': True
     '5': 'haha'
    }
    """

    dictionary_total = {}
    dictionary_total.update(usage_dic)
    dictionary_total.update(options_dic)
    dic_list = list(dictionary_total)
    length = len(dictionary_total)
    if length > 24:
        rows = math.ceil(length / 3)
    else:
        rows = 8
    return dictionary_total, output_formatter(rows, length, dic_list, dictionary_total)


# A helper function for display a nice looking dictionary to the user
def output_formatter(rows, length, dic_list, dictionary_total):
    """
    Args:
        rows: count for how many rows needed for output dictionary.
        length: the total length for the output usage and options dictionary.
        dic_list: reformat the dictionary into a array.
        dictionary_total: combined dictionary (usage dic + options dic).
    Returns:
        returns the string from display or an array for testing.

    >>> dic = {'--helping': True, '--sorted': True, '--output': 'ttt.pdf', '--version': False,
    >>>        '--speed': 10, '--moored': True, '--drifting': None, '--rr': False, '--aaa': 20.9,
    >>>        '--yyy': False}
    >>> d_list = list(dic)
    >>> output_formatter(rows=4, length=len(dic_list), dic_list=dic_list, dictionary_total=dic)
    "{'--helping': True         '--speed': 10          '--aaa': 20.9\n" + \
    " '--sorted': True          '--moored': True       '--yyy': False\n" + \
    " '--output': 'ttt.pdf'     '--drifting': None\n" + \
    " '--version': False        '--rr': False}\n"
    """

    col1 = [' '] * rows
    col2 = [' '] * rows
    col3 = [' '] * rows
    for i in range(0, rows):
        if length > i:
            col1[i] += insert_content(dic_list, i, rows, 0, dictionary_total)
        if length > i + rows:
            col2[i] += insert_content(dic_list, i, rows, 1, dictionary_total)
        if length > i + (2 * rows):
            col3[i] += insert_content(dic_list, i, rows, 2, dictionary_total)

    return print_output_from_rows(col1, col2, col3, rows)


# Helper function for inserting the key value pairs into output dictionary
def insert_content(dic_list, idx, rows, col_idx, dictionary_total):
    """
    Args:
        dic_list:  a dictionary the built from user argument but reform to a list.
        idx: the current row index.
        rows: count of the rows.
        col_idx: index of the col,
        dictionary_total: the dictionary that includes both keywords for output patterns
                          and options.
    Returns:
        returns the key value pair in a outputting form according to the type of values.

    >>> dic = {'--helping': True, '--sorted': None, '--output': 'ttt.pdf',
    >>>        '--speed': 10, '--aaa': 20.9}
    >>> d_list = list(dic)

    >>> insert_content(dic_list=dic_list, idx=0, rows=0, col_idx=0, dictionary_total=dic)
    '--helping: True'
    >>> insert_content(dic_list=dic_list, idx=1, rows=0, col_idx=0, dictionary_total=dic)
    '--sorted: None'
    >>> insert_content(dic_list=dic_list, idx=2, rows=0, col_idx=0, dictionary_total=dic)
    '--output: ttt.pdf'
    >>> insert_content(dic_list=dic_list, idx=3, rows=0, col_idx=0, dictionary_total=dic)
    '--speed: 10'
    >>> insert_content(dic_list=dic_list, idx=4, rows=0, col_idx=0, dictionary_total=dic)
    '--aaa: 20.9'
    """

    if check_value_type(dictionary_total[dic_list[idx + (col_idx * rows)]]):
        return '\'{}\': {}'.format(dic_list[idx + (col_idx * rows)],
                                   dictionary_total[dic_list[idx + (col_idx * rows)]])

    return '\'{}\': \'{}\''.format(dic_list[idx + (col_idx * rows)],
                                   dictionary_total[dic_list[idx + (col_idx * rows)]])


# Helper method for defining whether the value is a string or a primitive type
def check_value_type(value):
    """
    Args:
        value: the value for current key in the dictionary.
    Returns:
        returns a boolean value whether the value passed in is primitive.

     >>> check_value_type('Perfect')
    False
    >>> check_value_type(10)
    True
    >>> check_value_type(3.1415)
    True
    >>> check_value_type(True)
    True
    >>> check_value_type(None)
    True
    """

    return isinstance(value, (int, float, bool)) or value is None


# Helper method for printing out dictionary as a json string to user
def print_output_from_rows(col1, col2, col3, num_rows):
    """
    Args:
        col1: holds the values for output column one.
        col2: holds the values for output column two.
        col3: holds the values for output column three.
        num_rows: the number of rows
    Returns:
        final_output: returns output string

    >>> first_row = [' 11', ' 2', ' 3', ' 4', ' 5']
    >>> second_row = [' 1', ' 222', ' 3', ' 4', ' ']
    >>> third_row = [' 1', ' 2', ' 3333', ' ', ' ']
    >>> print_output_from_rows(col1=col1, col2=col2, col3=col3, num_rows=5)
    "{11     1       1\n" + \
    " 2      222     2\n" + \
    " 3      3       3333\n" + \
    " 4      4\n" + \
    " 5}\n"
    """

    spaces1 = len(max(col1, key=len))
    spaces2 = len(max(col2, key=len))
    final_output = ""
    for k in range(num_rows):
        if k == 0:
            out = '{' + col1[k].strip().ljust(spaces1) + ' ' * 4 \
                  + col2[k].strip().ljust(spaces2) + ' ' * 4 \
                  + col3[k].strip().ljust(spaces2)
        else:
            out = col1[k].ljust(spaces1) + ' ' * 4 \
                  + col2[k].ljust(spaces2) + ' ' * 4 \
                  + col3[k].ljust(spaces2)
        if k == num_rows - 1:
            final_output += (out.rstrip() + '}\n')
        else:
            final_output += (out.rstrip() + '\n')
    return final_output
