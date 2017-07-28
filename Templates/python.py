import os
import argparse

// Function example
def do_sth():
    return 10

// Class example
class MyClass():
    def say_hi():
        print("Hi!")

// Things to do when executed
if "__main__" == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", nargs=1, help="URL to read from")
    parser.add_argument("-d", "--directory", required=True, help="directory path for log files")
    parser.add_argument("--no-cache", dest="cache", action="store_false", help="disable caching")
    args = parser.parse_args()
