import datetime
import sys
import locale

import qdarkstyle
from PyQt5 import uic

from config import Configuration

if not getattr(sys, 'frozen', False):
    uic.compileUiDir('./ui')

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QLocale
from ui.window_main import MainWindow


if __name__ == "__main__":
    try:
        locale.setlocale(locale.LC_ALL, "pt_BR")
        QLocale.setDefault(QLocale('pt_BR'))
    except:
        pass

    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
