from threading import Event

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from config import Configuration
from log import QtPanelHandler
from thread import Threadzuda
from ui.window_main_raw import Ui_MainWindow
from ui.dialog_config import ConfigDialog


# noinspection PyCallByClass
class MainWindow(QMainWindow):
    signal_log = pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__(None, QtCore.Qt.WindowStaysOnTopHint)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.action_sobre.triggered.connect(self.sobre)
        self.ui.button_config.clicked.connect(self.config)
        self.ui.button_executar.clicked.connect(self.iniciar_parar)

        self.signal_log.connect(self.atualizar_log)
        self.done = Event()
        self.control_thread = None
        QtPanelHandler(self.signal_log)




    def sobre(self):
        QMessageBox.about(self, 'Sobre o Academicozudo', 'Academicozudo\n'
                                                         'Sistema de automação para o Acadêmico FUNCERN\n\n'
                                                         'Criado por Sedir Morais & Paulo de Tasso')

    def config(self):
        conf = ConfigDialog()
        conf.exec_()

    @pyqtSlot(str)
    def atualizar_log(self, log):
        self.ui.textEdit.moveCursor(QTextCursor.End)
        self.ui.textEdit.insertPlainText(log)
        self.ui.textEdit.moveCursor(QTextCursor.End)

    def iniciar_parar(self):
        if not self.control_thread:
            self.control_thread = Threadzuda(Configuration.load(), self.done)
            self.control_thread.start()
            return
        if self.control_thread.is_alive():
            self.done.set()
        elif self.control_thread.is_started():
            self.done = Event()
            self.control_thread = Threadzuda(Configuration.load(), self.done)
            self.control_thread.start()
        else:
            self.control_thread.start()



