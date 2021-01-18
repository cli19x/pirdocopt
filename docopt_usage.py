import json
import warnings
import sys

Name = ""
Version = ""
Usages = []
Options = []

Arguments = []


class Token:
    def __init__(self, text, left, right):
        self.txt = text
        self.l = left
        self.r = right

    def __str__(self):
        return self.txt


class Option:
    def __init__(self, text, argument, length):
        self.txt = text
        self.arg = argument
        self.length = length

    def __str__(self):
        if self.arg is not None:
            return "Option: " + self.txt + "\tArgument: " + self.arg + "\tLength: " + self.length
        else:
            return "Option: " + self.txt + "\tLength: " + self.length


# Split token by '|' into two mutually exclusive Token objects
def splitToken(token):
    rawSplit = token.txt.split('|')
    res = []
    index = 0
    for x in rawSplit:
        if index == 0:
            res.append(Token(x, token.l, None))
        else:
            if index < (len(res) - 1):
                tokenObj = Token(x, res[index], None)
            else:
                print(index)
                tokenObj = Token(x, res[index], token.r)
            res[index].r = tokenObj
            index += 1
    return res


# Extract raw tokens from pattern and convert them to Token objects
def convertTokens(pattern, name):
    # Split pattern into individual tokens and remove leading empty space
    tokensRaw = pattern.split(" ")
    tokensRaw.pop(0)
    tokensRaw.pop(0)

    tokenObjs = list()
    index = 0

    # Convert raw token to Token format, maintained as a linked list
    for tokenRaw in tokensRaw:
        if tokenRaw != name:
            if not tokenObjs:
                tokenObj = Token(tokenRaw, None, None)
                tokenObjs.append(tokenObj)

            else:
                tokenObj = Token(tokenRaw, tokenObjs[index], None)
                tokenObjs[index].right = tokenObj
                tokenObjs.append(tokenObj)
                index += 1
    return tokenObjs


# Returns a list of mutually exclusive elements taken from tokens
# Elements in the returned list may be Tokens or lists of Tokens
def getMutex(tokens):
    mutex = []
    for token in tokens:
        if type(token) is Token:
            if '|' in token.txt:
                mutex.append(splitToken(token))
        else:
            if type(token) is list:
                found = False
                for t in token:
                    if t.txt == '|':
                        found = True
                        index = token.index(t)
                        break
                if found:
                    token.remove(token[index])
                    mutex.append(token)
    return mutex


# Returns a list of arguments extracted from tokens
def getArgs(tokens):
    args = []
    for token in tokens:
        if '<' in token.txt:
            startIndex = token.txt.index('<') + 1
            endIndex = token.txt.index('>')
            args.append(token.txt[startIndex: endIndex])
        else:
            if token.txt.isupper():
                args.append(token.txt)
    return args


# Returns a list of Option objects extracted from tokens
def getOptions(tokens):
    options = []
    for token in tokens:
        argument = None
        if token.txt.startswith('--') is True:
            # Handle long option
            # If option has an argument
            if '=' in token.txt:
                index = token.txt.index('=')
                argument = token.txt[index + 2: len(token.txt) - 1]
                options.append(Option(token.txt[:index], argument, "LONG"))
            else:
                options.append(Option(token.txt, argument, "LONG"))
        else:
            if token.txt.startswith('-') is True:
                # Handle short option
                options.append(Option(token.txt, argument, "SHORT"))
    return options


def getCommands(tokens):
    commands = []
    for token in tokens:
        # Check if token is a lone '|'
        if token.txt != '|':
            # Check if token is an argument
            if '<' not in token.txt and token.txt.isupper() is False:
                # Check if token is an option
                if token.txt.startswith('-') is False:
                    if '|' in token.txt:
                        rawSplit = token.txt.split('|')
                        for item in rawSplit:
                            commands.append(item)
                    else:
                        commands.append(token.txt)
    return commands


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

    if help_message:
        output = name + "\n\n"
        if version is not None:
            output += "Version:\n  " + version + "\n\n"
        output += usage + "\n\n"
        output += options + "\n\n"
        print(output)
    dictionary_builder(name, version, usage, options)


# Process optional ( [] ) and required ( () ) elements
# Arguments: tokens = list of Token objects, character = '(' or '['
# Returns a list of either optional or required elements
def process_Paren(tokens, open):
    if open == '(':
        closed = ')'
    else:
        closed = ']'
    requiredTokens = []
    for token in tokens:
        if open in token.txt:
            complete = False
            token.txt = token.txt.strip(open)

            # if closed parenthesis is in the same token
            if closed in token.txt:
                complete = True
                token.txt = token.txt.strip(closed)
                requiredTokens.append(token)

            else:  # TO DO: SEARCH FOR PIPE
                tempRequired = []
                tempRequired.append(token)

                index = tokens.index(token)
                token = token.right
                # search for closed parenthesis until we find it or reach the end of the pattern
                while complete is False and token is not None:
                    tempRequired.append(token)
                    if closed in token.txt:
                        complete = True
                        token.txt = token.txt.strip(closed)
                    else:
                        token = token.right

                requiredTokens.append(tempRequired)
    return requiredTokens


def parse_usage():
    # Extract program name
    Usages.pop(0)
    s = Usages[1].split(" ")
    name = s[2]

    # Parse each pattern in Usages
    for count, pattern in enumerate(Usages):

        # Convert tokens in pattern to a linked list
        tokenObjs = convertTokens(pattern, name)

        # Process required tokens
        requiredTokens = process_Paren(tokenObjs, '(')

        # Process optional tokens
        optionalTokens = process_Paren(tokenObjs, '[')

        # Retrieve mutually exclusive elements
        mutex = getMutex(requiredTokens + optionalTokens)

        # Get arguments
        args = getArgs(tokenObjs)

        # Get options
        options = getOptions(tokenObjs)

        # Get commands
        commands = getCommands(tokenObjs)

        print(f"---------- Pattern {count + 1} ----------\n")
        print("Arguments:", end=" ")
        for arg in args:
            print(arg, end="\t")
        print("\nOptions:\n----------------------")
        for option in options:
            print(option)
        print("Commands:", end=" ")
        for command in commands:
            print(command, end="\t")
        print("\n\n")


def docopt(doc, argv=None, help_message=True, version=None):
    Arguments.extend(sys.argv)
    processing_string(doc, help_message, version)
    parse_usage()
    return doc
