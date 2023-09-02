from Utils.common_utils import *


class View(QObject):
    def __init__(self) -> None:
        self.ui = QtWidgets.QMainWindow()


    def show(self):
        self.ui.show()