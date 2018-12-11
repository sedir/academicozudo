from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip
from pip._internal import main as pipmain

from sys import platform


def main():
    pfile = Project(chdir=False).parsed_pipfile
    requirements = convert_deps_to_pip(pfile['packages'], r=False)
    test_requirements = convert_deps_to_pip(pfile['dev-packages'], r=False)

    install(requirements)


def install(packages):
    print(packages)
    for package in packages:
        pipmain(['install', package])

if __name__ == '__main__':
    main()