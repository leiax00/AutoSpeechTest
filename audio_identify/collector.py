# coding=utf-8
import threading
from time import sleep

import serial

from audio_identify.asr_queue import QUEUE


class Collector(threading.Thread):
    __start = True

    def __init__(self, com_number):
        super(Collector, self).__init__()
        self.com_number = com_number
        self.thread_name = '{0}:{1}'.format('collector', self.com_number)
        # self.serial = serial.Serial(port=self.com_number, baudrate=115200, timeout=0.5)

    def run(self):
        self.listen()

    def listen(self):
        # if not self.serial.isOpen():
        #     self.serial.open()

        i = 0
        while Collector.__start:
            # line = self.serial.readline()
            QUEUE.put(self.thread_name + ', line:' + str(i))
            i += 1
            sleep(1)

    def remove(self):
        Collector.__start = False
        # self.serial.close()
