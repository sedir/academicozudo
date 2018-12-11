import json
import sys, os
from pathlib import Path

import pkg_resources

frozen = getattr(sys, 'frozen', False)
if frozen:
    bundle_dir = sys._MEIPASS
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
# print('we are', frozen, 'frozen')
# print('bundle dir is', bundle_dir)
# print('sys.argv[0] is', sys.argv[0])
# print('sys.executable is', sys.executable)
# print('os.getcwd is', os.getcwd())


def config(file='config.json'):
    path = bundle_dir
    if frozen:
        path = os.path.dirname(sys.executable)

    with open(Path(path) / file, 'r') as f:
        return json.load(f)


def get_internal_file(file: str or Path):
    path = bundle_dir
    if frozen:
        path = sys._MEIPASS

    return Path(path) / file


def get_root_file(file: str or Path):
    path = bundle_dir
    if frozen:
        path = os.path.dirname(sys.executable)

    return Path(path) / file
