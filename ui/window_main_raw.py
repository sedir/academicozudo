# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/window_main_raw.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(306, 405)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setDocumentMode(False)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.button_config = QtWidgets.QPushButton(self.centralwidget)
        self.button_config.setMinimumSize(QtCore.QSize(0, 50))
        self.button_config.setObjectName("button_config")
        self.verticalLayout.addWidget(self.button_config)
        self.button_executar = QtWidgets.QPushButton(self.centralwidget)
        self.button_executar.setMinimumSize(QtCore.QSize(0, 50))
        self.button_executar.setObjectName("button_executar")
        self.verticalLayout.addWidget(self.button_executar)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.toolBar.setFont(font)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_sobre = QtWidgets.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.action_sobre.setFont(font)
        self.action_sobre.setObjectName("action_sobre")
        self.toolBar.addAction(self.action_sobre)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Academicozudo"))
        self.button_config.setText(_translate("MainWindow", "Configurações"))
        self.button_executar.setText(_translate("MainWindow", "Executar script"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_sobre.setText(_translate("MainWindow", "Sobre"))
        self.action_sobre.setShortcut(_translate("MainWindow", "R"))

