from View.view import View
from Utils.common_utils import *
import sys
import qdarktheme

class Controller():
    def __init__(self) -> None:
        self.app = QApplication([])
        self.view = View()
        qdarktheme.setup_theme()


    def run(self):
        self.view.show()
        self.app.exec_()

    def sigint_handler(self, signum = None, frame = None):
        sys.exit(self.app.exec_())