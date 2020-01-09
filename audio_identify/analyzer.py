# coding=utf-8
import threading

from audio_identify.asr_queue import QUEUE


class Analyzer(threading.Thread):
    __start = True

    def __init__(self):
        super(Analyzer, self).__init__()

    def run(self):
        self.analyze()

    def analyze(self):
        while True:
            if not QUEUE.empty():
                print(QUEUE.get())

    @staticmethod
    def remove():
        Analyzer.__start = False
