import pip
from sys import platform


def main():

    f = open('requirements.txt')
    _all_ = f.readlines()
    f.close()

    f = open('requirements_windows.txt')
    windows = f.readlines()
    f.close()

    f = open('requirements_linux.txt')
    linux = f.readlines()
    f.close()

    f = open('requirements_darwin.txt')
    darwin = f.readlines()
    f.close()

    install(_all_)
    if platform == 'windows':
        install(windows)
    if platform == 'linux':
        install(linux)
    if platform == 'darwin':  # MacOS
        install(darwin)


def install(packages):
    for package in packages:
        pip.main(['install', package])

if __name__ == '__main__':
    main()