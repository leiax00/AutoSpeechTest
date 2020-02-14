# coding=utf-8
import os
import re
import threading
from time import sleep

from audio_identify.asr_queue import aq
from common.logger import logger
from common.time_util import format_time
from conf.config import corpus_conf
from obj.audio_obj import AudioObj
from obj.default_log_obj import parse_default_log, write_default_log_2_csv


class Analyzer(threading.Thread):
    def __init__(self, func=parse_default_log):
        super(Analyzer, self).__init__()
        self.__start = True
        self.func = func

    def run(self):
        self.analyze()

    def analyze(self):
        while self.__start:
            try:
                if not aq.empty():
                    obj = aq.pop()
                    self.write_log(obj)
                    if self.func is not None:
                        self.func(obj)
            except Exception as e:
                logger.error('error happen when analyzing log, err:{0}'.format(e))
            finally:
                sleep(.001)  # 取消线程占用
        else:
            logger.info('analyzer thread finish....')

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


if __name__ == '__main__':
    """
    手动分析日志生成csv结果
    """
    log_path = r'C:\Users\Administrator\Desktop\bstd_result\bslight_191220_test_log.log'


    class Service:
        def __init__(self):
            self.can_write = True

    corpus_conf.load_conf()
    s = Service()
    threading.Thread(target=write_default_log_2_csv, args=(s,), daemon=True).start()
    with open(log_path, 'r', encoding='utf-8') as rf:
        for line in rf:
            re_str = r'cmd_info: (.*):(.*) -> log: (.*)'
            rst = re.match(re_str, line)
            if rst is not None:
                play_cmd = rst.group(1)
                wav_name = rst.group(2)
                log_info = rst.group(3)
                obj = AudioObj().set_v(wav_name, play_cmd, '')
                logs = [log.strip() for log in log_info.split('&&')]
                msg = [format_time(), 'COM12', obj, *logs]
                parse_default_log(msg)
    sleep(15)
    s.can_write = False
