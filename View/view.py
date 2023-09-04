from Utils.common_utils import *
from graph_editor import GraphEditor

class View(QObject):
    def __init__(self) -> None:
        self.ui = QtWidgets.QMainWindow()
        graph_layout = QVBoxLayout()
        graph_layout.addWidget()
        # self.ui

    def show(self):
        self.ui.show()