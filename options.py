"""
Options:
  -h --help --helping --haha -hhh --ooooo  Show this screen.
  --sorted  Show sorted.
  -o FILE --output=<file>  Speed in knots [default: ./test.txt].
  --version     Show version.
  --speed=<kn> -s KN  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
"""
import re
import json

Options_dic = {}

#####################################################################################################
#####################################################################################################
# Test cases
test_args1 = ["naval_fate.py", "--sorted", "-o=haha.txt", "--speed=15", "--quiet", "--verbose"]
test_args2 = ["naval_fate.py", "up", "-o=haha.txt", "--speed=27", "--quiet", "--verbose"]
test_args3 = ["naval_fate.py", "up", "down", "--speed=6", "--quiet", "--verbose"]
test_args4 = ["naval_fate.py", "up", "down", "left", "--quiet", "--verbose"]
test_args5 = ["naval_fate.py", "up", "down", "left", "right", "--verbose"]
test_args6 = ["naval_fate.py", "up", "down", "left", "right", "center"]


#####################################################################################################
#####################################################################################################


# Main function for checking options
def options():
    doc = __doc__
    if doc is None:
        return
    doc.strip()
    doc = doc.split("\n")
    check_option_lines(doc)


# Process options from docstring, treat lines that starts with '-' or '--' as options
def check_option_lines(doc):
    for line in doc:
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
def process_options(tmp_array, count, found, old_key):
    if not found:
        return check_first_option(tmp_array, count)
    else:
        return check_other_option(tmp_array, count, old_key)


# Insert the option into dictionary with no same option command exist in the dictionary ('--sorted')
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
def building_output_options_dictionary(test_args):
    output_dic = Options_dic.copy()
    output_dic = test_options(test_args, output_dic)

    for k in list(output_dic):
        if ' ' in k:
            put = sorted(k.split(), key=len, reverse=True)[0]
            if '=' in put:
                output_dic = {key if key != k else put.split('=')[0]: value for key, value in output_dic.items()}
            else:
                output_dic = {key if key != k else put: value for key, value in output_dic.items()}

    json_object = json.dumps(output_dic, indent=2)
    print(json_object)


# Matching the input options and separate them by whether the argument has a value (contains a equals sign)
def test_options(test_args, output_dic):
    for e in test_args:
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


if __name__ == '__main__':
    options()
    building_output_options_dictionary(test_args1)
    building_output_options_dictionary(test_args2)
    building_output_options_dictionary(test_args3)
    building_output_options_dictionary(test_args4)
    building_output_options_dictionary(test_args5)
    building_output_options_dictionary(test_args6)
