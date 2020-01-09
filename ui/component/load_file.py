# coding=utf-8
import sys

from PyQt5 import QtWidgets


class LoadFile(QtWidgets.QLayout):
    def __init__(self, parent=None):
        super(LoadFile, self).__init__(parent)
        self.__init_ui()

    def __init_ui(self):
        top_layout = QtWidgets.QGridLayout()
        top_layout.addWidget(QtWidgets.QLabel(r'导入文件：'), 0, 0)
        import_btn = QtWidgets.QPushButton()
        import_btn.setObjectName(r'导入文件')
        action = QtWidgets.QAction('open', self)
        action.setShortcut("Ctrl + 0")
        action.setStatusTip('open new file')
        action.triggered().connect(self.showDialog)
        import_btn.addAction(action)
        top_layout.addWidget(import_btn, 0, 1)
        self.setLayout(top_layout)

    def showDialog(self):
        print('aaaaaaa')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LoadFile()
    window.show()
    sys.exit(app.exec_())
