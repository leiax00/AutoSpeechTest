# coding=utf-8
import os
from queue import Queue
from threading import Thread

from common.time_util import format_time_4_log
from conf.config import corpus_conf


class SimpleLogger:
    def __init__(self):
        self.queue = Queue()
        self.level_info = 'INFO'
        self.level_warn = 'WARN'
        self.level_error = 'ERROR'
        self.level_debug = 'DEBUG'
        self.w_thread = Thread(name='log_write', target=self.start_write)
        self.w_thread.setDaemon(True)
        self.w_thread.start()

    def start_write(self):
        count, tmp_log = 0, ''
        with open(os.path.join(corpus_conf.output_path,
                               'tool_log_{0}.log'.format(corpus_conf.start_time)), 'a',
                  encoding='utf-8') as wf:
            while True:
                if not self.queue.empty():
                    count += 1
                    info = self.queue.get()
                    if 'pick bug' not in info:
                        print(info)
                    tmp_log += '{0}\n'.format(info)
                    if count == 100:
                        wf.write(tmp_log)
                        wf.flush()
                        tmp_log, count = '', 0

    def info(self, msg):
        info = '[%s**%s] %s' % (format_time_4_log(), self.level_info, msg)
        self.queue.put(info)

    def warn(self, msg):
        info = '[%s**%s] %s' % (format_time_4_log(), self.level_warn, msg)
        self.queue.put(info)

    def error(self, msg):
        info = '[%s**%s] %s' % (format_time_4_log(), self.level_error, msg)
        self.queue.put(info)

    def debug(self, msg):
        info = '[%s**%s] %s' % (format_time_4_log(), self.level_debug, msg)
        self.queue.put(info)


logger = SimpleLogger()
