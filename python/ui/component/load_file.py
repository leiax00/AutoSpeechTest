# coding=utf-8
import sys

from PyQt5 import QtWidgets


class LoadFile(QtWidgets.QWidget):
    count = 1

    def __init__(self, parent=None, name=None, callback=None):
        super(LoadFile, self).__init__(parent)
        self.name = name or ('load_component_' + str(LoadFile.count))
        LoadFile.count += 1
        self.__init_ui()
        self.callback = callback

    def __init_ui(self):
        top_layout = QtWidgets.QHBoxLayout()
        import_btn = QtWidgets.QPushButton(self.name)
        import_btn.setMinimumSize(100, 20)
        import_btn.clicked.connect(self.add_file)
        top_layout.addWidget(import_btn)
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setObjectName('import file')
        self.line_edit.setReadOnly(True)
        self.line_edit.setMinimumWidth(400)
        top_layout.addWidget(self.line_edit)
        self.setLayout(top_layout)

    def add_file(self):
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        f = dialog.getOpenFileName(self, 'open file', '../', "All Files (*)")
        self.line_edit.setText(f[0])
        if self.callback is not None:
            self.callback(f[0])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LoadFile()
    window.show()
    sys.exit(app.exec_())
