# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './dialog_config_raw.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!
import locale
import datetime
from functools import partial

from PyQt5.QtWidgets import QDialog, QDateEdit, QLineEdit, QListWidget
from PyQt5.QtCore import QDate

from ui.dialog_config_raw import Ui_Dialog
from ui.dialog_feriado import FeriadoDialog
from config import Configuration


class ConfigDialog(QDialog):
    def __init__(self):
        super(ConfigDialog, self).__init__()

        locale.setlocale(locale.LC_ALL, "pt_BR")

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.config = Configuration.load_configuration()

        self.ui.dateEdit_inicio.setDate(self.config.start_date)
        self.ui.dateEdit_fim.setDate(self.config.end_date)
        self.ui.lineEdit_usuario.setText(self.config.user)
        self.ui.lineEdit_senha.setText(self.config.password)
        self.ui.button_adicionar_feriado.clicked.connect(self.adicionar_feriado)
        self.ui.button_remover_feriado.clicked.connect(self.remover_feriado)

        for f in self.config.holidays:
            self.ui.listWidget_feriados.addItem(f.strftime('%a, %d/%m/%Y'))

        self.ui.dateEdit_inicio.dateChanged.connect(partial(self.alterar_config, 'start_date', self.ui.dateEdit_inicio))
        self.ui.dateEdit_fim.dateChanged.connect(partial(self.alterar_config, 'end_date', self.ui.dateEdit_fim))
        self.ui.lineEdit_usuario.textChanged.connect(partial(self.alterar_config, 'user', self.ui.lineEdit_usuario))
        self.ui.lineEdit_senha.textChanged.connect(partial(self.alterar_config, 'password', self.ui.lineEdit_senha))
        listconnect = partial(self.alterar_config, 'holidays', self.ui.listWidget_feriados)
        self.ui.listWidget_feriados.model().rowsInserted.connect(listconnect)
        self.ui.listWidget_feriados.model().rowsRemoved.connect(listconnect)
        self.ui.listWidget_feriados.model().rowsMoved.connect(listconnect)

    def alterar_config(self, name, comp):
        if isinstance(comp, QDateEdit):
            val = comp.date().toPyDate()
        elif isinstance(comp, QLineEdit):
            val = comp.text()
        elif isinstance(comp, QListWidget):
            print('teste')
            val = [datetime.datetime.strptime(comp.item(x).text(), '%a, %d/%m/%Y').date()
                   for x in range(0, comp.count())]

        setattr(self.config, name, val)

    def adicionar_feriado(self):
        date, ok = FeriadoDialog.getdatetime(self)
        if ok:
            self.ui.listWidget_feriados.addItem(date.strftime('%a, %d/%m/%Y'))

    def remover_feriado(self):
        self.ui.listWidget_feriados.takeItem(self.ui.listWidget_feriados.currentRow())

    def accept(self):
        self.config.save()
        super(ConfigDialog, self).accept()
