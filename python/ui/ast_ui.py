# coding=utf-8
import os
import shutil
import sys
from threading import Thread
from time import sleep

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from audio_identify.identify import AudioIdentify
from common.logger import logger
from common.path_helper import get_remote_result_dir_name
from common.ssh_util import ssh_exec
from conf.config import corpus_conf
from conf.load_source import LoadSource
from obj.real_monitor_obj import RealMonitor
from ui.component.combo_checkbox import ComboCheckBox
from ui.component.load_file import LoadFile


class AstUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AstUI, self).__init__(parent)
        self.__init_data()
        self.__init_ui()

    def __init_data(self):
        self.service = AudioIdentify()
        self.threads = {}

    def __init_ui(self):
        self.__init_basic_info()
        self.__init_content()

    def __init_wav(self):
        def retrieve_wav():
            self.monitor_label.setText('wav检索中\n请检索完成再进行操作')
            ssh_exec()
            self.monitor_label.setText(format(RealMonitor()))

        self.threads['retrieve_wav'] = Thread(name='retrieve_wav', target=retrieve_wav, daemon=True)
        self.threads['retrieve_wav'].start()

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
        self.monitor_label.setText(format(RealMonitor()))
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
        self.result_btn = QtWidgets.QPushButton('上传结果')
        self.result_btn.clicked.connect(self.upload_result)
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

    def closeEvent(self, event):
        self.service.release()

    def load_conf(self, conf_path=None):
        """
        todo: 待实现
        :param conf_path:
        :return:
        """
        if conf_path is None or conf_path.strip('\n\r\t') == '':
            return
        corpus_conf.load_conf(conf_path)
        self.__init_wav()
        logger.info('set software conf path: %s' % conf_path)

    def load_wav(self, wav_path=None):
        if wav_path is None or str(wav_path).strip() == '':
            return
        logger.info('set wav path: %s' % wav_path)
        self.service.wav_mapping = LoadSource().parse_wav(wav_path, corpus_conf.wav_count_one_cmder)
        self.start_btn.setEnabled(True)

    def select_coms(self, com_l):
        logger.info('set com list: %s' % com_l)
        self.service.replace_collectors_by_com(com_l)

    def start_test(self):
        name = 'play_thread'
        listen_name = 'listen_{0}'.format(name)
        logger.info('%s start....' % name)
        self.threads[name] = Thread(name=name, target=self.service.process, daemon=True)
        self.threads[listen_name] = Thread(name=listen_name, target=self.listen_play, args=(name, self.start_btn),
                                           daemon=True)
        self.threads[name].start()
        self.threads[listen_name].start()

    def status_change(self):
        """
        stop仅操作播放是否暂停，后台的日志收集，数据处理空跑
        :return:
        """
        logger.info('test status change....')
        self.service.player.set_play(not self.service.player.is_play())
        self.status_btn.setText('暂停测试' if self.service.player.is_play() else '继续测试')

    def output_wav_text(self):
        logger.info('begin to export wav_text...')
        self.__init_wav()
        name = 'export_thread'
        listen_name = 'listen_{0}'.format(name)

        def export_wav(o):
            while o.threads['retrieve_wav'].is_alive():
                sleep(.5)
            self.monitor_label.setText("正在导出中，请勿操作界面！！")
            self.service.output_wav_text()
            self.monitor_label.setText(format(RealMonitor()))

        self.threads[name] = Thread(name=name, target=export_wav, args=(self,), daemon=True)
        self.threads[listen_name] = Thread(name=listen_name, target=self.listen_play, args=(name, self.out_wav),
                                           daemon=True)
        self.threads[name].start()
        self.threads[listen_name].start()

    def listen_play(self, name, o):
        """
        :param name: 线程名
        :type o: QtWidgets.QPushButton
        """
        while self.threads[name].is_alive():
            if o.isEnabled():
                o.setEnabled(False)
            sleep(.5)
        else:
            o.setEnabled(True)
            logger.info('%s end....' % name)

    def upload_result(self):
        archive_dir = get_remote_result_dir_name()
        shutil.copytree(corpus_conf.output_path, archive_dir)
        shutil.copytree(os.path.join(corpus_conf.soft_root, 'res'), os.path.join(archive_dir, 'res'))
        logger.info('upload result to server finish....')

    def set_play_count(self):
        corpus_conf.repeat_play_count = int(self.play_count_box.currentText())
        logger.info('set play count:%d' % corpus_conf.repeat_play_count)


def main():
    print('app start......')
    corpus_conf.load_conf()
    app = QApplication(sys.argv)
    window = AstUI()
    window.show()
    sys.exit(app.exec_())
