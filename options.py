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
new_key = ""

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


def options():
    doc = __doc__
    if doc is None:
        return
    doc.strip()
    doc = doc.split("\n")
    for line in doc:
        tmp_array = line.split()
        found = False
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
            if re.search('default:', default_value, re.IGNORECASE):
                tmp_dic = {new_key: default_value.split()[1]}
                Options_dic.update(tmp_dic)
    print(Options_dic)


def process_options(tmp_array, count, found, old_key):
    if not found:
        return check_first_option(tmp_array, count)
    else:
        return check_second_option(tmp_array, count, old_key)


def check_first_option(tmp_array, count):
    global new_key

    if '=' in tmp_array[count]:
        new_key = tmp_array[count]
        tmp_dic = {new_key: None}
    elif len(tmp_array) > count + 1 and tmp_array[count + 1].isupper():
        new_key = f"{tmp_array[count]}=<{tmp_array[count + 1].lower()}>"
        tmp_dic = {new_key: None}
    else:
        new_key = tmp_array[count]
        tmp_dic = {new_key: False}

    Options_dic.update(tmp_dic)
    return new_key


def check_second_option(tmp_array, count, old_key):
    global new_key
    global Options_dic

    if '=' in tmp_array[count]:
        new_key = old_key + " " + tmp_array[count]
    elif len(tmp_array) > count + 1 and tmp_array[count + 1].isupper():
        new_key = old_key + " " + f"{tmp_array[count]}=<{tmp_array[count + 1].lower()}>"
    else:
        new_key = old_key + " " + tmp_array[count]

    Options_dic = {key if key != old_key else new_key: value for key, value in Options_dic.items()}
    return new_key


def test_options(test_args):
    output_dic = Options_dic.copy()
    for e in test_args:
        ne = e.strip()
        if ne[:2] == "--" and '=' not in ne:
            output_dic = check_keys(ne, False, output_dic)
        elif ne[:2] == "--" and '=' in ne:
            output_dic = check_keys(ne, True, output_dic)
        elif ne[:1] == "-" and '=' not in ne:
            output_dic = check_keys(ne, False, output_dic)
        elif ne[:1] == "-" and '=' in ne:
            output_dic = check_keys(ne, True, output_dic)
        else:
            continue

    for k in list(output_dic):
        if ' ' in k:
            put = sorted(k.split(), key=len, reverse=True)[0]
            if '=' in put:
                output_dic = {key if key != k else put.split('=')[0]: value for key, value in output_dic.items()}
            else:
                output_dic = {key if key != k else put: value for key, value in output_dic.items()}

    json_object = json.dumps(output_dic, indent=2)
    print(json_object)


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
                        output_dic = {key if key != k else put[0].split('=')[0]: value for key, value in output_dic.items()}
                        tmp_dic = {put[0].split('=')[0]: element.split('=')[1]}
                        output_dic.update(tmp_dic)
    return output_dic


if __name__ == '__main__':
    options()
    test_options(test_args1)
    test_options(test_args2)
    test_options(test_args3)
    test_options(test_args4)
    test_options(test_args5)
    test_options(test_args6)
