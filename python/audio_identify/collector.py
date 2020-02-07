# coding=utf-8
import threading
from time import sleep

import serial

from audio_identify.asr_queue import aq
from audio_identify.emit.emiter import Receiver, observer
from common.content import cmd_dict
from common.logger import logger
from common.time_util import format_time
from conf.config import corpus_conf

start_symbol = 'start aca'
end_symbol = 'end aca'
enter_symbol = '> '
linux_cmd_symbol = '/bin/sh'
linux_newline_symbol = '# '


class Collector(Receiver):
    def __init__(self, com_device):
        super().__init__()
        self.__start = True
        self.com_device = com_device
        self.thread_name = '{0}:{1}'.format('collector', self.com_device)
        self.serial_com = serial.Serial(port=self.com_device, baudrate=115200, timeout=0.5)
        self.tmp_data = [format_time(), self.com_device]
        self.lock = threading.Lock()

    def run(self):
        while self.serial_com is None:
            try:
                self.serial_com = serial.Serial(port=self.com_device, baudrate=115200, timeout=0.5)
            except Exception as e:
                sleep(5)
                logger.error('com connect exception, e:{0}'.format(e))
        self.listen()

    def listen(self):
        if not self.serial_com.isOpen():
            self.serial_com.open()
        logger.info('com connect success, com:{0}'.format(self.com_device))
        while self.__start:
            try:
                line = self.serial_com.readline().decode(encoding='utf-8').strip('\r\n\t')
                if line is None or line == '' or line == enter_symbol \
                        or linux_cmd_symbol in line or line == linux_newline_symbol:
                    continue
                logger.info('com:{0} receive info: {1}'.format(self.com_device, line))
                if start_symbol in line:
                    cmd_str = line.split(':')[1]
                    self.tmp_data = [format_time(), self.com_device, cmd_dict.get(cmd_str)]
                    continue
                elif end_symbol in line:
                    aq.send(self.tmp_data)
                    continue
                else:
                    if not corpus_conf.log_filter.need_filter(line):
                        with self.lock:
                            self.tmp_data.append(line)
            except Exception as e:
                logger.warn('com: {0} may may not read log, e:{1}'.format(self.com_device, e))
            finally:
                sleep(.001)  # 取消线程占用

    def remove(self):
        self.__start = False
        self.serial_com.close()
        logger.info('success to close thread, com:{0}'.format(self.com_device))

    def on_notify(self, *o):
        pass

    def notify_start(self, *o):
        self.serial_com.write(bytes('{0}:{1}\n'.format(start_symbol, o[0]), encoding='utf-8'))

    def notify_end(self, *o):
        self.serial_com.write(bytes('{0}:{1}\n'.format(end_symbol, o[0]), encoding='utf-8'))


if __name__ == '__main__':
    c = Collector('COM5')
    observer.on_notify('aa')
