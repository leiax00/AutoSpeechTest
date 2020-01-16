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
        self.serial_com = None
        self.tmp_data = [format_time(), self.com_device]
        self.setDaemon(True)

    def run(self):
        while self.serial_com is None:
            try:
                self.serial_com = serial.Serial(port=self.com_device, baudrate=115200, timeout=0.5)
            except Exception as e:
                logger.error('com connect exception, e:{0}'.format(e))
        self.listen()

    def listen(self):
        if not self.serial_com.isOpen():
            self.serial_com.open()
        logger.info('com connect success, com:{0}'.format(self.com_device))
        while self.__start:
            try:
                line = self.serial_com.readline().decode(encoding='utf-8').strip('\r\n\t')
                if line is not None and line != '' and not log_filter.need_filter(line):
                    self.tmp_data.append(line)
            except Exception as e:
                logger.warn('com may may not read log, e:{0}'.format(e))

    def remove(self):
        self.__start = False
        self.serial_com.close()
        logger.info('success to close thread, com:{0}'.format(self.com_device))

    def on_notify(self, *o):
        self.tmp_data.insert(2, o[0])
        aq.send(self.tmp_data)
        self.tmp_data = [format_time(), self.com_device]  # 可能存在多线程问题


if __name__ == '__main__':
    c = Collector('COM5')
    observer.notify('aa')
