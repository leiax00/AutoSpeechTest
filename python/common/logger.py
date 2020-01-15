# coding=utf-8
import os
from queue import Queue
from threading import Thread

from common.time_util import format_time
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
        with open(os.path.join(corpus_conf.output_path,
                               'tool_log_{0}.log'.format(format_time(time_formatter='%Y%m%d%H%M%S'))), 'a',
                  encoding='utf-8') as wf:
            while True:
                if not self.queue.empty():
                    wf.write('{0}\n'.format(self.queue.get()))
                    wf.flush()

    def info(self, msg):
        info = '[%s**%s] %s' % (format_time(), self.level_info, msg)
        print(info)
        self.queue.put(info)

    def warn(self, msg):
        info = '[%s**%s] %s' % (format_time(), self.level_warn, msg)
        print(info)
        self.queue.put(info)

    def error(self, msg):
        info = '[%s**%s] %s' % (format_time(), self.level_error, msg)
        print(info)
        self.queue.put(info)

    def debug(self, msg):
        info = '[%s**%s] %s' % (format_time(), self.level_debug, msg)
        print(info)
        self.queue.put(info)


logger = SimpleLogger()
