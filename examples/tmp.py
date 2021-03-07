doc2 = """Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
  naval_fate.py ship shoot <x> <y>
  naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]
  naval_fate.py (-h | --help)
  naval_fate.py --version

Options:
  -h --help --helping --haha -hhh --ooooo  Show this screen.
  --sorted  Show sorted.
  -o FILE --output=<value>  Speed in knots [default: ./test.txt].
  --version     Show version.
  --speed=<kn> -s KN  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
  --rr     Show version.
  --aaa=<value>      Moored (anchored) mine [default: 20].
  --yyy    Drifting mine.

"""
import re
import docopt_util

usage_array, options_array = docopt_util.processing_string(doc2, False, version="testing tmp")
print(usage_array)
print(options_array)
#
# res = re.sub(r'\[.*?]', lambda x: ''.join(x.group(0).split()), str)
# res = re.sub(r'\(.*?\)', lambda x: ''.join(x.group(0).split()), res)
# res = re.sub(r'<.*?>', lambda x: ''.join(x.group(0).split()), res)
#
# res = re.search(r'\((.*?)\)', res).group(1)
# print(res)
