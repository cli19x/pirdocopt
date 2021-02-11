``pirdocopt`` a helper for enhancing your command line project 
==================================================================

How to Use
========================
It is simple just include ``docopt.py`` in you project folder and import the module ``import docoopt``.

Usages
========
When you have a command-line python program which contains a docstring and want to show user all the usage patterns
and the options that provided by you program, you just need to call docopt.py:

    """Perfect
    
       Usage:
         naval_fate.py ship new <name>
         naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
         naval_fate.py ship shoot <x> <y>
         naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]
         naval_fate.py (-h | --help)
         naval_fate.py --version

       Options:
         -h --help --helping --haha -hhh --ooooo  Show this screen.
         --sorted  Show sorted.
         -o FILE --output=<file>  Speed in knots [default: ./test.txt].
         --version     Show version.
         --speed=<kn> -s KN  Speed in knots [default: 10].
         --moored      Moored (anchored) mine.
         --drifting    Drifting mine.
         --rr     Show version.
         --aaa=<file>      Moored (anchored) mine [default: 20].
         --yyy    Drifting mine.
    """
    from docopt import docopt

    if __name__ == '__main__':
        res = docopt(__doc__, version="", help_message=False, argv=)
        print(res)

Docopot will turns all your usage pattern and options into a tidy dictionary:

    {'ship': False      'set': True                  '--drifting': False
     'new': False       'remove': False              '--rr': False
     'name': None       '--helping': False           '--aaa': 20
     'move': False      '--sorted': False            '--yyy': False
     'x': '50'          '--output': './test.txt'
     'y': '200'         '--version': False
     'shoot': False     '--speed': 10
     'mine': True       '--moored': True}


Features
--------

- ``docopt`` will match the useage pattern specified by you in the docstring and show errors if user input a wrong pattern.
- <value> means the required value from usage arguments
- [--option] means a opotion 
- for usage patterns ``docopt`` support (value1|value2) for required choices from user 
  and [-option1 | --option2] for optional choices from user
- for options, ``docopt`` support multiple keywords for one option e.g. -h --help
- for options that has an value, you can either use -option=<value> or -option VALUE.
- for multiple keywords in options, the output dictionay will only display the detailest (longest) keyword. 

Usage pattern format

The minimum case for docstring:

    """Usage: my_program.py

    """

The different cases for usage patterns:
    
    my_program.py #GOOD a pattern that has no parameter and arguments
    my_program.py ship #GOOD a pattern that has one required parameter
    my_program.py <value> #GOOD a pattern that has one required user input value
    
    



Optional Parameters
------------
``docopt`` provides 4 different parameters
- ``__doc__`` is a required parameter for ``docopt` to recevie the docstring from you program.
- ``version=""`` is a optional parameter that you can specify you program version in string and display to user
- ``help_message=False`` is a optional parameter that default is set to ``Ture``. 
    It allows ``docopt`` to show you docstring as well as the version specified above each time your program is excuted.
- ``argv=[]`` is also a optional parameter in which you can put an array of default arguments (must match your docstring usage pattern).



Mim Case for Docstring
----------

- Issue Tracker: github.com/$project/$project/issues
- Source Code: github.com/$project/$project

Support
-------

If you are having issues, please let us know.
We have a mailing list located at: project@google-groups.com

License
-------

The project is licensed under the MIT license.
