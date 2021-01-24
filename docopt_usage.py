import json
import warnings
import sys

Name = ""
Version = ""
Usages = []
Options = []

Arguments = []

Usage_dic = {}

Patterns = []


class Token:
    def __init__(self, text, left, right, ty):
        self.txt = text
        self.l = left
        self.r = right
        self.type = ty
        self.isReq = True

    def __str__(self):
        return self.txt

    def __repr__(self):
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
            res.append(Token(x, token.l, None, None))
        else:
            if index < (len(res) - 1):
                tokenObj = Token(x, res[index], None, None)
            else:
                tokenObj = Token(x, res[index], token.r, None)
            if tokenObj.txt.startswith('-'):
                tokenObj.type = "Option"
            else:
                tokenObj.type = "Command"            
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
                tokenObj = Token(tokenRaw, None, None, None)
                tokenObjs.append(tokenObj)
                    
            else:
                tokenObj = Token(tokenRaw, tokenObjs[index], None, None)
                tokenObjs[index].r = tokenObj
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
                    token = splitToken(token)
                    mutex.append(token)
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
            args.append(token.txt[startIndex : endIndex])
            token.type = "Argument"
        else:
            if token.txt.isupper():
                args.append(token.txt)
                token.type = "Argument"
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
                argument = token.txt[index+2 : len(token.txt)-1]
                options.append(Option(token.txt[:index], argument, "LONG"))
                token.type = "Option"
            else:
                options.append(Option(token.txt, argument, "LONG"))
                token.type = "Option"
        else:
            if token.txt.startswith('-') is True:
                # Handle short option
                options.append(Option(token.txt, argument, "SHORT"))
                token.type = "Option"
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
                            token.type = "Command"
                    else:
                        commands.append(token.txt)
                        token.type = "Command"
    return commands

def getOneOrMore(tokens):
    oneOrMore = []
    for token in tokens:
        # If ellipsis occurs in its own token
        if token.txt == '...':
            oneOrMore.append(token.l.txt)
        else:
            # If ellipsis occurs in same token as another element
            if '...' in token.txt:
                index = token.txt.index('...')
                oneOrMore.append(token.txt[:index].strip("<>")) # Append part of token that does not include ellipsis
    return oneOrMore

def printElements(args, options, commands, count):
    print(f"---------- Pattern {count+1} ----------\n")
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
        isReq = True
    else:
        closed = ']'
        isReq = False
    requiredTokens = []
    for token in tokens:
        if open in token.txt:
            complete = False
            token.txt = token.txt.strip(open)

            # if closed parenthesis is in the same token
            if closed in token.txt:
                complete = True
                token.txt = token.txt.strip(closed)
                token.isReq = isReq
                requiredTokens.append(token)

            else:

                token.isReq = isReq
                tempRequired = [token]

                index = tokens.index(token)
                token = token.r
                # search for closed parenthesis until we find it or reach the end of the pattern
                while complete is False and token is not None:
                    token.isReq = isReq
                    tempRequired.append(token)
                    if closed in token.txt:
                        complete = True
                        token.txt = token.txt.strip(closed)
                    else:
                        token = token.r
                if complete is True:
                    requiredTokens.append(tempRequired)
                else:
                    warnings.warn("Could not find closed paren or bracket.")
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
        #print(mutex)
        
        # Get arguments
        args = getArgs(tokenObjs)

        # Get options
        options = getOptions(tokenObjs)

        # Get commands
        commands = getCommands(tokenObjs)

        # Get elements that can occur one or more times (...)
        oneOrMore = getOneOrMore(tokenObjs)

        # Create key value pairs for arguments
        for arg in args:
            if arg not in Usage_dic:
                Usage_dic[arg] = None

        # Create key value pairs for options
        for opt in options:
            if opt.txt not in Usage_dic:
                # Handle options without arguments
                if opt.arg is None:
                    Usage_dic[opt.txt] = False
                # Handle options with arguments by setting dict value to value previously found in args
                else:
                    Usage_dic[opt.txt] = Usage_dic[opt.arg]
                    del Usage_dic[opt.arg]  # Remove unneccesary argument

        # Create key value pairs for commands
        for com in commands:
            if com not in Usage_dic:
                Usage_dic[com] = False

        
        # Handle mutex tokens
        # Replace tokens containing mutex elements with a single list of mutex tokens
        # Ex: [--moored | --drifting] gets replaced with [[--moored, --drifting]]
        for index, token in enumerate(tokenObjs):
            if token.txt == '|':
                tokenObjs[index-1] = [token.l, token.r]
                tokenObjs.remove(token.r)
                tokenObjs.remove(token)
            elif '|' in token.txt:
                tokenObjs[index] = splitToken(token)

        Patterns.append(tokenObjs)

    #print(Usage_dic)


        # Print args, options, and commands for each pattern
        #printElements(args, options, commands, count)
        



def docopt(doc, argv=None, help_message=True, version=None):
    Arguments.extend(sys.argv[1:])
    processing_string(doc, help_message, version)
    parse_usage()

    patternToUse = None

    for num, p in enumerate(Patterns):
        foundConflict = False
        for index, token in enumerate(p):

            if index >= len(Arguments):
                inputToken = None
            else:
                inputToken = Arguments[index]
            print(f"Pattern #{num}: PToken: {token} InputToken: {inputToken}")

            # Skip if too many input tokens than tokens in the pattern
            if len(Arguments) > len(p):
                foundConflict = True
                break

            # ERROR TO FIX: TOO FEW INPUT TOKENS BUT NO OPTIONAL ELEMENTS
            
            # Handle mutex tokens, input token must match only one of them
            if type(token) is list:
                foundMutexMatch = False
                for t in token:
                    # Check if token is optional
                    if t.isReq is False:
                        break
                    if Arguments[index] == t.txt:
                        foundMutexMatch = True

                        # Check if next input token is also in mutex list
                        if index+1 < len(Arguments):
                            if any(n.txt == Arguments[index+1] for n in token):
                                foundConflict = True

                        break
            
            # If input doesn't contain an optional token
            elif token.isReq is False and index >= len(Arguments):
                continue

            # If pattern token is a command, check if input token matches
            elif token.type == "Command":
                if Arguments[index] == token.txt:
                    continue
                else:
                    foundConflict = True
                    break

            # If pattern token is an option, check if input token is also an option
            elif token.type == "Option" and Arguments[index].startswith('-') is False:
                foundConflict = True
                break

        if foundConflict is False:
            patternToUse = num
            break

    print(patternToUse)

    return doc







