import json
import warnings

Name = ""
Version = ""
Usages = []
Options = []


def processing_string(doc):
    usage = ""
    options = ""
    partition_string = doc.strip().split('\n\n')
    name = partition_string[0]
    for line in partition_string:
        if "Usage:" in line:
            usage = line.strip()
        if "Options:" in line:
            options = line.strip()

    if len(name) == 0:
        warnings.warn('Name of the project is empty')
    if len(usage) == 0:
        warnings.warn('No usage indicated from docstring')
    if len(options) == 0:
        warnings.warn('No options indicated from docstring')


def docopt(doc, msg="", argv=None, help_message=True, version=None):
    processing_string(doc)
    return doc







