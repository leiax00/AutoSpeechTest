# coding=utf-8
import threading

import serial

from audio_identify.asr_queue import aq
from audio_identify.emit.emiter import Receiver, observer
from audio_identify.filter.log_filter import log_filter
from common.logger import logger
from common.time_util import format_time


class Collector(Receiver):
    def __init__(self, com_device):
        super().__init__()
        self.__start = True
        self.com_device = com_device
        self.thread_name = '{0}:{1}'.format('collector', self.com_device)
        self.serial = serial.Serial(port=self.com_device, baudrate=115200, timeout=0.5)
        self.tmp_data = [format_time(), self.com_device]

    def run(self):
        self.listen()

    def listen(self):
        if not self.serial.isOpen():
            self.serial.open()

        while self.__start:
            line = self.serial.readline().decode(encoding='utf-8').strip('\r\n\t')
            if line is not None and line != '' and not log_filter.need_filter(line):
                self.tmp_data.append(line)

    def remove(self):
        self.__start = False
        self.serial.close()
        logger.info('success to close thread, com:{0}'.format(self.com_device))

    def on_notify(self, *o):
        self.tmp_data.insert(2, o[0])
        aq.send(self.tmp_data)
        self.tmp_data = [format_time(), self.com_device]  # 可能存在多线程问题


if __name__ == '__main__':
    c = Collector('COM5')
    observer.notify('aa')
