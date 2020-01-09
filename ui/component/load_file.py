# coding=utf-8
import sys

from PyQt5 import QtWidgets


class LoadFile(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(LoadFile, self).__init__(parent)
        self.__init_ui()

    def __init_ui(self):
        top_layout = QtWidgets.QGridLayout()
        top_layout.addWidget(QtWidgets.QLabel(r'导入文件：'), 0, 0)
        import_btn = QtWidgets.QPushButton(r'导入文件')
        import_btn.clicked.connect(self.showDialog)
        top_layout.addWidget(import_btn, 0, 1)
        self.setLayout(top_layout)

    def showDialog(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        f = dialog.getOpenFileName(self, 'open file', './', "All Files (*);;Text Files (*.py)")
        print(f)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LoadFile()
    window.show()
    sys.exit(app.exec_())
