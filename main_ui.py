# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import sys
import locale

from PyQt5 import uic


if not getattr(sys, 'frozen', False):
    uic.compileUiDir('./ui')

from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import QLocale
from ui.window_main_raw import Ui_MainWindow
from ui.dialog_config import ConfigDialog


# noinspection PyCallByClass
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.action_sobre.triggered.connect(self.sobre)
        self.ui.button_config.clicked.connect(self.config)

    def sobre(self):
        QMessageBox.about(self, 'Sobre o Academicozudo', 'Academicozudo\n'
                                                         'Sistema de automação para o Acadêmico FUNCERN\n\n'
                                                         'Criado por Sedir Morais & Paulo de Tasso')

    def config(self):
        conf = ConfigDialog()
        conf.exec_()


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, "pt_BR")
    QLocale.setDefault(QLocale('pt_BR'))

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
