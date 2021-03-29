# # Process options from docstring, treat lines that
# # starts with '-' or '--' as options
# def check_option_lines(options):
#     """
#     Args:
#         options: options the options strings from docstring.
#
#     Returns:
#         new_pat: the array that holds all options objects.
#
#     >>> check_option_lines(options= "-h --help")
#     [Option('-h')]
#     >>> check_option_lines(options= "hello world")
#     []
#     """
#     new_pat = []
#     for line in options:
#         tmp_array = line.split()
#         if len(tmp_array) > 0 and tmp_array[0].strip()[:1] != '-':
#             continue
#         token = None
#         for count, element in enumerate(tmp_array, start=0):
#
#             if element[:2] == '--':
#                 token = check_option_lines_long(element, tmp_array, count, token)
#             elif element[:1] == '-':
#                 token = check_option_lines_short(element, tmp_array, count, token)
#
#         token = find_default_value(line, token)
#         new_pat.append(token)
#     return new_pat
#
#
# # create the Option with long keyword type if the current keyword is not exists.
# # else insert the long version of keyword into the existing keyword object.
# def check_option_lines_long(element, tmp_array, count, token):
#     """
#        Args:
#            element: the keyword of the current option.
#            tmp_array: the string the contains the current line of option description.
#            count: the index of current keyword in the option line.
#            token: the class object of Option that holds information of option. If object is None,
#                   then create a brand new object for the new keyword.
#
#        Returns:
#            token: the updated options object with long form of the keyword.
#
#        >>> check_option_lines_long('--value=<help>', '--value=<help> Input value', 0, None)
#        token = Option('--value', None, True, None, '--value')
#        >>> check_option_lines_long('--value', '--value HELP', 0, None)
#        token = Option('--value', None, True, None, '--value')
#        >>> check_option_lines_long('--help', '--help show help message', 0, None)
#        token = Option(''--help', False, False, None, ''--help')
#        """
#     if len(tmp_array) > count + 1 and tmp_array[count + 1].isupper():
#         if token is None:
#             token = Option(element, None, has_value=True, short=None, long=element)
#         else:
#             token.long = element
#     elif '=' in element:
#         if token is None:
#             text = re.search('\\S+=', element).group().strip("=")
#             token = Option(text, None, has_value=True, short=None, long=text)
#         else:
#             token.long = re.search('\\S+=', element).group().strip("=")
#     else:
#         if token is None:
#             token = Option(element, False, has_value=False, short=None, long=element)
#         else:
#             token.long = element
#     return token
#
#
# # create the Option with short keyword type if the current keyword is not exists.
# # else insert the short version of keyword into the existing keyword object.
# def check_option_lines_short(element, tmp_array, count, token):
#     """
#     Args:
#         element: the keyword of the current option.
#         tmp_array: the string the contains the current line of option description.
#         count: the index of current keyword in the option line.
#         token: the class object of Option that holds information of option.
#
#         Returns:
#             token: the updated options object with short form of the keyword.
#
#        >>> check_option_lines_long('-v=<help>', '-v=<help> Input value', 0, None)
#        token = Option('-v', None, True, '-v', None)
#        >>> check_option_lines_long('-v', '-v HELP', 0, None)
#        token = Option('-v', None, True, '-v', None)
#        >>> check_option_lines_long('-h', '-h show help message', 0, None)
#        token = Option('-h', False, False, '-h', None)
#     """
#     if len(tmp_array) > count + 1 and tmp_array[count + 1].isupper():
#         if token is None:
#             token = Option(element, None, has_value=True, short=element, long=None)
#         else:
#             token.short = element
#     elif '=' in element:
#         if token is None:
#             text = re.search('\\S+=', element).group().strip("=")
#             token = Option(text, None, has_value=True, short=text, long=None)
#         else:
#             token.short = re.search('\\S+=', element).group().strip("=")
#     else:
#         if token is None:
#             token = Option(element, False, has_value=False, short=element, long=None)
#         else:
#             token.short = element
#     return token
#
#
# # A function for finding whether the current line of option has
# # a default value that specify by the programmer
# def find_default_value(line, token):
#     """
#     Args:
#         line: a string that holds the current line.
#         token: The toekn object for holding option.
#
#     Returns:
#         token: the updated token accroding the existence of default value
#
#     >>> tmp_token = Option('-v', None, True, '-v', None)
#     >>> find_default_value('-v FILE  input file [default: ./test.txt].', tmp_token)
#     tmp_token = Option('-v', './test.txt', True, '-v', None)
#
#     >>> tmp_token = Option('--location', None, True, '-l', '--location')
#     >>> find_default_value('-l=<location_value>  insert coordinate [default: 10.88].', tmp_token)
#     tmp_token = Option('--location', 10.88, True, '-l', '--location')
#     """
#
#     matching = re.search(r'\[.*?]', line)
#     if matching is not None:
#         default_value = matching.group(0)[1:-1].strip()
#
#         # Test if this line of docstring contains a default value
#         if re.search('default:', default_value, re.IGNORECASE):
#             try:
#                 int(default_value.split()[1])
#                 token.value = int(default_value.split()[1])
#             except ValueError:
#                 try:
#                     float(default_value.split()[1])
#                     token.value = float(default_value.split()[1])
#                 except ValueError:
#                     token.value = default_value.split()[1]
#     return token
