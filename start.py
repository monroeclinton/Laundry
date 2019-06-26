import getpass
import os
import sys
import argparse
from umdlaundry import main


def start():
    username = sys.argv[1]
    password = getpass.getpass('Password:')

    main.main(username, password)


if __name__ == '__main__':
    app_dir = os.path.dirname(os.path.abspath(__file__))
    # Change working dir to start.py dir
    os.chdir(app_dir)

    parser = argparse.ArgumentParser(
        description='''Discord Bot that alerts users privately when a washer/drier becomes available in their dorm. '''
    )
    parser.add_argument('username', type=str, help='Your UMD directory ID')

    args = parser.parse_args()
    if not args.username:
        parser.error("-u [Your UMD directory ID] argument is required")

    start()
