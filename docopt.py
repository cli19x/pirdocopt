"""
  docopt is for the ...
"""
import warnings
import sys
import re
import math

TEST = False


#########################################################################
##########################################################################
# Main function for docopt.
# @param doc docstring that pass from the user program
# @param argv programmer can pre-pass some parameters into docopt and
#       those parameters is treat as default existing arguments
# @param help_message user can specify whether they want docopt to display
#       the help message whenever user execute the program
# @param version programmers can specify the version of
# the project and display to user
def docopt(doc, argv=None, help_message=True, version=None):
    usages, options = processing_string(doc, help_message, version)
    options_dic = options_parser(argv, sys.argv, options)
    usage_dic = []
    return print_output_dictionary(usage_dic, options_dic)


#####################################################################
######################################################################
# Main Controller for processing the docstring.
# @param doc docstring pass from the main function
# @param help_message to tell docopt whether user want to
# display help message when the program executes
# @param version The version string pass from main function
def processing_string(doc, help_message, version):
    if doc is None:
        warnings.warn('No docstring found')
        return
    name, usage, options = get_usage_and_options(doc)
    check_warnings(usage, options)
    if help_message:
        print(show_help(name, version, usage, options))
    return usage.split("\n"), options.split("\n")


# Helper function for getting usage, options and name strings from doc
def get_usage_and_options(doc):
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
# @param usage a string the retrieve from the docstring
# @param options a string that retrieve from the docstring
def check_warnings(usage, options):
    if len(usage) == 0:
        warnings.warn('No usage indicated from docstring')
        return 1
    if len(options) == 0:
        warnings.warn('No options indicated from docstring')
        return 2
    return 0


# This function will be involved when user program specify help=True.
# @param name name passed from the main function that retrieve
# from the docstring
# @param version version information that retrieve from the docstring
# @param usage usage string that retrieve from the docstring
# @param options options string that retrieve from the docstring
def show_help(name, version, usage, options):
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
# Main function for checking options
def options_parser(argv, user_argv, options):
    options_dic = check_option_lines(options)
    if argv is not None:
        output_dic = options_dic.copy()
        options_dic = check_option_contain_value(output_dic, options_dic, argv, False)
    return build_output_options_dictionary(user_argv, options_dic)


# Process options from docstring, treat lines that
# starts with '-' or '--' as options
def check_option_lines(options):
    options_dic = {}
    for line in options:
        tmp_array = line.split()
        # Skip the line that is not starts with '-' or '--'
        if len(tmp_array) > 0 and tmp_array[0].strip()[:1] != '-':
            continue

        found = False
        old_key = None
        for count in range(len(tmp_array)):
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
# @param line a string that holds the current line
# @param old_key a string that holds the current key for the options dictionary
def find_default_value(line, old_key, options_dic):
    default_value = line[line.find("[") + 1:line.find("]")]
    if default_value is not None:
        default_value.strip()

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


# Insert the option into dictionary with no same option command
# exist in the dictionary ('--sorted')
# @param tmp_array the current checking line from options in the docstring
# @param count specify the location of array for the string
# that is split by space
# @return return the current new key for the dictionary for the current line
def check_first_option(tmp_array, count):
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
# @param tmp_array the current checking line from options in the docstring
# @param count specify the location of array for the string that
# is split by space
# @param old_key specify the current key for updating the key
# in options dictionary
# @return return the current new key for the dictionary for the current line
def check_other_option(tmp_array, count, old_key):
    if '=' in tmp_array[count]:
        new_key = old_key + " " + tmp_array[count]
    elif len(tmp_array) > count + 1 and tmp_array[count + 1].isupper():
        # The option with Value (either in -s FILE or -p=<file>)
        # will always change to -p=<file>
        # when insert into the dictionary
        new_key = old_key + " " + f"{tmp_array[count]}=" \
                                  f"<{tmp_array[count + 1].lower()}>"
    else:
        new_key = old_key + " " + tmp_array[count]

    return old_key, new_key


# Update the options dictionary with new value according to user arguments,
# remove the duplicated option keys
# after the new dictionary is built
# @return return the new dictionary and set values according
# to the user command line
def build_output_options_dictionary(user_argv, options_dic):
    output_dic = options_dic.copy()
    output_dic = check_option_contain_value(output_dic, options_dic, user_argv, True)
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
# @param output_dic a copy of the options dic
# @return return the updated output_dic according to the user arguments
def check_option_contain_value(output_dic, options_dic, arguments, remove_duplicate):
    for e in arguments:
        ne = e.strip()
        if ne[:1] == "-" and '=' not in ne:
            output_dic = check_keys(ne, False, output_dic, options_dic, remove_duplicate)
        elif ne[:1] == "-" and '=' in ne:
            output_dic = check_keys(ne, True, output_dic, options_dic, remove_duplicate)
        else:
            continue
    return output_dic


# Helper function for matching the input options from user
# and the option dictionary
# Always output the most detail keyword for option command
# when there exists choices
# @param element one of the argument that pass in by the user command line
# @param is_contain_equal a boolean for whether the argument
# from command line contains a value
# @param output_dic a copy of the options dic
# @param remove_duplicate indicate whether the dictionary needs to remove
# duplicate keyword for options
# @return returns a updated value dictionary according the arguments
# in the user command line
def check_keys(element, is_contain_equal, output_dic, options_dic, remove_duplicate):
    if not is_contain_equal:
        output_dic = check_key_without_equal(element, remove_duplicate, options_dic,
                                             output_dic)
    else:
        output_dic = check_key_contain_equal(element, remove_duplicate, options_dic,
                                             output_dic)
    return output_dic


# Helper function for check keys that not contains a value
# @param element one of the argument that pass in by the user command line
# @param output_dic a copy of the options dic
# @param remove_duplicate indicate whether the dictionary needs to remove
# duplicate keyword for options
# @return returns a updated value dictionary according the arguments
# in the user command line
def check_key_without_equal(element, remove_duplicate, options_dic, output_dic):
    for k in options_dic:
        put = sorted(k.split(), key=len, reverse=True)
        if element in put:
            if remove_duplicate:
                output_dic = {key if key != k else put[0]: value for
                              key, value in output_dic.items()}
                tmp_dic = {put[0]: True}
            else:
                tmp_dic = {k: True}
            output_dic.update(tmp_dic)
    return output_dic


# Helper function for check keys that contains a value
# @param element one of the argument that pass in by the user command line
# @param output_dic a copy of the options dic
# @param remove_duplicate indicate whether the dictionary needs to remove
# duplicate keyword for options
# @return returns a updated value dictionary according the arguments
# in the user command line
def check_key_contain_equal(element, remove_duplicate, options_dic, output_dic):
    for k in options_dic:
        if '=' in k:
            put = sorted(k.split(), key=len, reverse=True)
            for tmp in put:
                if element.split('=')[0] == tmp.split('=')[0]:
                    if remove_duplicate:
                        output_dic = {
                            key if key != k else put[0].split('=')[0]: value
                            for key, value in
                            output_dic.items()}
                        tmp_dic = {
                            put[0].split('=')[0]: element.split('=')[1]}
                    else:
                        tmp_dic = {k: element.split('=')[1]}
                    output_dic.update(tmp_dic)
    return output_dic


####################################################################
###################################################################
# Main function for building output strings to user
# {'--drifting': False,    'mine': False,
#  '--help': False,        'move': True,
#  '--moored': False,      'new': False,
#  '--speed': '15',        'remove': False,
#  '--version': False,     'set': False,
#  '<name>': ['Guardian'], 'ship': True,
#  '<x>': '100',           'shoot': False,
#  '<y>': '150'}
#  print('We are the {} who say "{}!"'.format('knights', 'Ni'))
def print_output_dictionary(usage_dic, options_dic):
    dictionary_total = {}
    dictionary_total.update(usage_dic)
    dictionary_total.update(options_dic)
    dic_list = list(dictionary_total)
    length = len(dictionary_total)
    if length > 24:
        rows = math.ceil(length / 3)
    else:
        rows = 8
    return output_formatter(rows, length, dic_list, dictionary_total)


# A helper function for display a nice looking dictionary to the user
# @param rows count for how many rows I need
# @param length the total length for the output usage and options dictionary
# @param dic_list reformat the dictionary into a array
def output_formatter(rows, length, dic_list, dictionary_total):
    col1 = [' '] * rows
    col2 = [' '] * rows
    col3 = [' '] * rows
    col1[0] = '{'
    for i in range(0, rows):
        if length > i:
            col1[i] += insert_content(dic_list, i, rows, 0, dictionary_total)
        if length > i + rows:
            col2[i] += insert_content(dic_list, i, rows, 1, dictionary_total)
        if length > i + (2 * rows):
            col3[i] += insert_content(dic_list, i, rows, 2, dictionary_total)

    return print_output_from_rows(col1, col2, col3, rows)


# Helper function for inserting the key value pairs into output dictionary
# @param dic_list a dictionary the built from user argument but reform to a list
# @param idx the current row index
# @param rows count of the rows
# @col_idx index of the col
# @return return the key value pair in a outputting form according to the type of values
def insert_content(dic_list, idx, rows, col_idx, dictionary_total):
    if check_value_type(dictionary_total[dic_list[idx + (col_idx * rows)]]):
        return '\'{}\': {}'.format(dic_list[idx + (col_idx * rows)],
                                   dictionary_total[dic_list[idx + (col_idx * rows)]])
    else:
        return '\'{}\': \'{}\''.format(dic_list[idx + (col_idx * rows)],
                                       dictionary_total[dic_list[idx + (col_idx * rows)]])


# Helper method for defining whether the value is a string or a primitive type
# @param value the value for current key in the dictionary
def check_value_type(value):
    return type(value) == int or type(value) == float \
           or type(value) == bool or value is None


# Helper method for printing out dictionary as a json string to user
# @param row1 hold the values for output column one
# @param row1 hold the values for output column two
# @param row1 hold the values for output column three
# @param rows2 counter for number of rows
def print_output_from_rows(col1, col2, col3, rows):
    spaces1 = len(max(col1, key=len))
    spaces2 = len(max(col2, key=len))
    if TEST:
        return col1 + col2 + col3
    final_output = ""
    for k in range(rows):
        out = col1[k].ljust(spaces1) + ' ' * 4 \
              + col2[k].ljust(spaces2) + ' ' * 4 \
              + col3[k].ljust(spaces2)
        if not TEST:
            if k == rows - 1:
                final_output += (out.rstrip() + '}\n')
            else:
                final_output += (out.rstrip() + '\n')
    return final_output
