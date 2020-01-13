# coding=utf-8
import threading

import serial

from audio_identify.asr_queue import aq
from audio_identify.emit.emiter import Receiver, observer
from audio_identify.filter.log_filter import log_filter
from common.time_util import format_time


class Collector(threading.Thread, Receiver):
    __start = True

    def __init__(self, com_device):
        super(Collector, self).__init__()
        self.com_device = com_device
        self.thread_name = '{0}:{1}'.format('collector', self.com_device)
        self.serial = serial.Serial(port=self.com_device, baudrate=115200, timeout=0.5)
        self.tmp_data = [format_time(), self.com_device]
        observer.register(self)

    def run(self):
        self.listen()

    def listen(self):
        if not self.serial.isOpen():
            self.serial.open()

        while Collector.__start:
            line = self.serial.readline().decode(encoding='utf-8').strip('\r\n\t')
            if line is not None and line != '' and not log_filter.need_filter(line):
                self.tmp_data.append(line)

    def remove(self):
        Collector.__start = False
        self.serial.close()

    def on_notify(self):
        if len(self.tmp_data) > 2:
            aq.send(self.tmp_data)
            self.tmp_data = [format_time(), self.com_device]  # 可能存在多线程问题