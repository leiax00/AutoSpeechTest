# coding=utf-8
import threading
import time
from time import sleep

import serial

from audio_identify.asr_queue import aq
from audio_identify.emit.emiter import Receiver, observer
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
        self.serial_com = None
        self.tmp_data = [format_time(), self.com_device]
        self.lock = threading.Lock()

    def run(self):
        while self.serial_com is None:
            try:
                self.serial_com = serial.Serial(port=self.com_device, baudrate=115200, timeout=.01)
                logger.info('com connect success, com:{0}'.format(self.com_device))
            except Exception as e:
                sleep(5)
                logger.error('com connect exception, e:{0}'.format(e))
        self.listen()

    def listen(self):
        ave_t = []
        while self.__start:
            try:
                start = int(round(time.time() * 1000))
                line = self.serial_com.readline().decode(encoding='utf-8').strip('\r\n\t')
                if line is None or line == '':
                    continue
                ave_t.append(int(round(time.time() * 1000)) - start)
                logger.info(
                    'com:{0} receive info: {1}, cost:{2}'.format(self.com_device, line, int(sum(ave_t) / len(ave_t))))
                if not corpus_conf.log_filter.need_filter(line):
                    with self.lock:
                        self.tmp_data.append(line)
            except Exception as e:
                logger.warn('com: {0} may may not read log, e:{1}'.format(self.com_device, e))
            finally:
                sleep(.001)  # 取消线程占用
        else:
            logger.info('com:{0} collector thread finish....'.format(self.com_device))

    def remove(self):
        self.__start = False
        self.serial_com.close()
        logger.info('success to close thread, com:{0}'.format(self.com_device))

    def on_notify(self, *o):
        with self.lock:
            self.tmp_data.insert(2, o[0])
            aq.send(self.tmp_data)
            self.tmp_data = [format_time(), self.com_device]

    def notify_start(self, *o):
        pass

    def notify_end(self, *o):
        pass


if __name__ == '__main__':
    c = Collector('COM5')
    observer.on_notify('aa')
