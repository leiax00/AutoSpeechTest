# coding=utf-8
import os
import sys
from threading import Thread

# pyqt5的bug,需要添加这段代码才能找到pyqt5.dll
from time import sleep

if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from audio_identify.identify import AudioIdentify
from common.conf_paser import parse_wav
from common.logger import logger
from conf.config import corpus_conf
from ui.component.combo_checkbox import ComboCheckBox
from ui.component.load_file import LoadFile


class ACAApp(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ACAApp, self).__init__(parent)
        self.__init_data()
        self.__init_ui()

    def __init_data(self):
        self.service = AudioIdentify()
        self.threads = {}

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
        self.com_box = ComboCheckBox(items=self.service.com_devices.copy(), callback=self.select_coms)
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
        self.status_btn = QtWidgets.QPushButton('暂停测试')
        self.status_btn.clicked.connect(self.status_change)
        self.out_wav = QtWidgets.QPushButton('输出语料')
        self.out_wav.clicked.connect(self.output_wav_text)
        self.result_btn = QtWidgets.QPushButton('查看报告')
        self.result_btn.clicked.connect(self.look_result)
        a.addWidget(emp)
        a.addWidget(self.start_btn)
        a.addWidget(self.status_btn)
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
        logger.info('set software conf path: %s' % conf_path)

    def load_wav(self, wav_path=None):
        if wav_path is None or str(wav_path).strip() == '':
            return
        logger.info('set wav path: %s' % wav_path)
        self.service.wav_mapping = parse_wav(wav_path, corpus_conf.wav_count_one_cmder)

    def select_coms(self, com_l):
        logger.info('set com list: %s' % com_l)
        self.service.replace_collectors_by_com(com_l)

    def start_test(self):
        name = 'play_thread'
        logger.info('%s start....' % name)
        self.threads[name] = Thread(name=name, target=self.service.player.play_all,
                                    args=(self.service.wav_mapping, corpus_conf.repeat_play_count), daemon=True)

        def listen_play():
            while self.threads[name].is_alive():
                if self.start_btn.isEnabled():
                    self.start_btn.setEnabled(False)
                sleep(.5)
            else:
                self.start_btn.setEnabled(True)
                logger.info('%s end....' % name)

        self.threads['listen_play'] = Thread(name=name, target=listen_play, daemon=True)
        self.threads[name].start()
        self.threads['listen_play'].start()

    def status_change(self):
        """
        stop仅操作播放是否暂停，后台的日志收集，数据处理空跑
        :return:
        """
        logger.info('test status change....')
        self.service.player.set_play(not self.service.player.is_play())
        self.status_btn.setText('暂停测试' if self.service.player.is_play() else '继续测试')

    def output_wav_text(self):
        logger.info('output_wav_text')
        self.service.output_wav_text()

    def look_result(self):
        logger.info('output_wav_text')
        pass

    def set_play_count(self):
        corpus_conf.wav_count_one_cmder = int(self.play_count_box.currentText())
        logger.info('set play count:%d' % corpus_conf.wav_count_one_cmder)


if __name__ == '__main__':
    corpus_conf.load_conf()
    app = QApplication(sys.argv)
    window = ACAApp()
    window.show()
    sys.exit(app.exec_())
