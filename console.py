import locale
from threading import Event

from PyQt5.QtCore import QLocale

from config import Configuration
from thread import Threadzuda

if __name__ == '__main__':
    try:
        locale.setlocale(locale.LC_ALL, "pt_BR")
        QLocale.setDefault(QLocale('pt_BR'))
    except:
        pass

    config = Configuration.load()

    thread = Threadzuda(Configuration.load(), Event())
    thread.start()

    thread.join()


