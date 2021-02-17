"""
  docopt is for displaying the usages and options table that written by the programmer
  to the users. this program allows....
"""
import warnings
import sys
import re
import math


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

    # def __getitem__(self, item):
    #    pass

    def __init__(self, text, left, right, ty):
        self.txt = text
        self.left = left
        self.right = right
        self.type = ty
        self.is_req = True

    # def __str__(self):
    #    return self.txt

    # def __repr__(self):
    #    return self.txt


#########################################################################
##########################################################################
# Main function for docopt program
def docopt(doc, argv=None, help_message=True, version=None):
    """
    :param doc: docstring that pass from the user program
    :param argv: programmer can pre-pass some parameters into docopt and
       those parameters is treat as default existing arguments
    :param help_message: user can specify whether they want docopt to display
       the help message whenever user execute the program
    :param version: programmers can specify the version of
       the project and display to user
    :return: returns the complete dictionary from parameters passed in
    """

    usages, options = processing_string(doc, help_message, version)
    options_dic = options_parser(argv, sys.argv, options)
    usage_dic = usage_parser(usages, argv, sys.argv[1:])
    total_dic, output_string = print_output_dictionary(usage_dic, options_dic)
    print(output_string)
    return total_dic


#####################################################################
######################################################################
# Main Controller for processing the docstring.
def processing_string(doc, help_message, version):
    """
    :param doc: docstring pass from the main function
    :param help_message: to tell docopt whether user want to
        display help message when the program executes
    :param version: the version string pass from main function
    :return: returns the array of usage patterns and the array of options from docstring
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
    :param doc: docstring that passed from main function
    :return: returns the strings of name of program, usage patterns,
        and options that received from docstring
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


# Function for testing whether the docstring contains
# a usage part and a options part.
# Will display warning to the user program when missing parts
def check_warnings(usage, options):
    """
    :param usage: a string the retrieve from the docstring
    :param options: a string that retrieve from the docstring
    :return: returns 1 if no usage pattern found, returns 2 if no options found,
        and returns 0 if everything is ok in docstring
    """

    if len(usage) == 0:
        warnings.warn('No usage indicated from docstring')
        return 1
    if len(options) == 0:
        warnings.warn('No options indicated from docstring')
        return 2
    return 0


# This function will be involved when user program specify help=True.
def show_help(name, version, usage, options):
    """
    :param name: name passed from the main function that retrieve
        from the docstring
    :param version: version information that retrieve from the docstring
    :param usage: usage string that retrieve from the docstring
    :param options: options string that retrieve from the docstring
    :return: returns the help message to caller function
    """

    output = ""
    if len(name) > 0:
        output += name + "\n\n"
    if version is not None:
        output += "Version:\n  " + version + "\n\n"
    output += usage + "\n\n"
    output += options + "\n\n"
    return output


####################################################################
###################################################################
# Main function for checking usage
# After execution, Usage_dic is populated with appropriate values if successful
def usage_parser(usages, argv, user_argv):
    """Matches user input with usage patterns and returns populated usage_dic."""
    arguments = user_argv
    if argv is not None:
        arguments = argv
    patterns, usage_dic = parse_usage(usages)
    pattern_to_use = find_matching_pattern(patterns, arguments)
    populate_usage_dic(pattern_to_use, patterns, arguments, usage_dic)
    return usage_dic


# Split token by '|' into two mutually exclusive Token objects
# @param token is a Token object of the form "token1|token2"
# Returns a list object with the split tokens, i.e. ["token1", "token2"]
def split_token(token):
    """Splits Token by '|' and returns list of separated Tokens."""
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


# Extract raw tokens from pattern and convert them to Token objects
# @param pattern is a string containing a single usage pattern
# @param name the name of the program - used to ignore the program name when creating the tokens
# Returns a linked list of Token objects
def convert_tokens(pattern, name):
    """Extracts raw pattern tokens and returns linked list of converted Tokens."""
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


# @param tokens is the list of Token objects for a given pattern
# Simply modifies the existing tokens, no return value
def parse_args(tokens):
    """Sets type attribute for all argument tokens to Argument."""
    for token in tokens:
        if token.txt.startswith('<') is True and token.txt.endswith('>') is True:
            token.type = "Argument"
        else:
            if token.txt.isupper():
                token.type = "Argument"


# @param tokens is the list of Token objects for a given pattern
# Simply modifies the existing tokens, no return value
def parse_options(tokens):
    """Sets type attribute for all option tokens to Option."""
    for token in tokens:
        if token.txt.startswith('-') is True:
            token.type = "Option"


# @param tokens is the list of Token objects for a given pattern
# Simply modifies the existing tokens, no return value
def parse_commands(tokens):
    """Sets type attribute for all command tokens to Command."""
    for token in tokens:
        # Ignore lone '|' tokens
        if token.txt != '|':
            # If token isn't an argument or an option, it must be a command
            if token.type != "Argument" and token.type != "Option":
                token.type = "Command"


# Handle mutex tokens
# Ex: "[--moored | --drifting]" gets replaced with [[--moored, --drifting]]
# @param token_objects the list of Token objects for a given pattern
# No return value
def parse_mutex(token_objects):
    """Replace tokens with mutex elements with a single list of mutex tokens."""
    for index, token in enumerate(token_objects):
        if token.txt == '|':
            token_objects[index - 1] = [token.left, token.right]
            token_objects.remove(token.right)
            token_objects.remove(token)
        elif '|' in token.txt:
            token_objects[index] = split_token(token)


# Populate Usage_dic with default argument and command values
# @param token_objects the finalized list of Token objects for a given pattern
def build_usage_dic(token_objects):
    """Uses finalized list of Token objects to return a default-value populated usage_dic."""
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


# Process optional ( [] ) and required ( () ) elements
# @param tokens a list of Token objects for a given pattern
# @param open_c the open character used to denote whether to process () or []
# Labels each token as required or optional under the is_req parameter
# No return value
def process_paren(tokens, open_c):
    """Process and label tokens as optional or required using [] and ()."""
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


# Examine each usage pattern and label each token appropriately
# (argument, option, or command; optional or required)
# Builds Usage_dic using these Token objects
# Fills Patterns global object with finalized lists of tokens
def parse_usage(usages):
    """Processes usages string to return default usage_dic and list of tokens for each pattern."""
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


# Check if input token matches one (and only one) of the mutually exclusive tokens
# @param index the index of which token we are examining, used to retrieve input token in Arguments
# @param token the token we are examining
# Returns true if a conflict is found, false otherwise
def check_mutex(index, token, arguments):
    """Checks if input matches only one of the mutex tokens, returns false if no conflict."""
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


# Check individual arg, command, and optional tokens for a match with corresponding input token
# @param index the index of which token we are examining, used to retrieve input token in Arguments
# @param token the token we are examining
# Returns true if a conflict is found, false otherwise
def check_tokens(index, token, arguments):
    """Check individual tokens for a match with corresponding input token."""
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


# Compare input tokens with a Usage pattern p
# @param p the usage pattern we are checking, a list of Token objects
# Returns True if a conflict is found, False otherwise
def find_conflict(pat, arguments):
    """Compare user args with a usage pattern p, return false if no conflict."""
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


# Finds which Usage pattern matches the input
# Returns index of first match found
# If no match found, function returns None
def find_matching_pattern(patterns, arguments):
    """Finds which usage pattern matches user args and returns index of that pattern."""
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


# Fill Usage_dic with appropriate values from the input
# @param pattern_to_use an integer denoting which Usage pattern matches the input
# No return value
def populate_usage_dic(pattern_to_use, patterns, arguments, usage_dic):
    """Fill usage_dic with appropriate input values if pattern match found."""
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


####################################################################
###################################################################
# Main function for checking options
def options_parser(argv, user_argv, options):
    """
    :param argv: the default arguments that specify by the programmer
    :param user_argv: the arguments passed from user command line
    :param options: the options strings from docstring
    :return: returns the built options dictionary from another method
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
    :param options: options the options strings from docstring
    :return: returns the updated options dictionary to caller function
    """

    options_dic = {}
    for line in options:
        tmp_array = line.split()
        # Skip the line that is not starts with '-' or '--'
        if len(tmp_array) > 0 and tmp_array[0].strip()[:1] != '-':
            continue

        found = False
        old_key = None
        for count, _ in enumerate(tmp_array, start=0):
            if tmp_array[count][:1] == '-':
                if not found:
                    old_key, tmp_dic = check_first_option(tmp_array, count)
                    options_dic.update(tmp_dic)
                else:
                    old_key, new_key = check_other_option(tmp_array, count, old_key)
                    # This line is for updating the key in the option dictionary
                    options_dic = {key if key != old_key else new_key: value for key, value in
                                   options_dic.items()}
                    old_key = new_key
                found = True
        options_dic = find_default_value(line, old_key, options_dic)
    return options_dic


# A function for finding whether the current line of option has
# a default value that specify by the programmer
def find_default_value(line, old_key, options_dic):
    """
    :param line: a string that holds the current line
    :param old_key: a string that holds the current key for the options dictionary
    :param options_dic: a dictionary that passed from main function,
        needs to do updates on it from this function
    :return: the updated options dic to the caller function
    """

    m = re.search(r"\[([A-Za-z0-9_]+)/]", line)
    print(m)
    if m is not None:
        default_value = m.group(1)
        print(default_value)
    # if len(default_value) > 0:
    #     default_value.strip()
    #
    #     # Test if this line of docstring contains a default value
    #     if re.search('default:', default_value, re.IGNORECASE):
    #         try:
    #             int(default_value.split()[1])
    #             tmp_dic = {old_key: int(default_value.split()[1])}
    #         except ValueError:
    #             try:
    #                 float(default_value.split()[1])
    #                 tmp_dic = {old_key: float(default_value.split()[1])}
    #             except ValueError:
    #                 tmp_dic = {old_key: default_value.split()[1]}
    #         options_dic.update(tmp_dic)
    #     return options_dic
    return options_dic


# Insert the option into dictionary with no same option command
# exist in the dictionary ('--sorted')
def check_first_option(tmp_array, count):
    """
    :param tmp_array: the current checking line from options in the docstring
    :param count: specify the location of array for the string
        that is split by space
    :return: returns the current new key for the dictionary for the current line
        and the old_key from matching the stored pattern in the dictionary for updating
    """

    if '=' in tmp_array[count]:
        old_key = tmp_array[count]
        tmp_dic = {old_key: None}
    elif len(tmp_array) > count + 1 and tmp_array[count + 1].isupper():
        # The option with Value (either in -s FILE or -p=<file>)
        # will always change to -p=<file>
        # when insert into the dictionary
        old_key = f"{tmp_array[count]}=<{tmp_array[count + 1].lower()}>"
        tmp_dic = {old_key: None}
    else:
        old_key = tmp_array[count]
        tmp_dic = {old_key: False}

    return old_key, tmp_dic


# Insert the option into dictionary with same option command
# already exist in the dictionary
# e.g. insert '--help' when '-h' is exists already
def check_other_option(tmp_array, count, old_key):
    """
    :param tmp_array: the current checking line from options in the docstring
    :param count: specify the location of array for the string that
        is split by space
    :param old_key: specify the current key for updating the key in options dictionary
    :return: the current new key for the dictionary for the current line
        and the old_key from matching the stored pattern in the dictionary for updating
    """

    if len(tmp_array) > count + 1 and tmp_array[count + 1].isupper():
        # The option with Value (either in -s FILE or -p=<file>)
        # will always change to -p=<file>
        # when insert into the dictionary
        new_key = old_key + " " + f"{tmp_array[count]}=" \
                                  f"<{tmp_array[count + 1].lower()}>"
    else:
        new_key = old_key + " " + tmp_array[count]

    return old_key, new_key


# Update the options dictionary with new value according to user arguments,
# remove the duplicated option keys after the new dictionary is built
def build_output_options_dictionary(user_argv, options_dic):
    """
    :param user_argv: passed in arguments from user command line
    :param options_dic: passed in the options dictionary from main function
    :return: the new dictionary and set values according
        to the user command line
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
    :param output_dic: a copy of the options dictionary
    :param options_dic: the original options dictionary from main function
    :param arguments: a boolean to indicate whether needs to remove the duplicate keywords
        in the dictionary
    :return: returns the updated output_dic according to the user arguments
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
    :param element: one of the arguments that pass in by the user command line
    :param options_dic: indicates whether the program  needs to remove
        duplicate keyword for options dictionary
    :param output_dic: a copy of the options dic
    :return: returns a updated value dictionary according the arguments
        in the user command line
    """

    for k in options_dic:
        if element in k:
            tmp_dic = {k: True}
            output_dic.update(tmp_dic)
    return output_dic


# Helper function for check keys that contains a value
def check_key_contain_equal(element, options_dic, output_dic):
    """
    :param element: one of the argument that pass in by the user command line
    :param options_dic: the original options dictionary from main function
    :param output_dic: a copy of the options dic
    :return: a updated value dictionary according the arguments
        in the user command line
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


####################################################################
###################################################################
# Main function for building output strings to user
def print_output_dictionary(usage_dic, options_dic):
    """
    :param usage_dic: the original usage dictionary from main function
    :param options_dic: the original options dictionary from main function
    :return: returns the output string or testing array to caller function
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
    :param rows: count for how many rows needed for output dictionary
    :param length: the total length for the output usage and options dictionary
    :param dic_list: reformat the dictionary into a array
    :param dictionary_total: combined dictionary (usage dic + options dic)
    :return: returns the string from display or an array for testing
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
    :param dic_list:  a dictionary the built from user argument but reform to a list
    :param idx: the current row index
    :param rows: count of the rows
    :param col_idx: index of the col
    :param dictionary_total: the dictionary that includes both keywords for output patterns
        and options
    :return: returns the key value pair in a outputting
        form according to the type of values
    """

    if check_value_type(dictionary_total[dic_list[idx + (col_idx * rows)]]):
        return '\'{}\': {}'.format(dic_list[idx + (col_idx * rows)],
                                   dictionary_total[dic_list[idx + (col_idx * rows)]])

    return '\'{}\': \'{}\''.format(dic_list[idx + (col_idx * rows)],
                                   dictionary_total[dic_list[idx + (col_idx * rows)]])


# Helper method for defining whether the value is a string or a primitive type
def check_value_type(value):
    """
    :param value: the value for current key in the dictionary
    :return:  returns a boolean value whether the value passed in is primitive
    """

    return isinstance(value, (int, float, bool)) or value is None


# Helper method for printing out dictionary as a json string to user
def print_output_from_rows(col1, col2, col3, rows):
    """
    :param col1: holds the values for output column one
    :param col2: holds the values for output column two
    :param col3: holds the values for output column three
    :param rows: counter for number of rows
    :return: returns output string
    """

    spaces1 = len(max(col1, key=len))
    spaces2 = len(max(col2, key=len))
    final_output = ""
    for k in range(rows):
        if k == 0:
            out = '{' + col1[k].strip().ljust(spaces1) + ' ' * 4 \
                  + col2[k].strip().ljust(spaces2) + ' ' * 4 \
                  + col3[k].strip().ljust(spaces2)
        else:
            out = col1[k].ljust(spaces1) + ' ' * 4 \
                  + col2[k].ljust(spaces2) + ' ' * 4 \
                  + col3[k].ljust(spaces2)
        if k == rows - 1:
            final_output += (out.rstrip() + '}\n')
        else:
            final_output += (out.rstrip() + '\n')
    return final_output
