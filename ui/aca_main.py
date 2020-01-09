# coding=utf-8
import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from ui.component.load_file import LoadFile


class ACAApp(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ACAApp, self).__init__(parent)
        self.__init_ui()

    def __init_ui(self):
        self.set_basic_info()
        self.set_content()

    def set_content(self):
        top_layout = QtWidgets.QGridLayout()
        top_layout.addWidget(LoadFile(self), 0, 0)
        self.setLayout(top_layout)

    def set_basic_info(self):
        self.setWindowTitle('ACA')
        self.setWindowIcon(QIcon(''))
        self.setGeometry(1000, 500, 800, 500)  # margin-x, margin-y, length, width


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ACAApp()
    window.show()
    sys.exit(app.exec_())
