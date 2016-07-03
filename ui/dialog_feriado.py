import locale

from PyQt5.QtWidgets import QDialog

from ui.dialog_feriado_raw import Ui_Dialog


class FeriadoDialog(QDialog):

    def __init__(self, parent=None):
        super(FeriadoDialog, self).__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def accept(self):
        super(FeriadoDialog, self).accept()

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def getdatetime(parent=None):
        dialog = FeriadoDialog(parent)
        result = dialog.exec_()
        date = dialog.ui.calendarWidget.selectedDate()
        return date.toPyDate(), result == QDialog.Accepted
