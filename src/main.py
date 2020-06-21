import sys
from graph_lib import test_func


def main(path: str, start: str, end: str):
    test_func(path, start, end)


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 3:
        exit("Usage: python3 script.py path/to/Stooq/sheets YYYYMMDD YYYYMMDD")

    sys.exit(main(args[0], args[1], args[2]))
