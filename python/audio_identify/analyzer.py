# coding=utf-8
import threading

from audio_identify.asr_queue import aq
from obj.default_log_obj import parse_default_log


class Analyzer(threading.Thread):
    def __init__(self, func=parse_default_log):
        super(Analyzer, self).__init__()
        self.__start = True
        self.func = func

    def run(self):
        self.analyze()

    def analyze(self):
        while self.__start:
            if not aq.empty():
                obj = aq.pop()
                print('analyzer: {0} -> {1}'.format(obj[2].content, obj))
                if self.func is not None:
                    self.func(obj)


    @staticmethod
    def remove():
        Analyzer.__start = False
