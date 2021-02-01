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

# Object for storing token information
# @param text stores the raw text of the token
# @param left is a pointer to the token to the left in the usage pattern
# @param right is a pointer to the token to the right in the usage pattern
# @param ty denotes the type of the token (Argument, Command, or Option)
# @param isReq denotes whether the token is required or optional (True if required, False if optional)
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

# Split token by '|' into two mutually exclusive Token objects
# @param token is a Token object of the form "token1|token2"
# Returns a list object with the split tokens, i.e. ["token1", "token2"]
def splitToken(token):
    rawSplit = token.txt.split('|')
    res = []
    index = 0
    for x in rawSplit:

        # Create first Token object
        if index == 0:
            tokenObj = Token(x, token.l, None, None)
            tokenObj.isReq = token.isReq
            res.append(tokenObj)

        # Create rest of the Token objects
        else:
            if index < (len(res) - 1):
                tokenObj = Token(x, res[index], None, None)
            else:
                tokenObj = Token(x, res[index], token.r, None)
            tokenObj.isReq = token.isReq
            res.append(tokenObj)  
            res[index].r = tokenObj     # Link previous token to new token
            index += 1
        
        # Set type for split tokens
        if tokenObj.txt.startswith('-'):
            tokenObj.type = "Option"
        else:
            tokenObj.type = "Command" 

    return res

# Extract raw tokens from pattern and convert them to Token objects
# @param pattern is a string containing a single usage pattern
# @param name the name of the program - used to ignore the program name when creating the tokens
# Returns a linked list of Token objects
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

# Sets type attribute for all argument tokens to Argument
# @param tokens is the list of Token objects for a given pattern
# Simply modifies the existing tokens, no return value
def parseArgs(tokens):
    for token in tokens:
        if token.txt.startswith('<') is True and token.txt.endswith('>') is True:
            token.type = "Argument"
        else:
            if token.txt.isupper():
                token.type = "Argument"

# Sets type attribute for all option tokens to Option
# @param tokens is the list of Token objects for a given pattern
# Simply modifies the existing tokens, no return value
def parseOptions(tokens):
    for token in tokens:
        if token.txt.startswith('-') is True:
            token.type = "Option"

# Sets type attribute for all command tokens to Command
# @param tokens is the list of Token objects for a given pattern
# Simply modifies the existing tokens, no return value
def parseCommands(tokens):
    commands = []
    for token in tokens:
        # Ignore lone '|' tokens
        if token.txt != '|':
            # If token isn't an argument or an option, it must be a command
            if token.type != "Argument" and token.type != "Option":
                if '|' not in token.txt:
                    token.type = "Command"
    return commands

# Handle mutex tokens
# Replace tokens containing mutex elements with a single list of mutex tokens
# Ex: "[--moored | --drifting]" gets replaced with [[--moored, --drifting]]
# @param tokenObjs the list of Token objects for a given pattern
# No return value
def parseMutex(tokenObjs):
    for index, token in enumerate(tokenObjs):
        if token.txt == '|':
            tokenObjs[index-1] = [token.l, token.r]
            tokenObjs.remove(token.r)
            tokenObjs.remove(token)
        elif '|' in token.txt:
            tokenObjs[index] = splitToken(token)

# Populate global Usage_dic with default argument and command values
# @param tokenObjs the finalized list of Token objects for a given pattern
# No return value
def buildUsageDic(tokenObjs):
    for token in tokenObjs:
        if type(token) is list:
            for t in token:
                if t.type == "Argument":
                    Usage_dic[t.txt.strip("<>")] = None
                elif t.type == "Command":
                    Usage_dic[t.txt] = False
        else:
            if token.type == "Argument":
                Usage_dic[token.txt.strip("<>")] = None
            if token.type == "Command":
                Usage_dic[token.txt] = False

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
# @param tokens a list of Token objects for a given pattern
# @param open the open character used to denote whether to process () or []
# Labels each token as required or optional under the isReq parameter
# No return value
def process_Paren(tokens, open):
    if open == '(':
        closed = ')'
        isReq = True
    else:
        closed = ']'
        isReq = False
    for token in tokens:
        if open in token.txt:
            complete = False
            token.txt = token.txt.strip(open)

            # if closed parenthesis is in the same token
            if closed in token.txt:
                complete = True
                token.txt = token.txt.strip(closed)
                token.isReq = isReq

            else:
                token.isReq = isReq
                tempRequired = [token]
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
                if complete is False:
                    warnings.warn("Could not find closed paren or bracket.")

# Examine each usage pattern and label each token appropriately (argument, option, or command; optional or required)
# Builds Usage_dic using these Token objects
# Fills Patterns global object with finalized lists of tokens
def parse_usage():
    # Extract program name
    Usages.pop(0)
    s = Usages[1].split(" ")
    name = s[2]
    
    # Parse each pattern in Usages
    for pattern in Usages:

        # Convert tokens in pattern to a linked list
        tokenObjs = convertTokens(pattern, name)

        # Process required tokens
        process_Paren(tokenObjs, '(')

        # Process optional tokens
        process_Paren(tokenObjs, '[')

        parseArgs(tokenObjs)

        parseOptions(tokenObjs)

        parseCommands(tokenObjs)

        # Handle mutually exclusive elements
        parseMutex(tokenObjs)

        # Build the usage dic using finalized token objects
        buildUsageDic(tokenObjs)
            
        # Append the finalized token list to the list of patterns
        Patterns.append(tokenObjs)

# Check if input token matches one (and only one) of the mutually exclusive tokens
# @param index the index of which token we are examining, used to retrieve input token in Arguments
# @param token the token we are examining
# Returns true if a conflict is found, false otherwise
def checkMutex(index, token):
    foundConflict = False
    if type(token) is list:
        if token[0].isReq is False and index >= len(Arguments):
            Arguments.insert(index, "None")
        foundMutexMatch = False
        for t in token:
            # Check if token is optional
            if t.isReq is False:
                foundMutexMatch = True  # Bypass check later on
                break
            if Arguments[index] == t.txt:
                foundMutexMatch = True

                # Check if next input token is also in mutex list
                if index+1 < len(Arguments):
                    if any(n.txt == Arguments[index+1] for n in token):
                        foundConflict = True
                break
        if foundMutexMatch is False:
            if token[0].isReq is True:
                foundConflict = True
            else:
                Arguments.insert(index, "None")
            foundConflict = True
    return foundConflict

# Check individual arg, command, and optional tokens for a match with corresponding input token
# @param index the index of which token we are examining, used to retrieve input token in Arguments
# @param token the token we are examining
# Returns true if a conflict is found, false otherwise
def checkTokens(index, token):
    foundConflict = False
    # Handle missing optional arguments
    if token.type == "Argument" and token.isReq is False:
        if Arguments[index] == (token.r.txt if type(token.r) is Token else token.r[0].txt):
            Arguments.insert(index, "None")
            
    # If pattern token is a command, check if input token matches
    elif token.type == "Command":
        if Arguments[index] != token.txt:
            # Ignore if optional, break if required
            if token.isReq is True:
                foundConflict = True
            else:
                Arguments.insert(index, "None")

    # If pattern token is an option, check if input token matches
    elif token.type == "Option":
        inputToken = Arguments[index]
        pToken = token.txt
        # Ignore option arguments
        if '=' in Arguments[index] and '=' in token.txt:
            inputToken = Arguments[index][:Arguments[index].find('=')]
            pToken = pToken[:pToken.find('=')]
        if inputToken != pToken:
            # Ignore if optional, break if required
            if token.isReq is True:
                foundConflict = True
            else:
                Arguments.insert(index, "None")
    return foundConflict

# Compare input tokens with a Usage pattern p
# @param p the usage pattern we are checking, a list of Token objects
# Returns True if a conflict is found, False otherwise
def findConflict(p):
    foundConflict = False   # Used to check if the pattern does not match, success if foundConflict remains False
    for index, token in enumerate(p): 

        if type(token) is list:
            foundConflict = checkMutex(index, token)
            if foundConflict is True:
                break
            
        # Check if input doesn't contain trailing optional token
        elif token.isReq is False and index >= len(Arguments):
            Arguments.insert(index, "None")
            continue

        else:
            foundConflict = checkTokens(index, token)
            if foundConflict is True:
                break

    return foundConflict

# Finds which Usage pattern matches the input
# Returns index of first match found
# If no match found, function returns None
def findMatchingPattern():
    patternToUse = None

    # Explore each pattern to determine which one matches the input
    for num, p in enumerate(Patterns):

        numReq = 0
        # Get number of req tokens for each pattern
        for t in p:
            if type(t) is Token:
                if t.isReq is True:
                    numReq += 1
            else:
                if t[0].isReq is True:
                    numReq += 1

        if len(Arguments) < numReq:
            continue

        # Skip if more input tokens than tokens in the pattern
        if len(Arguments) > len(p):
            continue

        if findConflict(p) is False:
            patternToUse = num
            break
    return patternToUse


# Fill Usage_dic with appropriate values from the input
# @param patternToUse an integer denoting which Usage pattern matches the input
# No return value
def populateUsageDic(patternToUse):
    if patternToUse is not None:
        for index, token in enumerate(Patterns[patternToUse]):
            if type(token) is list:
                if token[0].type != "Option":
                    Usage_dic[Arguments[index]] = True
            else:
                if token.type == "Argument":
                    Usage_dic[token.txt.strip('<>')] = Arguments[index]
                elif token.type == "Command":
                    # Check if input ignores optional command
                    if Arguments[index] != "None":
                        Usage_dic[token.txt] = True
        print(Usage_dic)
    else:
        print("No pattern found")
        

####################################################################
###################################################################
# Main function for checking usage
# After execution, Usage_dic is populated with appropriate values if successful
def usage_parser():
    parse_usage()
    patternToUse = findMatchingPattern()  
    populateUsageDic(patternToUse)

def docopt(doc, argv=None, help_message=True, version=None):
    Arguments.extend(sys.argv[1:])
    processing_string(doc, help_message, version)

    usage_parser()
    

    return doc







