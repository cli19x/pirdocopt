import json
import warnings
import sys

Name = ""
Version = ""
Usages = []
Options = []

Arguments = []


def dictionary_builder(name, version, usage, options):
    global Name
    global Version
    Name = name
    Version = version
    Usages.extend(usage.split("\n"))
    Options.extend(options.split("\n"))


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
    print_help(help_message, name, version, usage, options)
    dictionary_builder(name, version, usage, options)


def check_warnings(usage, options):
    if len(usage) == 0:
        warnings.warn('No usage indicated from docstring')
    if len(options) == 0:
        warnings.warn('No options indicated from docstring')


def print_help(is_help, name, version, usage, options):
    if is_help:
        output = name + "\n\n"
        if version is not None:
            output += "Version:\n  " + version + "\n\n"
        output += usage + "\n\n"
        output += options + "\n\n"
        print(output)


def docopt(doc, argv=None, help_message=True, version=None):
    Arguments.extend(sys.argv)
    processing_string(doc, help_message, version)
    return doc
