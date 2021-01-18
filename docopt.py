"""
  docopt is for the ...
"""
import warnings
import sys
import re
import json

# A global variable for storing the name of the user project
Name = ""
# A global variable for storing the version of the user project
Version = ""
# A global array for storing the usage paragraphs line by line
Usages = []
# A global array for storing the options paragraphs line by line
Options = []
# A global array for storing the arguments that passed by the user command line
Arguments = []
# A global dictionary for storing the key and value for the options in docstring
Options_dic = {}


# Main function for docopt.
# @param doc docstring that pass from the user program
# @param argv programmer can pre-pass some parameters into docopt and
#       those parameters is treat as default existing arguments
# @param help_message user can specify whether they want docopt to display
#       the help message whenever user execute the program
# @param version programmers can specify the version of the project and display to user
def docopt(doc, argv=None, help_message=True, version=None):
    Arguments.extend(sys.argv)
    processing_string(doc, help_message, version)
    options_parser()
    return doc


# Main Controller for processing the docstring.
# @param doc docstring pass from the main function
# @param help_message to tell docopt whether user want to display help message when the program executes
# @param version The version string pass from main function
def processing_string(doc, help_message, version):
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

    check_warnings(usage, options)
    if help_message:
        print_help(name, version, usage, options)
    dictionary_builder(name, version, usage, options)


# Function for building an array for usages, options from docstring
# and gets the name and version from docstring.
# @param name the project name specify in the docstring
# @param version the version passed from the main function
# @param usage a string that retrieve from the docstring
# @param options a string that retrieve from the docstring
def dictionary_builder(name, version, usage, options):
    global Name
    global Version
    Name = name
    Version = version
    Usages.extend(usage.split("\n"))
    Options.extend(options.split("\n"))


# Function for testing whether the docstring contains a usage part and a options part.
# Will display warning to the user program when missing parts
# @param usage a string the retrieve from the docstring
# @param options a string that retrieve from the docstring
def check_warnings(usage, options):
    if len(usage) == 0:
        warnings.warn('No usage indicated from docstring')
    if len(options) == 0:
        warnings.warn('No options indicated from docstring')


# This function will be involved when user program specify help=True.
# @param name name passed from the main function that retrieve from the docstring
# @param version version information that retrieve from the docstring
# @param usage usage string that retrieve from the docstring
# @param options options string that retrieve from the docstring
def print_help(name, version, usage, options):
    output = ""
    if len(name) > 0:
        output += name + "\n\n"
    if version is not None:
        output += "Version:\n  " + version + "\n\n"
    output += usage + "\n\n"
    output += options + "\n\n"
    print(output)


# Main function for checking options
def options_parser():
    check_option_lines()
    options_dic = building_output_options_dictionary()
    print(options_dic)


# Process options from docstring, treat lines that starts with '-' or '--' as options
def check_option_lines():
    for line in Options:
        tmp_array = line.split()
        # Skip the line that is not starts with '-' or '--'
        if len(tmp_array) > 0 and tmp_array[0].strip()[:1] != '-':
            continue

        # This value will set to ture if a keyword for a option command is found and inserted into the dictionary
        found = False
        # This key will keep updating while there is more keyword choices for the same option command
        old_key = None

        for count in range(len(tmp_array)):
            if tmp_array[count][:2] == '--':
                old_key = process_options(tmp_array, count, found, old_key)
                found = True
            elif tmp_array[count][:1] == '-':
                old_key = process_options(tmp_array, count, found, old_key)
                found = True

        default_value = line[line.find("[") + 1:line.find("]")]
        if default_value is not None:
            default_value.strip()

            # Test if this line of docstring contains a default value
            if re.search('default:', default_value, re.IGNORECASE):
                tmp_dic = {old_key: default_value.split()[1]}
                Options_dic.update(tmp_dic)
    print(Options_dic)


# Check if the option dictionary already exists the same option
# (different keyword but same option command e.g."-h --help")
# @param tmp_array the current checking line from options in the docstring
# @param count specify the location of array for the string that is split by space
# @param found a boolean to show whether the keyword for command is exists in the dictionary already
# @param old_key the current key string in options dictionary
# @return return the current new key for the dictionary for the current line
def process_options(tmp_array, count, found, old_key):
    if not found:
        return check_first_option(tmp_array, count)
    else:
        return check_other_option(tmp_array, count, old_key)


# Insert the option into dictionary with no same option command exist in the dictionary ('--sorted')
# @param tmp_array the current checking line from options in the docstring
# @param count specify the location of array for the string that is split by space
# @return return the current new key for the dictionary for the current line
def check_first_option(tmp_array, count):
    if '=' in tmp_array[count]:
        old_key = tmp_array[count]
        tmp_dic = {old_key: None}
    elif len(tmp_array) > count + 1 and tmp_array[count + 1].isupper():
        # The option with Value (either in -s FILE or -p=<file>) will always change to -p=<file>
        # when insert into the dictionary
        old_key = f"{tmp_array[count]}=<{tmp_array[count + 1].lower()}>"
        tmp_dic = {old_key: None}
    else:
        old_key = tmp_array[count]
        tmp_dic = {old_key: False}

    Options_dic.update(tmp_dic)
    return old_key


# Insert the option into dictionary with same option command already exist in the dictionary
# e.g. insert '--help' when '-h' is exists already
# @param tmp_array the current checking line from options in the docstring
# @param count specify the location of array for the string that is split by space
# @param old_key specify the current key for updating the key in options dictionary
# @return return the current new key for the dictionary for the current line
def check_other_option(tmp_array, count, old_key):
    global Options_dic

    if '=' in tmp_array[count]:
        new_key = old_key + " " + tmp_array[count]
    elif len(tmp_array) > count + 1 and tmp_array[count + 1].isupper():
        # The option with Value (either in -s FILE or -p=<file>) will always change to -p=<file>
        # when insert into the dictionary
        new_key = old_key + " " + f"{tmp_array[count]}=<{tmp_array[count + 1].lower()}>"
    else:
        new_key = old_key + " " + tmp_array[count]

    # This line is for updating the key in the option dictionary
    Options_dic = {key if key != old_key else new_key: value for key, value in Options_dic.items()}
    return new_key


# Update the options dictionary with new value according to user arguments, remove the duplicated option keys
# after the new dictionary is built
# @return return the new dictionary and set values according to the user command line
def building_output_options_dictionary():
    output_dic = Options_dic.copy()
    output_dic = test_options(output_dic)
    for k in list(output_dic):
        if ' ' in k:
            put = sorted(k.split(), key=len, reverse=True)[0]
            if '=' in put:
                output_dic = {key if key != k else put.split('=')[0]: value for key, value in output_dic.items()}
            else:
                output_dic = {key if key != k else put: value for key, value in output_dic.items()}
    return output_dic


# Matching the input options and separate them by whether the argument has a value (contains a equals sign)
# @param output_dic a copy of the options dic
# @return return the updated output_dic according to the user arguments
def test_options(output_dic):
    for e in Arguments:
        ne = e.strip()
        if ne[:1] == "-" and '=' not in ne:
            output_dic = check_keys(ne, False, output_dic)
        elif ne[:1] == "-" and '=' in ne:
            output_dic = check_keys(ne, True, output_dic)
        else:
            continue
    return output_dic


# Helper function for matching the input options from user and the option dictionary
# Always output the most detail keyword for option command when there exists choices
# @param element one of the argument that pass in by the user command line
# @param is_contain_equal a boolean for whether the argument from command line contains a value
# @param output_dic a copy of the options dic
# @return returns a updated value dictionary according the arguments in the user command line
def check_keys(element, is_contain_equal, output_dic):
    if not is_contain_equal:
        for k in Options_dic:
            put = sorted(k.split(), key=len, reverse=True)
            if element in put:
                output_dic = {key if key != k else put[0]: value for key, value in output_dic.items()}
                tmp_dic = {put[0]: True}
                output_dic.update(tmp_dic)
    else:
        for k in Options_dic:
            if '=' in k:
                put = sorted(k.split(), key=len, reverse=True)
                for tmp in put:
                    if element.split('=')[0] == tmp.split('=')[0]:
                        output_dic = {key if key != k else put[0].split('=')[0]: value for key, value in
                                      output_dic.items()}
                        tmp_dic = {put[0].split('=')[0]: element.split('=')[1]}
                        output_dic.update(tmp_dic)
    return output_dic
