import sys


def main(args=None):
    if args is None:
        args = sys.argv[1:]
        print("This is the main routine")


if __name__ == '__main__':
    main()
