import sys
import locale

from PyQt5 import uic

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
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
