from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
import locale
from config import Configuration
from thread import Threadzuda
from threading import Event
from log import ConsolePanelHandler

locale.setlocale(locale.LC_ALL, 'pt_BR')


class RootWidget(FloatLayout):
    pass


class MainApp(App):
    def __init__(self):
        super().__init__()
        self.config = Configuration.load()
        self.threadDone = Event()
        self.thread = Threadzuda(self.config, self.threadDone)

    def start_stop(self):
        if self.thread.is_alive():
            self.threadDone.set()
        elif self.thread.is_started():
            self.threadDone = Event()
            self.thread = Threadzuda(self.config, self.threadDone)
            self.thread.start()
        else:
            self.thread.start()

    def write_config(self, prop, value):
        setattr(self.config, prop, value)
        self.config.save()

    def load_config(self, prop=None):
        if prop is not None:
            return getattr(self.config, prop)
        return prop

    def build(self):
        self.title = 'Academicozudo'
        return RootWidget()

    def on_start(self):
        super(MainApp, self).on_start()
        ConsolePanelHandler(self.root.ids.log_input)


if __name__ == '__main__':
    MainApp().run()
