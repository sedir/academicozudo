import sys
import os
from distutils.core import setup
from Cython.Build import cythonize
import install_deps

try:
    from PyQt5 import uic
    if not getattr(sys, 'frozen', False):
        uic.compileUiDir('./ui')
except:
    pass

install_deps.main()

setup(
    ext_modules=cythonize(["config.py", "ui/dialog*.py", "ui/window*.py"])
)

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".c"):
            os.remove(os.path.join(root, file))