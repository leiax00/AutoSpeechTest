# coding=utf-8
import os
import threading

from audio_identify.asr_queue import aq
from common.logger import logger
from conf.config import corpus_conf
from obj.default_log_obj import parse_default_log


class Analyzer(threading.Thread):
    def __init__(self, func=parse_default_log):
        super(Analyzer, self).__init__()
        self.__start = True
        self.func = func
        self.setDaemon(True)

    def run(self):
        self.analyze()

    def analyze(self):
        while self.__start:
            if not aq.empty():
                obj = aq.pop()
                self.write_log(obj)
                if self.func is not None:
                    self.func(obj)

    @staticmethod
    def write_log(obj):
        logger.info('analyzer: {0} -> {1}'.format(obj[2].content, obj))
        file_name = '{0}_test_log.log'.format(corpus_conf.log_name_by_serial.get(obj[1]))
        with open(os.path.join(corpus_conf.output_path, file_name), 'a', encoding='utf-8') as wf:
            cmd_str = '{0}:{1}'.format(obj[2].content, obj[2].aid)
            log_info = '' if len(obj) <= 3 else ' && '.join(obj[3:])
            wf.write('cmd_info: {0} -> log: {1}\n'.format(cmd_str, log_info))

    def remove(self):
        self.__start = False
        logger.info('success to close Analyzer thread, status:{0}'.format(self.__start))
