# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dialog_config_raw.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import QDialog

from ui.dialog_config_raw import Ui_Dialog


class ConfigDialog(QDialog):

    def __init__(self):
        super(ConfigDialog, self).__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
