
# Get docstring from python: import sys; file print(__doc__)
def docstring(doc):
    print(doc)


# To return text between parenthesis: s[s.find("(")+1:s.find(")")]
s = "naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]"
a = s[s.find("(")+1:s.find(")")]
print(a)
a_r = a.split('|')
print(a_r)



