# coding=utf-8
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from audio_identify.identify import AudioIdentify
from common.conf_paser import get_wav_mapping
from conf.config import CorpusConf
from ui.component.combo_checkbox import ComboCheckBox
from ui.component.load_file import LoadFile


class ACAApp(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ACAApp, self).__init__(parent)
        self.service = AudioIdentify()
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
        self.play_style.addItems(['顺序播放'])

        self.play_count_box = QtWidgets.QComboBox()
        self.play_count_box.setMinimumWidth(140)
        self.play_count_box.addItems(['1', '5', '10', '20', '50'])
        self.play_count_box.activated.connect(self.set_play_count)

        a.addWidget(l1)
        a.addWidget(self.play_style)
        a.addWidget(emp)
        a.addWidget(l2)
        a.addWidget(self.play_count_box)
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
        self.com_box = ComboCheckBox(items=self.service.com_devices, callback=self.select_coms)
        a.addWidget(QtWidgets.QLabel('选择串口：'))
        a.addWidget(self.com_box)
        w.setLayout(a)
        return w

    def __init_control_btn(self):
        w = QtWidgets.QWidget()
        a = QtWidgets.QHBoxLayout()
        emp = QtWidgets.QLabel()
        emp.setMinimumWidth(80)
        self.start_btn = QtWidgets.QPushButton('开始测试')
        self.start_btn.clicked.connect(self.start_test)
        self.stop_btn = QtWidgets.QPushButton('暂停测试')
        self.stop_btn.clicked.connect(self.stop_test)
        self.out_wav = QtWidgets.QPushButton('输出语料')
        self.out_wav.clicked.connect(self.output_wav_text)
        self.result_btn = QtWidgets.QPushButton('查看报告')
        self.result_btn.clicked.connect(self.look_result)
        a.addWidget(emp)
        a.addWidget(self.start_btn)
        a.addWidget(self.stop_btn)
        a.addWidget(self.out_wav)
        a.addWidget(self.result_btn)
        w.setLayout(a)
        return w

    def __init_basic_info(self):
        self.setObjectName('ACA')
        self.setWindowTitle('ACA')
        self.setWindowIcon(QIcon(''))
        self.setGeometry(200, 200, 600, 200)  # margin-x, margin-y, length, width

    def load_conf(self, conf_path=None):
        """
        todo: 待实现
        :param conf_path:
        :return:
        """
        if conf_path is None:
            return
        print('set software conf path: %s' % conf_path)

    def load_wav(self, wav_path=None):
        if wav_path is None:
            return
        print('set wav path:' % wav_path)
        self.service.wav_mapping = get_wav_mapping()

    def select_coms(self, com_l):
        print('set com list: %s' % com_l)
        self.service.replace_collectors_by_com(com_l)

    def start_test(self):
        print('start_test')
        pass

    def stop_test(self):
        print('stop_test')
        pass

    def output_wav_text(self):
        print('output_wav_text')
        pass

    def look_result(self):
        print('output_wav_text')
        pass

    def set_play_count(self):
        CorpusConf.WAV_COUNT_ONE_CMDER = int(self.play_count_box.currentText())
        print('set play count:%d' % CorpusConf.WAV_COUNT_ONE_CMDER)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ACAApp()
    window.show()
    sys.exit(app.exec_())
