import getopt
import os
import sys

# Make library available in path
library_paths = [
    os.path.join(os.getcwd(), 'lib', 'log')
]

for p in library_paths:
    if not (p in sys.path):
        sys.path.insert(0, p)

# Import library classes
from telegram_logger import TelegramLogger

# Configuration
RELOAD_DATA = True
RECONVERT_DATA = True
CLEAN_DATA = True

# Set script path
file_path = os.path.realpath(__file__)
script_path = os.path.dirname(file_path)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "m:", ["message="])
    except getopt.GetoptError:
        print("message.py -m \"<message>\"")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("message.py -m \"<message>\"")
            sys.exit()
        elif opt in ("-m", "--message"):
            TelegramLogger().log_line(arg)


if __name__ == "__main__":
    main(sys.argv[1:])
