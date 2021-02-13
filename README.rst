``pirdocopt`` a helper for enhancing your command line project
==================================================================

API
============

.. code:: python

    from docopt import docopt
    arguments = docopt(__doc__, version="", help_message=Ture, argv=[])

How to Install
========================
It is simple just include ``docopt.py`` in you project folder and import the module ``import docoopt``.

Usages
========
When you have a command-line python program which contains a docstring and want to show user all the usage patterns
and the options that provided by you program, you just need to call docopt.py:

.. code:: python

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
