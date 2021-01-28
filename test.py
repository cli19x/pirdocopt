from docopt import docopt
import test_runner

if __name__ == '__main__':
    testing = docopt(test_runner.doc, version="test 2.0", help_message=False,
                     argv=test_runner.argv)
    print(testing)
