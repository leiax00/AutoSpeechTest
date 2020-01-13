# coding=utf-8
from common.time_util import format_time


class SimpleLogger:
    def __init__(self):
        self.level_info = 'INFO'
        self.level_warn = 'WARN'
        self.level_error = 'ERROR'
        self.level_debug = 'DEBUG'

    def info(self, msg):
        print('[%s**%s] %s' % (format_time(), self.level_info, msg))

    def warn(self, msg):
        print('[%s**%s] %s' % (format_time(), self.level_warn, msg))

    def error(self, msg):
        print('[%s**%s] %s' % (format_time(), self.level_error, msg))

    def debug(self, msg):
        print('[%s**%s] %s' % (format_time(), self.level_debug, msg))


logger = SimpleLogger()
