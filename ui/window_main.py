from PyQt5.QtWidgets import QMainWindow, QMessageBox
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
