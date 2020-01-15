# coding=utf-8
from conf.config import corpus_conf


class LogFilter:
    def __init__(self):
        self.keywords = corpus_conf.log_filter

    def need_filter(self, str):
        for k in self.keywords:
            if k in str:
                return True
        return False


log_filter = LogFilter()
