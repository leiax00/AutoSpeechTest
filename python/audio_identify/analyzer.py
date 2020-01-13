# coding=utf-8
import threading

from audio_identify.asr_queue import aq, AsrQueue


class Analyzer(threading.Thread):
    __start = True

    def __init__(self):
        super(Analyzer, self).__init__()

    def run(self):
        self.analyze()

    def analyze(self):
        while Analyzer.__start:
            if not aq.empty():
                print('analyzer:', aq.pop())

    @staticmethod
    def remove():
        Analyzer.__start = False
