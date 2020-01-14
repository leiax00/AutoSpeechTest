# coding=utf-8
import threading

from audio_identify.asr_queue import aq, AsrQueue


class Analyzer(threading.Thread):
    def __init__(self):
        super(Analyzer, self).__init__()
        self.__start = True

    def run(self):
        self.analyze()

    def analyze(self):
        while self.__start:
            if not aq.empty():
                obj = aq.pop()
                print('analyzer: {0} -> {1}'.format(obj[2].content, obj))

    @staticmethod
    def remove():
        Analyzer.__start = False
