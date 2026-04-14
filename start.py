import sys
from main import main
from mq import setup_queue

if __name__ == "__main__":
    if len(sys.argv) > 1:
        date_string = sys.argv[1]
        main(date_string)
    else:
        setup_queue()