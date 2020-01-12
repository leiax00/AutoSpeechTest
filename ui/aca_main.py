# coding=utf-8
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from ui.component.combo_checkbox import ComboCheckBox
from ui.component.load_file import LoadFile


class ACAApp(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ACAApp, self).__init__(parent)
        self.__init_ui()

    def __init_ui(self):
        self.__init_basic_info()
        self.__init_content()

    def __init_content(self):
        self.top_layout = QtWidgets.QGridLayout()
        self.top_layout.setContentsMargins(20, 20, 20, 20)
        self.top_layout.addWidget(LoadFile(self, '导入配置', callback=self.load_conf), 0, 0, Qt.AlignLeft | Qt.AlignCenter)
        self.top_layout.addWidget(LoadFile(self, '导入语料', callback=self.load_wav), 1, 0, Qt.AlignLeft | Qt.AlignCenter)
        self.top_layout.addWidget(self.__init_com(), 2, 0, Qt.AlignLeft | Qt.AlignCenter)
        self.top_layout.addWidget(self.__init_play_style(), 3, 0, Qt.AlignLeft | Qt.AlignCenter)
        self.top_layout.addWidget(self.__init_control_btn(), 4, 0, Qt.AlignLeft | Qt.AlignCenter)
        self.top_layout.addWidget(self.__init_real_monitor(), 0, 1, 5, 1, Qt.AlignLeft | Qt.AlignCenter)
        self.setLayout(self.top_layout)

    def __init_play_style(self):
        w = QtWidgets.QWidget()
        a = QtWidgets.QHBoxLayout()
        l1 = QtWidgets.QLabel('播放方式：')
        emp = QtWidgets.QLabel()
        emp.setMinimumWidth(50)
        l2 = QtWidgets.QLabel('循环次数：')

        self.play_style = QtWidgets.QComboBox()
        self.play_style.setMinimumWidth(140)
        self.play_style.addItems(['a', 'b'])

        box2 = QtWidgets.QComboBox()
        box2.setMinimumWidth(140)
        box2.addItems(['1', '5', '10', '20', '50'])

        a.addWidget(l1)
        a.addWidget(self.play_style)
        a.addWidget(emp)
        a.addWidget(l2)
        a.addWidget(box2)
        w.setLayout(a)
        return w

    def __init_real_monitor(self):
        w = QtWidgets.QWidget()
        a = QtWidgets.QHBoxLayout()

        self.monitor_label = QtWidgets.QLabel()
        self.monitor_label.setStyleSheet('background-color: rgb(238,229,222);')
        self.monitor_label.setMinimumSize(300, 200)
        self.monitor_label.setText('''
  播放进度：0 / 0
  已播时长：00:00:00
  播放内容：
  识别内容：   
实时准确率: 0.00%
        ''')
        a.addWidget(self.monitor_label)

        w.setLayout(a)
        return w

    def __init_com(self):
        w = QtWidgets.QWidget()
        a = QtWidgets.QHBoxLayout()
        self.com_box = ComboCheckBox(items=['a', 'b', 'c'], callback=self.select_coms)
        a.addWidget(QtWidgets.QLabel('选择串口：'))
        a.addWidget(self.com_box)
        w.setLayout(a)
        return w

    def __init_control_btn(self):
        w = QtWidgets.QWidget()
        a = QtWidgets.QHBoxLayout()
        self.start_btn = QtWidgets.QPushButton('开始测试')
        emp = QtWidgets.QLabel()
        emp.setMinimumWidth(100)
        self.stop_btn = QtWidgets.QPushButton('暂停测试')
        self.result_btn = QtWidgets.QPushButton('查看报告')
        a.addWidget(self.start_btn)
        a.addWidget(emp)
        a.addWidget(self.stop_btn)
        a.addWidget(emp)
        a.addWidget(self.result_btn)
        w.setLayout(a)
        return w

    def __init_basic_info(self):
        self.setObjectName('ACA')
        self.setWindowTitle('ACA')
        self.setWindowIcon(QIcon(''))
        self.setGeometry(1000, 500, 600, 200)  # margin-x, margin-y, length, width

    def load_conf(self, conf_path=None):
        if conf_path is None:
            return
        print(conf_path)

    def load_wav(self, wav_path=None):
        if wav_path is None:
            return
        print(wav_path)

    def select_coms(self, coms):
        print(coms)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ACAApp()
    window.show()
    sys.exit(app.exec_())
